import asyncio
import json
import aiohttp
import copy
import logging
import datetime

logger = logging.getLogger(__name__)
consumers = {}


class DceException(Exception):
    def __init__(self, error, data):
        self.error = error
        self.data = data

    def __repr__(self):
        return self.error

    def __str__(self):
        return self.error


def consumer(func):
    consumers[func.__name__] = func

    async def wrapped():
        return await func()
    return wrapped


class Dce:
    def __init__(self, url, session_params=None, connection_params=None, on_connect=None):
        self.ws_url = url
        self.session_params = session_params if session_params else {}  # aiohttp.ClientSession params
        self.connection_params = connection_params if connection_params else {}  # session.ws_connect params
        self.ws_socket = None
        self.loop = asyncio.get_event_loop()
        self.connection_task = self.loop.create_task(self.connect(), name='connect')
        self.cmd_id = 0
        self.futures = {}
        self.closed = False
        self.connected = asyncio.Event()
        self.on_connect = on_connect

    def close(self):
        self.closed = True
        if self.ws_socket:
            self.loop.run_until_complete(self.ws_socket.close())
        self.loop.run_until_complete(self.connection_cancel())
        logger.debug(f'[dce client] close: {self.ws_url}')

    async def connection_cancel(self):
        self.connection_task.cancel()
        try:
            await asyncio.wait({self.connection_task})
        except asyncio.CancelledError:
            await asyncio.wait({self.connection_task})
            raise

    async def _connect(self):
        try:
            async with aiohttp.ClientSession(**self.session_params) as session:
                async with session.ws_connect(self.ws_url, **self.connection_params) as self.ws_socket:
                    logger.debug(f'[dce client] open: {self.ws_url}')
                    self.connected.set()
                    if self.on_connect:
                        self.loop.create_task(self.on_connect(self))

                    async for msg in self.ws_socket:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            await self.on_message(msg)
                        elif msg.type == aiohttp.WSMsgType.CLOSED:
                            await self.on_closed(msg)
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            await self.on_error(msg)

        except asyncio.CancelledError:
            pass
        except aiohttp.ClientError as e:
            logger.error(f'[dce client] {e}')
        except Exception as e:
            logger.exception(f'[dce client] {e}')

    async def connect(self):
        while True:
            self.connected.clear()
            if self.closed:
                break
            await self._connect()
            await asyncio.sleep(1)

    async def on_message(self, msg):
        async def task():
            try:
                data = json.loads(msg.data)

                if data['msg_type'] == 'service':
                    return

                cmd_id = data['cmd_id']

                # rpc response
                if cmd_id:
                    future = self.futures.get(cmd_id, None)
                    if not future or future['future'].cancelled():
                        return
                    if future['future'].cancelled():
                        return

                    elapsed = (datetime.datetime.now() - future['created']).total_seconds()

                    if data['status'] == 'error':
                        logger.debug(f'[dce client] <- [{cmd_id}] {future["endpoint"]} {elapsed} {data["error"]}')
                        future['future'].set_exception(DceException(error=data['error'], data=data['error_data']))
                    else:
                        logger.debug(f'[dce client] <- [{cmd_id}] {future["endpoint"]} {elapsed}')
                        future['future'].set_result(data['data'])

                # consumer data
                else:
                    tasks = []
                    for c in data['consumers']:
                        if _consumer := consumers.get(c, None):
                            tasks.append(_consumer(data))
                    await asyncio.gather(*tasks)

            except asyncio.CancelledError:
                pass
        asyncio.create_task(task())

    async def on_closed(self, msg):
        raise Exception(f'Connection closed: {msg}')

    async def on_error(self, msg):
        raise Exception(f'Connection error: {msg}')

    async def send(self, request):
        await self.connected.wait()
        await self.ws_socket.send_str(request)

    async def request(self, endpoint, data, push=False):
        self.cmd_id += 1
        cmd_id = copy.deepcopy(self.cmd_id)
        try:
            req = json.dumps({'endpoint': endpoint, 'cmd_id': cmd_id, 'data': data})
            if not push:
                await self.send(req)
                logger.debug(f'[dce client] -> [{cmd_id}] {endpoint} {data}')
                future = self.loop.create_future()
                self.futures[cmd_id] = {'future': future, 'created': datetime.datetime.now(), 'endpoint': endpoint}
                return await future
            else:
                await self.send(req)
                logger.debug(f'[dce client] -> [{cmd_id}] [push] {endpoint} {data}')

        except asyncio.CancelledError as e:
            future = self.futures.pop(cmd_id)
            cancel_req = json.dumps({'endpoint': endpoint, 'cmd_id': cmd_id, 'data': None, 'cancel': True})
            self.loop.create_task(self.send(cancel_req))
            elapsed = (datetime.datetime.now() - future['created']).total_seconds()
            logger.debug(f'[dce client] <- [{cmd_id}] {endpoint} {elapsed} CancelledError')
            raise e
        except DceException as e:
            self.futures.pop(cmd_id)
            raise e


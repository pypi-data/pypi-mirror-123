# Django channels endpoints

This package provides endpoints as functions for django [channels](https://github.com/django/channels)
package.

# Installation

```shell
pip install channels-endpoints
```

# Usage
In your django app create dce.py file: 

```python
from channels_endpoints.main import endpoint, Response
from django.contrib.auth.models import User
from django.core import serializers
from .permissions import UsersPermissions
from asgiref.sync import sync_to_async


users_logger = logging.getLogger('users')


@endpoint(logger=users_logger, permissions=[UsersPermissions], timeout=42)
async def get_users(request):
    
    print(request.data)
    
    def _get():
        return serializers.serialize('python', User.objects.all(), fields=('username', 'id'))

    await request.consumer.send(text_data=Response(None, f'hello', consumers=['SomeConsumer']))
    
    return Response(
        request,
        await sync_to_async(_get)()
    )
```

## Python client:

```python
from channels_endpoints.client import Dce, DceException, consumer

@consumer
async def SomeConsumer(response):
    print(f'SomeConsumer: {response["data"]}')
    
dce = Dce('http://127.0.0.1:8000/ws/')

try:
    data = await dce.request('myapp.get_users', {'some': 'data'})
except DceException as e:
    print(e.__repr__())

dce.close()
```

## Javascript client:

```js
import {dce, consumer} from "channels_endpoints"

consumer('SomeConsumer', (response) => {
    console.log('SomeConsumer: ', response.data)
})

dce('myapp.get_users', {some: "data"}).then(
    response => {
        console.log('users:', response)
    }
)
```

see js client package [https://www.npmjs.com/package/channels_endpoints](https://www.npmjs.com/package/channels_endpoints)


# Examples

For complete usage examples see [example chat](https://github.com/avigmati/chat_project)

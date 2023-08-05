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


users_logger = logging.getLogger('users')


@endpoint(logger=users_logger, permissions=[UsersPermissions], timeout=42)
async def get_users(request):
    
    print(request.data)
    
    def _get():
        return serializers.serialize('python', User.objects.all())

    return Response(
        request,
        await sync_to_async(_get)()
    )
```

And in javascript on client side:

```js
import {dce} from "channels_endpoints"

dce('myapp.get_users', {some: "data"}).then(
    response => {
        console.log('users:', response)
    }
)
```

see js client package [https://www.npmjs.com/package/channels_endpoints](https://www.npmjs.com/package/channels_endpoints)



# Example

Django project  [example chat](https://github.com/avigmati/chat_project)

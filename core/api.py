from typing import Any, Optional
from django.http import HttpRequest
from ninja import NinjaAPI, Router
from ninja.security import HttpBearer

# Declare an auth scheme that will always fail.
class CustomAuth(HttpBearer):
    def authenticate(self, request, token):
        return False

# Create the API with a system wide auth.
api = NinjaAPI(auth=CustomAuth())

# Create the routers
first_router = Router()
second_router = Router()

# This endpoint will end up being /api/first/first
@first_router.get('/first')
def first(request):
    return 'first'

# This endpoint will end up being /api/second/second
@second_router.get('/second')
def second(request):
    return 'second'

# I expect this router to be restricted.
api.add_router('/first', first_router)

# I would expect this router to be exempt from the restriction, but it's also restricted.
api.add_router('/second', second_router, auth=None)

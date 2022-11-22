from django.urls import path

import myapp.routings
from myapp import consumers
from channels.routing import URLRouter
websocket_urlpatterns ={
    path("websocket/", URLRouter(myapp.routings.websocket_urlpatterns)),
}
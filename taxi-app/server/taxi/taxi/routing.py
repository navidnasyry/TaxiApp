
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from trips.consumers import TaxiConsumer



application = ProtocolTypeRouter({
    'websocket':URLRouter([
        path('taxi/', TaxiConsumer),
    ]),


})

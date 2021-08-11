
from channels.testing import WebsocketCommunicator
from django.http import response
from channels.layers import get_channel_layer
import pytest 
from taxi.routing import application
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken


TEST_CHANNEL_LAYERS= {
    'derault':{
        'BACKEND' : 'channels.layers.InMemoryChannelLayer',
    }
}

@database_sync_to_async
def create_user(username, password):
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    access = AccessToken.for_user(user)
    return user, access



    
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'PAsswor0'
        )

        communicator = WebsocketCommunicator(
            application= application,
            path=f'/taxi/?token={access}'
        )
        connected , _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()
        
    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'PAsswor0'
        )
        communicator = WebsocketCommunicator(
            application = application,
            path=f'/taxi/?token={access}'
        )

        connected, _ = await communicator.connect()

        message = {
            'type' : 'echo.message',
            'data' : 'This is a test message...'
        }

        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    
    async def test_can_send_and_receive_broadcast_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'PAsswor0'
        )

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('test', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect() 

    async def test_cannot_connect_to_socket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'PAsswor0'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()
        assert connected is False


    

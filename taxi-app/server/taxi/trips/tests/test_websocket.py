
from channels.testing import WebsocketCommunicator

import pytest 
from taxi.routing import application



TEST_CHANNEL_LAYERS= {
    'derault':{
        'BACKEND' : 'channels.layers.InMemoryChannelLayer',
    }
}


@pytest.mark.asyncio
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application= application,
            path='/taxi/'
        )
        connected , _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()
        



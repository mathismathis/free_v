import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"room_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        print(f"WebSocket connected for user: {self.channel_name}")

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print(f"WebSocket disconnected for user: {self.channel_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'offer':
            offer_data = data.get('offer')
            if should_handle_offer(offer_data):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'forward_offer',
                        'offer': offer_data,
                    }
                )
        elif message_type == 'answer':
            answer_data = data.get('answer')
            if should_handle_answer(answer_data):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'forward_answer',
                        'answer': answer_data,
                    }
                )
        elif message_type == 'candidate':
            candidate_data = data.get('candidate')
            if should_handle_candidate(candidate_data):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'forward_candidate',
                        'candidate': candidate_data,
                    }
                )

        print(f"Received message from user {self.channel_name}: {text_data}")

    async def forward_offer(self, event):
        offer_data = event['offer']

        # Forward the offer message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'offer',
            'offer': offer_data,
        }))

    async def forward_answer(self, event):
        answer_data = event['answer']

        # Forward the answer message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'answer',
            'answer': answer_data,
        }))

    async def forward_candidate(self, event):
        candidate_data = event['candidate']

        # Forward the candidate message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'candidate',
            'candidate': candidate_data,
        }))

# Define your custom conditional checks here

def should_handle_offer(offer_data):
    # Implement your logic to determine whether to handle the offer
    # Return True if the offer should be handled, or False otherwise
    return True

def should_handle_answer(answer_data):
    # Implement your logic to determine whether to handle the answer
    # Return True if the answer should be handled, or False otherwise
    return True

def should_handle_candidate(candidate_data):
    # Implement your logic to determine whether to handle the candidate
    # Return True if the candidate should be handled, or False otherwise
    return True

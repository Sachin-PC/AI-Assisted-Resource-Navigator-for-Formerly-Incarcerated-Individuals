import unittest
from src.ai_arnfi.services.user_chat_service import UserChatService

class TestChatService(unittest.TestCase):
    def setUp(self):
        self.userChatService = UserChatService()

    def test_get_response(self):
        user_query = "What are legal documents?"
        user_id = 1
        chat_session_id = 1
        response = self.userChatService.get_response(user_query, user_id, user_id, chat_session_id)
        print("response =",response)

        self.assertIsInstance(response['response'], str)
        
    
        
    
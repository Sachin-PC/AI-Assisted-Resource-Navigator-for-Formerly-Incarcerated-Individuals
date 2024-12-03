import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_user_chat_endpoint():
    user_query = "How does Legal Documents help for formerly incarcerated people"
    user_id = 1
    chat_session_id = 1
    params = {"user_query": user_query,
              "chat_session_id": chat_session_id
              }
    
    query_response = client.post("api/get_response", json=params)
    print("\n\nQUERY RESOPNSE \n\n")
    print(query_response)
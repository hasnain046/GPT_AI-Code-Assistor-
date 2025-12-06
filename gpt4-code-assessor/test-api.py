import requests
from config import RAPIDAPI_KEY, RAPIDAPI_HOST, RAPIDAPI_URL

def test_gpt4_api():
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': RAPIDAPI_HOST,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'messages': [
            {
                'role': 'user',
                'content': 'Hello, can you help me fix Python code?'
            }
        ],
        'max_tokens': 100
    }
    
    try:
        response = requests.post(RAPIDAPI_URL, headers=headers, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing RapidAPI GPT-4 connection...")
    success = test_gpt4_api()
    print(f"API Test: {'SUCCESS' if success else 'FAILED'}")
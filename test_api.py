import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables for API key
load_dotenv()
API_KEY = os.getenv("API_KEY", "your_secret_api_key_here")

def test_translation_api():
    """Test the translation API endpoint."""
    base_url = "http://localhost:8000"
    
    # Set up headers with API key
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    # Test Maranao to English translation
    maranao_to_english = {
        "source_lang": "MARANAO",
        "target_lang": "ENGLISH",
        "source_text": "Anda ka song?"
    }
    
    # Test English to Maranao translation
    english_to_maranao = {
        "source_lang": "ENGLISH",
        "target_lang": "MARANAO",
        "source_text": "Where are you going?"
    }
    
    # Test invalid language combination
    invalid_combination = {
        "source_lang": "MARANAO",
        "target_lang": "MARANAO",
        "source_text": "Anda ka song?"
    }
    
    # Test missing API key
    missing_api_key_test = {
        "source_lang": "MARANAO",
        "target_lang": "ENGLISH",
        "source_text": "Anda ka song?"
    }
    
    print("Testing Maranao to English translation...")
    try:
        response = requests.post(f"{base_url}/translate", json=maranao_to_english, headers=headers)
        print(f"Status code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTesting English to Maranao translation...")
    try:
        response = requests.post(f"{base_url}/translate", json=english_to_maranao, headers=headers)
        print(f"Status code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTesting invalid language combination...")
    try:
        response = requests.post(f"{base_url}/translate", json=invalid_combination, headers=headers)
        print(f"Status code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
        
    print("\nTesting missing API key (should return 401)...")
    try:
        response = requests.post(f"{base_url}/translate", json=missing_api_key_test)
        print(f"Status code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
        
    print("\nTesting invalid API key (should return 403)...")
    invalid_headers = {
        "Content-Type": "application/json",
        "X-API-Key": "invalid_key"
    }
    try:
        response = requests.post(f"{base_url}/translate", json=maranao_to_english, headers=invalid_headers)
        print(f"Status code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_translation_api() 
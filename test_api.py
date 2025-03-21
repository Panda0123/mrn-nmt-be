import requests
import json

def test_translation_api():
    """Test the translation API endpoint."""
    base_url = "http://localhost:8000"
    
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
    
    print("Testing Maranao to English translation...")
    try:
        response = requests.post(f"{base_url}/translate", json=maranao_to_english)
        print(f"Status code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTesting English to Maranao translation...")
    try:
        response = requests.post(f"{base_url}/translate", json=english_to_maranao)
        print(f"Status code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTesting invalid language combination...")
    try:
        response = requests.post(f"{base_url}/translate", json=invalid_combination)
        print(f"Status code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_translation_api() 
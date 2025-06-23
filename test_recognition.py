#!/usr/bin/env python3
"""
Test script to verify the recognition endpoint format
"""

import requests
import os

BASE_URL = "http://localhost:8000"

def test_recognition_format():
    """Test what parameter name the recognition endpoint expects"""
    print("🔍 Testing recognition endpoint parameter names...")
    
    # Test 1: Try with 'image' parameter
    print("\n1. Testing with 'image' parameter:")
    try:
        files = {'image': ('test.jpg', b'fake_image_data', 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/recognize/", files=files)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Try with 'face_image' parameter
    print("\n2. Testing with 'face_image' parameter:")
    try:
        files = {'face_image': ('test.jpg', b'fake_image_data', 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/recognize/", files=files)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Try with 'photo' parameter
    print("\n3. Testing with 'photo' parameter:")
    try:
        files = {'photo': ('test.jpg', b'fake_image_data', 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/recognize/", files=files)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_recognition_format() 
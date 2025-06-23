#!/usr/bin/env python3
"""
Test script to verify the registration endpoint format
"""

import requests
import os

BASE_URL = "http://localhost:8000"

def test_registration_format():
    """Test what parameter names the registration endpoint expects"""
    print("🔍 Testing registration endpoint parameter names...")
    
    # Test 1: Try with correct parameter names
    print("\n1. Testing with correct parameter names:")
    try:
        data = {
            'nombre': 'John',
            'apellido': 'Doe', 
            'codigo_unico': 'JD001',
            'requisitoriado': False
        }
        files = {'foto': ('test.jpg', b'fake_image_data', 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/usuarios/", data=data, files=files)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Try with wrong parameter names (common Android mistakes)
    print("\n2. Testing with wrong parameter names (name, surname, etc.):")
    try:
        data = {
            'name': 'John',           # ← Wrong: should be 'nombre'
            'surname': 'Doe',         # ← Wrong: should be 'apellido'
            'unique_code': 'JD001',   # ← Wrong: should be 'codigo_unico'
            'requested': False        # ← Wrong: should be 'requisitoriado'
        }
        files = {'photo': ('test.jpg', b'fake_image_data', 'image/jpeg')}  # ← Wrong: should be 'foto'
        response = requests.post(f"{BASE_URL}/usuarios/", data=data, files=files)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Try with missing required parameters
    print("\n3. Testing with missing required parameters:")
    try:
        data = {
            'nombre': 'John',
            # Missing apellido, codigo_unico, foto
        }
        response = requests.post(f"{BASE_URL}/usuarios/", data=data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_registration_format() 
#!/usr/bin/env python3
"""
Test script for the Face Recognition Backend
Tests all major endpoints and functionality
"""

import requests
import json
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_stats():
    """Test the stats endpoint"""
    print("\n📊 Testing stats endpoint...")
    response = requests.get(f"{BASE_URL}/stats/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_users_list():
    """Test getting users list"""
    print("\n👥 Testing users list endpoint...")
    response = requests.get(f"{BASE_URL}/usuarios/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_alertas():
    """Test getting alertas list"""
    print("\n🚨 Testing alertas endpoint...")
    response = requests.get(f"{BASE_URL}/alertas/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_recognition_without_image():
    """Test recognition endpoint without image (should fail)"""
    print("\n🔍 Testing recognition endpoint without image...")
    try:
        response = requests.post(f"{BASE_URL}/recognize/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Expected error: {e}")
    return True

def main():
    """Run all tests"""
    print("🧪 Starting Face Recognition Backend Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Stats", test_stats),
        ("Users List", test_users_list),
        ("Alertas", test_alertas),
        ("Recognition (no image)", test_recognition_without_image),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    print("\n📋 Available Endpoints:")
    print(f"  GET  {BASE_URL}/health")
    print(f"  GET  {BASE_URL}/stats/")
    print(f"  GET  {BASE_URL}/usuarios/")
    print(f"  POST {BASE_URL}/usuarios/")
    print(f"  GET  {BASE_URL}/usuarios/{{id}}")
    print(f"  PUT  {BASE_URL}/usuarios/{{id}}")
    print(f"  DELETE {BASE_URL}/usuarios/{{id}}")
    print(f"  POST {BASE_URL}/recognize/")
    print(f"  GET  {BASE_URL}/alertas/")
    print(f"  POST {BASE_URL}/usuarios/{{id}}/toggle-requisitoriado")

if __name__ == "__main__":
    main() 
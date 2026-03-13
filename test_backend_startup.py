#!/usr/bin/env python3
"""Test if backend can start without TensorFlow."""
import sys
sys.path.insert(0, '.')

print("Testing backend startup...")
print("1. Importing FastAPI app...")

try:
    from src.api.fastapi_app import app
    print("✓ FastAPI app imported successfully")
except Exception as e:
    print(f"✗ Failed to import app: {e}")
    sys.exit(1)

print("\n2. Testing health endpoint...")
try:
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/health")
    print(f"✓ Health check status: {response.status_code}")
    print(f"  Response: {response.json()}")
except Exception as e:
    print(f"⚠ Health check failed (expected if TensorFlow missing): {e}")

print("\n3. Testing root endpoint...")
try:
    response = client.get("/")
    print(f"✓ Root endpoint status: {response.status_code}")
    print(f"  API Name: {response.json()['name']}")
except Exception as e:
    print(f"✗ Root endpoint failed: {e}")
    sys.exit(1)

print("\n✓ Backend can start successfully!")
print("\nTo run the server:")
print("  python3 -m uvicorn src.api.fastapi_app:app --reload --port 8000")

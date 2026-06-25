import os
import sys
from io import BytesIO
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app
from config.database import SessionLocal
from models.auth import User
from utilities.security import get_current_user

# Dependency override to bypass authentication
def override_get_current_user():
    db = SessionLocal()
    user = db.query(User).first()
    db.close()
    if not user:
        # Create a dummy user if none exists
        user = User(id=1, email="test@example.com", is_active=True, roles=[])
    return user

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_upload():
    # We need a recipe and a step to test this. 
    # For now, let's just test that the endpoint receives the file and processes it.
    # To truly verify, we'll try uploading to a random step and catch the expected 404 (or upload to an existing one if available)
    
    # Let's see if we get a 404 meaning the endpoint is properly hit and parsed
    # We create a dummy image in memory
    dummy_image = BytesIO(b"fake_image_data")
    dummy_image.name = "test_image.jpg"
    
    print("Testing POST /api/v1/recipes/1/steps/1/image ...")
    response = client.post(
        "/api/v1/recipes/1/steps/1/image",
        files={"file": ("test_image.jpg", dummy_image, "image/jpeg")}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code in [200, 404]:
        print("Endpoint is functioning and reachable! (404 means recipe/step wasn't found, 200 means success)")
    else:
        print("Something went wrong.")

if __name__ == "__main__":
    test_upload()

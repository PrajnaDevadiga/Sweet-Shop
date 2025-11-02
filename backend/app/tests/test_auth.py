import pytest
from fastapi import status
from sqlalchemy.orm import Session


class TestUserRegistration:
    """Test user registration endpoint"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "hashed_password" not in data
        assert data["is_admin"] is False
    
    def test_register_duplicate_username(self, client, test_user):
        """Test registration with duplicate username"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "different@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "differentuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "invalid-email",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserLogin:
    """Test user login endpoint"""
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "testuser",
                "password": "testpassword"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_token_validity(self, client, test_user):
        """Test that token can be used to access protected endpoints"""
        # Login first
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "testuser",
                "password": "testpassword"
            }
        )
        token = login_response.json()["access_token"]
        
        # Use token to access protected endpoint
        response = client.get(
            "/api/sweets",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        response = client.get(
            "/api/sweets",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_no_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/sweets")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


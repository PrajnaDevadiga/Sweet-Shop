import pytest
from fastapi import status


class TestPurchaseSweet:
    """Test purchasing sweets"""
    
    def test_purchase_success(self, client, test_user, test_admin):
        """Test successful purchase"""
        # Create sweet as admin
        admin_login = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        admin_token = admin_login.json()["access_token"]
        
        create_response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        sweet_id = create_response.json()["id"]
        
        # Purchase as regular user
        user_login = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        user_token = user_login.json()["access_token"]
        
        response = client.post(
            f"/api/sweets/{sweet_id}/purchase",
            json={"quantity": 5},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == 45
    
    def test_purchase_multiple_quantities(self, client, test_user, test_admin):
        """Test purchasing multiple quantities"""
        admin_login = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        admin_token = admin_login.json()["access_token"]
        
        create_response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        sweet_id = create_response.json()["id"]
        
        user_login = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        user_token = user_login.json()["access_token"]
        
        # Purchase 10 items
        response = client.post(
            f"/api/sweets/{sweet_id}/purchase",
            json={"quantity": 10},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["quantity"] == 40
    
    def test_purchase_insufficient_quantity(self, client, test_user, test_admin):
        """Test purchasing when quantity is insufficient"""
        admin_login = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        admin_token = admin_login.json()["access_token"]
        
        create_response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 5
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        sweet_id = create_response.json()["id"]
        
        user_login = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        user_token = user_login.json()["access_token"]
        
        response = client.post(
            f"/api/sweets/{sweet_id}/purchase",
            json={"quantity": 10},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient quantity" in response.json()["detail"]
    
    def test_purchase_zero_quantity(self, client, test_user, test_admin):
        """Test purchasing with zero or negative quantity"""
        admin_login = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        admin_token = admin_login.json()["access_token"]
        
        create_response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        sweet_id = create_response.json()["id"]
        
        user_login = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        user_token = user_login.json()["access_token"]
        
        response = client.post(
            f"/api/sweets/{sweet_id}/purchase",
            json={"quantity": 0},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_purchase_nonexistent_sweet(self, client, test_user):
        """Test purchasing non-existent sweet"""
        user_login = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        user_token = user_login.json()["access_token"]
        
        response = client.post(
            "/api/sweets/999/purchase",
            json={"quantity": 5},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestRestockSweet:
    """Test restocking sweets"""
    
    def test_restock_success(self, client, test_admin):
        """Test admin can restock a sweet"""
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        # Create sweet
        create_response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        sweet_id = create_response.json()["id"]
        
        # Restock sweet
        response = client.post(
            f"/api/sweets/{sweet_id}/restock",
            json={"quantity": 30},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == 80
    
    def test_restock_as_regular_user(self, client, test_user, test_admin):
        """Test regular user cannot restock"""
        # Create sweet as admin
        admin_login = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        admin_token = admin_login.json()["access_token"]
        
        create_response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        sweet_id = create_response.json()["id"]
        
        # Try to restock as regular user
        user_login = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        user_token = user_login.json()["access_token"]
        
        response = client.post(
            f"/api/sweets/{sweet_id}/restock",
            json={"quantity": 30},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_restock_zero_quantity(self, client, test_admin):
        """Test restocking with zero or negative quantity"""
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        create_response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        sweet_id = create_response.json()["id"]
        
        response = client.post(
            f"/api/sweets/{sweet_id}/restock",
            json={"quantity": 0},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_restock_nonexistent_sweet(self, client, test_admin):
        """Test restocking non-existent sweet"""
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/sweets/999/restock",
            json={"quantity": 30},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


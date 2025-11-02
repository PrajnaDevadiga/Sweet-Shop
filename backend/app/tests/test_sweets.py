import pytest
from fastapi import status


class TestCreateSweet:
    """Test creating sweets"""
    
    def test_create_sweet_as_admin(self, client, test_admin):
        """Test admin can create a sweet"""
        # Login as admin
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        # Create sweet
        response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Chocolate Bar"
        assert data["category"] == "Chocolate"
        assert data["price"] == 5.99
        assert data["quantity"] == 50
        assert "id" in data
    
    def test_create_sweet_as_regular_user(self, client, test_user):
        """Test regular user cannot create sweets"""
        # Login as regular user
        login_response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        token = login_response.json()["access_token"]
        
        # Try to create sweet
        response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_duplicate_sweet(self, client, test_admin):
        """Test cannot create sweet with duplicate name"""
        # Login as admin
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        # Create first sweet
        client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Try to create duplicate
        response = client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Candy",
                "price": 4.99,
                "quantity": 30
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestListSweets:
    """Test listing sweets"""
    
    def test_list_sweets_empty(self, client, test_user):
        """Test listing sweets when none exist"""
        login_response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        token = login_response.json()["access_token"]
        
        response = client.get(
            "/api/sweets",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_list_sweets_with_data(self, client, test_admin):
        """Test listing sweets with data"""
        # Login as admin
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        # Create sweets
        client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            "/api/sweets",
            json={
                "name": "Gummy Bears",
                "category": "Gummies",
                "price": 3.99,
                "quantity": 100
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # List sweets
        response = client.get(
            "/api/sweets",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2


class TestSearchSweets:
    """Test searching sweets"""
    
    def test_search_by_name(self, client, test_admin):
        """Test searching sweets by name"""
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        # Create sweets
        client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            "/api/sweets",
            json={
                "name": "Gummy Bears",
                "category": "Gummies",
                "price": 3.99,
                "quantity": 100
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Search by name
        response = client.get(
            "/api/sweets/search?name=Chocolate",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Chocolate Bar"
    
    def test_search_by_category(self, client, test_admin):
        """Test searching sweets by category"""
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        # Create sweets
        client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            "/api/sweets",
            json={
                "name": "Gummy Bears",
                "category": "Gummies",
                "price": 3.99,
                "quantity": 100
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Search by category
        response = client.get(
            "/api/sweets/search?category=Gummies",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Gummies"
    
    def test_search_by_price_range(self, client, test_admin):
        """Test searching sweets by price range"""
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        # Create sweets
        client.post(
            "/api/sweets",
            json={
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 5.99,
                "quantity": 50
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            "/api/sweets",
            json={
                "name": "Gummy Bears",
                "category": "Gummies",
                "price": 3.99,
                "quantity": 100
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Search by price range
        response = client.get(
            "/api/sweets/search?min_price=4.0&max_price=6.0",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Chocolate Bar"


class TestUpdateSweet:
    """Test updating sweets"""
    
    def test_update_sweet_as_admin(self, client, test_admin):
        """Test admin can update a sweet"""
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
        
        # Update sweet
        response = client.put(
            f"/api/sweets/{sweet_id}",
            json={
                "price": 6.99,
                "quantity": 60
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["price"] == 6.99
        assert data["quantity"] == 60
        assert data["name"] == "Chocolate Bar"  # Unchanged
    
    def test_update_sweet_as_regular_user(self, client, test_user, test_admin):
        """Test regular user cannot update sweets"""
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
        
        # Try to update as regular user
        user_login = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        user_token = user_login.json()["access_token"]
        
        response = client.put(
            f"/api/sweets/{sweet_id}",
            json={"price": 6.99},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_nonexistent_sweet(self, client, test_admin):
        """Test updating non-existent sweet"""
        login_response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "adminpassword"}
        )
        token = login_response.json()["access_token"]
        
        response = client.put(
            "/api/sweets/999",
            json={"price": 6.99},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteSweet:
    """Test deleting sweets"""
    
    def test_delete_sweet_as_admin(self, client, test_admin):
        """Test admin can delete a sweet"""
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
        
        # Delete sweet
        response = client.delete(
            f"/api/sweets/{sweet_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify deleted
        get_response = client.get(
            f"/api/sweets/{sweet_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_sweet_as_regular_user(self, client, test_user, test_admin):
        """Test regular user cannot delete sweets"""
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
        
        # Try to delete as regular user
        user_login = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        user_token = user_login.json()["access_token"]
        
        response = client.delete(
            f"/api/sweets/{sweet_id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


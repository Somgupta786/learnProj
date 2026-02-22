import requests
from config import API_URL
from typing import Optional, Dict, List

class APIClient:
    def __init__(self):
        self.base_url = API_URL
        self.token = None

    def set_token(self, token: str):
        """Set JWT token for authenticated requests"""
        self.token = token

    def _get_headers(self, include_auth: bool = False) -> Dict:
        """Get request headers"""
        headers = {"Content-Type": "application/json"}
        if include_auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    # Auth endpoints
    def register(self, name: str, email: str, password: str, phone: str = None) -> Dict:
        """Register new user"""
        data = {"name": name, "email": email, "password": password, "phone": phone}
        response = requests.post(f"{self.base_url}/auth/register", json=data)
        return response.json()

    def login(self, email: str, password: str) -> Dict:
        """Login user"""
        data = {"email": email, "password": password}
        response = requests.post(f"{self.base_url}/auth/login", json=data)
        return response.json()

    # Product endpoints
    def get_products(self, page: int = 1, limit: int = 10, category: str = None) -> Dict:
        """Get all products"""
        params = {"page": page, "limit": limit}
        if category:
            params["category"] = category
        response = requests.get(f"{self.base_url}/products", params=params)
        return response.json()

    def search_products(self, query: str, page: int = 1, limit: int = 10) -> Dict:
        """Search products"""
        params = {"q": query, "page": page, "limit": limit}
        response = requests.get(f"{self.base_url}/products/search", params=params)
        return response.json()

    def get_product(self, product_id: int) -> Dict:
        """Get single product"""
        response = requests.get(f"{self.base_url}/products/{product_id}")
        return response.json()

    def create_product(self, product_data: Dict) -> Dict:
        """Create product (admin only)"""
        response = requests.post(
            f"{self.base_url}/products",
            json=product_data,
            headers=self._get_headers(include_auth=True)
        )
        return response.json()

    def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Update product (admin only)"""
        response = requests.put(
            f"{self.base_url}/products/{product_id}",
            json=product_data,
            headers=self._get_headers(include_auth=True)
        )
        return response.json()

    def delete_product(self, product_id: int) -> Dict:
        """Delete product (admin only)"""
        response = requests.delete(
            f"{self.base_url}/products/{product_id}",
            headers=self._get_headers(include_auth=True)
        )
        return response.json()

    # Order endpoints
    def create_order(self, order_data: Dict) -> Dict:
        """Create order"""
        response = requests.post(
            f"{self.base_url}/orders",
            json=order_data,
            headers=self._get_headers(include_auth=True)
        )
        return response.json()

    def get_user_orders(self, page: int = 1, limit: int = 10) -> Dict:
        """Get user's orders"""
        params = {"page": page, "limit": limit}
        response = requests.get(
            f"{self.base_url}/orders",
            params=params,
            headers=self._get_headers(include_auth=True)
        )
        return response.json()

    def get_order(self, order_id: int) -> Dict:
        """Get single order"""
        response = requests.get(
            f"{self.base_url}/orders/{order_id}",
            headers=self._get_headers(include_auth=True)
        )
        return response.json()

    def get_all_orders(self, page: int = 1, limit: int = 10) -> Dict:
        """Get all orders (admin only)"""
        params = {"page": page, "limit": limit}
        response = requests.get(
            f"{self.base_url}/orders/admin/all",
            params=params,
            headers=self._get_headers(include_auth=True)
        )
        return response.json()

    def update_order_status(self, order_id: int, status: str) -> Dict:
        """Update order status (admin only)"""
        data = {"status": status}
        response = requests.put(
            f"{self.base_url}/orders/{order_id}/status",
            json=data,
            headers=self._get_headers(include_auth=True)
        )
        return response.json()

# Create global API client instance
api_client = APIClient()

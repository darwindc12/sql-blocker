import requests


class AuthService:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.access_token = None
        self.refresh_token = None
        self.user = None

    # --------------------------------------------------------
    # Login
    # --------------------------------------------------------
    def login(self, username, password):
        try:
            response = requests.post(
                f"http://localhost:8000/api/auth/login/",
                json={
                    "username": username,
                    "password": password
                },
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()

                self.access_token = data.get("access")
                self.refresh_token = data.get("refresh")

                self.user = self.get_user_info()

                return True, "Login successful"

            return False, response.json().get("detail", "Invalid credentials")

        except Exception as e:
            return False, f"Connection error: {e}"

    # --------------------------------------------------------
    # Get User Info
    # --------------------------------------------------------
    def get_user_info(self):
        try:
            response = requests.get(
                f"http://localhost:8000/api/auth/me/",
                headers={
                    "Authorization": f"Bearer {self.access_token}"
                },
                timeout=5
            )

            if response.status_code == 200:
                return response.json()

        except Exception:
            pass

        return None

    # --------------------------------------------------------
    # Role Helpers
    # --------------------------------------------------------

    def get_role(self):
        if not self.user:
            return None
        return self.user.get("role")

    def is_admin(self):
        role = self.get_role()
        return role in ["admin", "super_admin"]

    def is_user(self):
        return self.get_role() == "user"

    def is_service(self):
        return self.get_role() == "service"

    # --------------------------------------------------------
    # Token Refresh (optional)
    # --------------------------------------------------------
    def refresh(self):
        if not self.refresh_token:
            return False

        try:
            response = requests.post(
                f"http://localhost:8000/api/auth/refresh/",
                json={"refresh": self.refresh_token},
                timeout=5
            )

            if response.status_code == 200:
                self.access_token = response.json().get("access")
                return True

        except Exception:
            pass

        return False
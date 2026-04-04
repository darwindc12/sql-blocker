import requests


class AuthService:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.user = None

    def login(self, username, password):
        try:
            response = requests.post(
                f"{self.base_url}/api/token/",
                json={
                    "username": username,
                    "password": password
                },
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access")

                # Optional: decode or fetch user info
                self.user = self.get_user_info()

                return True, "Login successful"

            return False, "Invalid credentials"

        except Exception as e:
            return False, f"Error: {e}"

    def get_user_info(self):
        try:
            response = requests.get(
                f"{self.base_url}/api/user/",
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=5
            )

            if response.status_code == 200:
                return response.json()

        except Exception:
            pass

        return None

    def is_admin(self):
        if self.user:
            return self.user.get("is_staff") or self.user.get("role") == "admin"
        return False
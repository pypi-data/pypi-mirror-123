import os

class Settings:
    BASE_URL = os.environ.get('API_BASE_URL', 'https://api.international-design.pro')
    SANDBOX_BASE_URL = os.environ.get('API_SANDBOX_BASE_URL', 'https://api-sandbox.international-design.pro')

settings = Settings()
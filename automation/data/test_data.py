import random
import string

class TestData:
    @staticmethod
    def get_valid_patient():
        return {"email": "patient@smile.com", "password": "password123"}

    @staticmethod
    def get_valid_doctor():
        return {"email": "doc@smile.com", "password": "docpassword", "doctor_id": "1234"}

    @staticmethod
    def generate_random_email():
        chars = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"user_{chars}@example.com"

    @staticmethod
    def generate_random_string(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

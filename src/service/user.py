from datetime import datetime, timedelta
import os
import time
import bcrypt
import random
from jose import jwt


class UserService:
    encoding: str = "utf-8"

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(password.encode(self.encoding), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(self.encoding), hashed_password.encode(self.encoding))

    def create_token(self, user_id: int) -> str:
        return jwt.encode(
            {
                "sub": str(user_id), 
                "exp": datetime.now() + timedelta(days=1)
            }, 
            key=os.getenv("JWT_SECRET_KEY"), 
            algorithm=os.getenv("JWT_ALGORITHM")
        )
    
    def decode_token(self, token: str) -> int:
        payload: dict = jwt.decode(token, key=os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
        return int(payload["sub"])
    
    @staticmethod
    def create_opt() -> int:
        return random.randint(1000, 9999)

    @staticmethod
    def send_email_to_user(email: str) -> None:
        time.sleep(10)
        print(f"Sending email to {email}")

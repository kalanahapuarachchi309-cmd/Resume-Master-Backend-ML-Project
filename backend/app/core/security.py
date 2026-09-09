"""Security, Hashing, and JWT Authentication Subsystem (Kalana)."""
import os
import hmac
import hashlib

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    _has_passlib = True
except Exception:
    _has_passlib = False


def get_password_hash(password: str) -> str:
    """Generate secure salted password hash with pbkdf2 fallback."""
    if _has_passlib:
        try:
            return pwd_context.hash(password)
        except Exception:
            pass
    salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return f"pbkdf2:{salt}:{hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify raw password against stored hash."""
    if hashed_password.startswith("pbkdf2:"):
        parts = hashed_password.split(":")
        if len(parts) == 3:
            salt = parts[1]
            stored_hash = parts[2]
            computed = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
            return hmac.compare_digest(stored_hash, computed)
    if _has_passlib:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            pass
    return False

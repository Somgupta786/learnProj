import re
from email_validator import validate_email, EmailNotValidError

def validate_user_email(email: str) -> bool:
    """Validate email format"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_password(password: str) -> bool:
    """Validate password (min 6 characters)"""
    return len(password) >= 6

def validate_phone(phone: str) -> bool:
    """Validate phone number"""
    phone_regex = r"^[0-9]{10,15}$"
    digits_only = re.sub(r"\D", "", phone)
    return bool(re.match(phone_regex, digits_only))

def validate_price(price: float) -> bool:
    """Validate price is positive"""
    try:
        return float(price) > 0
    except (ValueError, TypeError):
        return False

def validate_stock(stock: int) -> bool:
    """Validate stock is non-negative integer"""
    try:
        return isinstance(int(stock), int) and int(stock) >= 0
    except (ValueError, TypeError):
        return False

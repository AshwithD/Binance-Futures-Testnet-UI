VALID_SIDES = ["BUY", "SELL"]
VALID_TYPES = ["MARKET", "LIMIT"]

def validate_symbol(symbol: str):
    if not symbol.isalnum():
        raise ValueError("Symbol must be alphanumeric")
    
def validate_side(side: str):
    if side.upper() not in VALID_SIDES:
        raise ValueError("side must be BUY or SELL")
    
def validate_order_type(order_type: str):
    if order_type.upper() not in VALID_TYPES:
        raise ValueError("Order type must be MARKET or LIMIT")
    
def validate_quantity(qty: float):
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")
    
def validate_price(price: float):
    if price <= 0:
        raise ValueError("Price must be greater than 0")

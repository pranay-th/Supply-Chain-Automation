# Regex patterns & extraction functions
import re
from datetime import datetime

ORDER_ID_PATTERN=r"\bORD\d+\b"
SHIPMENT_ID_PATTERN=r"\bSHP\d+\b"
DELIVERY_DATE_PATTERN=r"\b\d{4}-\d{2}-\d{2}\b"

def extract_shipment_fields(message:str) -> dict:
    order_match = re.search(ORDER_ID_PATTERN,message)
    shipment_match = re.search(SHIPMENT_ID_PATTERN,message)
    date_match = re.search(DELIVERY_DATE_PATTERN,message)

    if order_match:
        order_id=order_match.group(0)
    else:
        order_id=None
    
    if shipment_match:
        shipment_id=shipment_match.group(0)
    else:
        shipment_id=None
    
    if date_match:
        try:
            datetime.strptime(date_match.group(0), "%Y-%m-%d")
            delivery_date = date_match.group(0)
        except ValueError:
            delivery_date = None
    else:
        delivery_date = None
    
    return {
        "order_id":order_id,
        "shipment_id":shipment_id,
        "delivery_date":delivery_date
    }
    

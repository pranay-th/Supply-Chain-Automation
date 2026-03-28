# Defines shipment JSON schema
def build_shipment_payload(
    order_id: str,
    shipment_id: str,
    delivery_date: str,
    raw_message: str
) -> dict:
    return {
        "order_id": order_id,
        "shipment_id": shipment_id,
        "delivery_date": delivery_date,
        "raw_message": raw_message,
    }
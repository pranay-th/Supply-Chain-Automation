# Handles forwarding data via requests
import requests
from config.settings import CENTRAL_TRACKING_URL, FORWARD_TIMEOUT_SECONDS

def forward_shipment_data(payload: dict) -> dict:
    try:
        response = requests.post(
            CENTRAL_TRACKING_URL,
            json=payload,
            timeout=FORWARD_TIMEOUT_SECONDS
        )
        return {
            "forwarded":True,
            "status_code":response.status_code,
            "error":None
        }

    except requests.RequestException as exc:
        return {
            "forwarded":False,
            "status_code":None,
            "error":str(exc)
        }
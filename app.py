# Entry point for Flask app
from flask import Flask
from routes.shipment_routes import shipment_bp

app = Flask(__name__)
app.register_blueprint(shipment_bp)

@app.route("/")
def health():
    return {"status": "ok", "service": "supply_chain_service"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
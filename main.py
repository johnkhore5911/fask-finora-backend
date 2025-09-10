from flask import Flask, request, jsonify
import json
from datetime import datetime
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    return "Finora backend is running 🚀"

@app.route("/webhook/bitgo", methods=["POST"])
def bitgo_webhook():
    try:
        # Log raw request data for debugging
        raw_data = request.get_data(as_text=True)
        logger.info(f"Raw request data: {raw_data}")
        
        # Try to parse JSON
        try:
            data = request.get_json()
            if data is None:
                return jsonify({"error": "Invalid JSON or no JSON data"}), 400
        except Exception as json_error:
            logger.error(f"JSON parsing error: {json_error}")
            return jsonify({"error": "Invalid JSON format"}), 400

        # Log the successful webhook
        logger.info(f"\n=== Webhook Received at {datetime.now()} ===")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"JSON Data: {json.dumps(data, indent=2)}")
        logger.info("=== End of Webhook ===")
        
        # Process different webhook types
        webhook_type = data.get('type')
        state = data.get('state')
        
        if webhook_type == 'transfer' and state == 'confirmed':
            logger.info("💰 Deposit confirmed!")
            value = data.get('value', {})
            logger.info(f"Amount: {value.get('amount')}")
            logger.info(f"Currency: {value.get('currency')}")
            logger.info(f"Transaction ID: {data.get('hash')}")
            
        elif webhook_type == 'wallet_confirmation':
            logger.info("👛 Wallet confirmation received")
            
        elif webhook_type == 'block':
            logger.info("⛓ New block notification")
            
        else:
            logger.info(f"📨 Other webhook type: {webhook_type}")
        
        return jsonify({"status": "OK"}), 200
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(port=4000, debug=True)

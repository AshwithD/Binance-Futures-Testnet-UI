import os
from binance.client import Client
from dotenv import load_dotenv
from bot.logging_config import logger

# load_dotenv()
load_dotenv(dotenv_path=".env", override=True)


API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# TESTNET = True

# def get_binance_client():
#     try:
#         client = Client(API_KEY, API_SECRET, testnet=TESTNET)
#         logger.info("Connected to Binance Testnet API")
#         return client
    
#     except Exception as e:
#         logger.error(f"Failed to create Binance Client: {e}")
#         raise

import os
from binance.client import Client
from dotenv import load_dotenv

# Load .env locally (harmless on Streamlit Cloud)
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

def get_binance_client():
    if not API_KEY or not API_SECRET:
        raise RuntimeError("Binance API keys not found in environment variables")

    client = Client(API_KEY, API_SECRET, testnet=True)
    client.FUTURES_URL = "https://testnet.binancefuture.com"
    return client


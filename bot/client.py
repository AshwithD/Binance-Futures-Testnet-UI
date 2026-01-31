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

# Load .env for local development
load_dotenv()

def get_binance_client():
    """
    Returns a Binance Futures Testnet client.
    Works both locally (.env) and on Streamlit Cloud (st.secrets).
    """

    api_key = None
    api_secret = None

    try:
        import streamlit as st
        api_key = st.secrets.get("BINANCE_API_KEY")
        api_secret = st.secrets.get("BINANCE_API_SECRET")
    except Exception:
        pass  # Streamlit not available (local run)

    # 2️⃣ Fallback to environment variables (.env)
    if not api_key or not api_secret:
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

    # 3️⃣ Final validation
    if not api_key or not api_secret:
        raise RuntimeError(
            "Binance API keys not found. "
            "Set them in Streamlit Secrets or in a .env file."
        )

    client = Client(api_key, api_secret, testnet=True)
    client.FUTURES_URL = "https://testnet.binancefuture.com"
    return client


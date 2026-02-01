import os
from binance.client import Client
# from dotenv import load_dotenv

# Load .env for local development
# load_dotenv()

def get_binance_client():
    """
    Returns a Binance Futures Testnet client.
    Works both locally (.env) and on Streamlit Cloud (st.secrets).
    """

    # api_key = None
    # api_secret = None

    # 1️⃣ Try Streamlit secrets (Cloud)
    try:
        import streamlit as st
        api_key = st.secrets.get("BINANCE_API_KEY")
        api_secret = st.secrets.get("BINANCE_API_SECRET")
    except Exception:
        pass

    # 2️⃣ Fallback to environment variables (.env)
    # if not api_key or not api_secret:
    #     api_key = os.getenv("BINANCE_API_KEY")
    #     api_secret = os.getenv("BINANCE_API_SECRET")

    # 3️⃣ Final validation
    # if not api_key or not api_secret:
    #     raise RuntimeError(
    #         "Binance API keys not found. "
    #         "Set them in Streamlit Secrets or a .env file."
    #     )

    # 🚫 Disable ping (CRITICAL for Futures Testnet + Streamlit)
    client = Client(
        api_key,
        api_secret,
        testnet=True,
        ping=False
    )

    # Futures Testnet endpoint
    client.FUTURES_URL = "https://testnet.binancefuture.com"

    return client

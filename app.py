import streamlit as st
from binance.exceptions import BinanceAPIException

from bot.orders import (
    place_market_order,
    place_limit_order,
    set_leverage,
    get_futures_balance,
    get_mark_price,
    get_open_positions
)

# ---------------- Page Config ----------------
st.set_page_config(page_title="Trading Bot UI", layout="centered")

st.title("📈 Binance Futures Testnet Trading Bot")
st.write("Streamlit UI for placing Futures orders on Binance Testnet")

# ---------------- Inputs ----------------
symbol = st.selectbox("Symbol", ["BTCUSDT", "ETHUSDT"])
side = st.selectbox("Side", ["BUY", "SELL"])
order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])

quantity = st.number_input(
    "Quantity",
    min_value=0.001,
    step=0.001,
    value=0.003
)

leverage = st.slider(
    "Leverage (x)",
    min_value=1,
    max_value=20,
    value=10
)

# ---------------- Market Data ----------------
st.subheader("📊 Market Data")

mark_price = get_mark_price(symbol)

st.metric(
    label=f"{symbol} Mark Price",
    value=f"{mark_price:,.2f} USDT"
)

# ---------------- Margin Info ----------------
st.subheader("💰 Futures Margin (USDT)")

balance_info = get_futures_balance()

st.metric(
    label="Available Margin",
    value=f"{balance_info['available']:.2f} USDT"
)

st.metric(
    label="Total Balance",
    value=f"{balance_info['balance']:.2f} USDT"
)

if balance_info["available"] < 50:
    st.warning("⚠️ Low available margin. Increase leverage or add testnet funds.")

# ---------------- Price Input (LIMIT only) ----------------
price = None
if order_type == "LIMIT":
    price = st.number_input(
        "Limit Price",
        min_value=1.0,
        step=100.0,
        value=mark_price + 1000 if side == "SELL" else max(mark_price - 1000, 1)
    )

# ---------------- Place Order ----------------
if st.button("🚀 Place Order"):
    try:
        # ---- Minimum notional check ----
        notional = quantity * mark_price
        if notional < 20:
            st.error(
                f"❌ Order notional too small: {notional:.2f} USDT "
                "(minimum is 20 USDT)"
            )
            st.stop()

        with st.spinner("Placing order..."):
            # Set leverage first
            set_leverage(symbol, leverage)

            # Place order
            if order_type == "MARKET":
                result = place_market_order(symbol, side, quantity)
            else:
                if price is None:
                    st.error("Price is required for LIMIT orders")
                    st.stop()
                result = place_limit_order(symbol, side, quantity, price)

        st.success(f"✅ Order placed successfully ({leverage}x leverage)")

        st.subheader("📄 Order Summary")
        st.json({
            "Order ID": result.get("orderId"),
            "Symbol": result.get("symbol"),
            "Side": side,
            "Order Type": order_type,
            "Leverage": f"{leverage}x",
            "Status": result.get("status"),
            "Executed Qty": result.get("executedQty"),
            "Avg Price": result.get("avgPrice", "N/A"),
        })

    except BinanceAPIException as e:
        if "Margin is insufficient" in str(e):
            st.error("❌ Insufficient margin. Increase leverage or add testnet USDT.")
        elif "notional" in str(e):
            st.error("❌ Order notional too small. Increase quantity.")
        else:
            st.error(f"Binance API Exception: {str(e)}")

    except ValueError as e:
        st.error(f"Invalid input: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

# ---------------- Open Positions ----------------
st.subheader("📌 Open Positions")

positions = get_open_positions()

if positions:
    st.table(positions)
else:
    st.info("No open positions")

from bot.client import get_binance_client
from bot.logging_config import logger
from bot.validators import validate_quantity, validate_price, validate_side
from binance.exceptions import BinanceAPIException


# ---------------- MARKET ORDER ----------------
def place_market_order(symbol, side, quantity):
    try:
        validate_side(side)
        validate_quantity(quantity)

        client = get_binance_client()

        logger.info(f"Placing MARKET {side} order: {symbol} {quantity}")

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        logger.info(f"Order successful: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Exception while placing market order: {str(e)}")
        raise


# ---------------- LIMIT ORDER ----------------
def place_limit_order(symbol, side, quantity, price):
    try:
        validate_side(side)
        validate_quantity(quantity)
        validate_price(price)

        client = get_binance_client()

        logger.info(f"Placing LIMIT {side} order: {symbol} {quantity} @ {price}")

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )

        logger.info(f"Order successful: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise


# ---------------- LEVERAGE ----------------
def set_leverage(symbol, leverage):
    try:
        client = get_binance_client()

        client.futures_change_leverage(
            symbol=symbol,
            leverage=leverage
        )

        logger.info(f"Leverage set to {leverage}x for {symbol}")

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception while setting leverage: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to set leverage: {str(e)}")
        raise


# ---------------- FUTURES BALANCE ----------------
def get_futures_balance():
    client = get_binance_client()

    balances = client.futures_account_balance()
    for asset in balances:
        if asset["asset"] == "USDT":
            return {
                "balance": float(asset["balance"]),
                "available": float(asset["availableBalance"])
            }

    return {"balance": 0.0, "available": 0.0}


# ---------------- MARK PRICE ----------------
def get_mark_price(symbol):
    client = get_binance_client()

    data = client.futures_mark_price(symbol=symbol)
    return float(data["markPrice"])


# ---------------- OPEN POSITIONS ----------------
def get_open_positions():
    client = get_binance_client()

    positions = client.futures_position_information()
    open_positions = []

    for pos in positions:
        amt = float(pos["positionAmt"])
        if amt != 0.0:
            open_positions.append({
                "Symbol": pos["symbol"],
                "Side": "LONG" if amt > 0 else "SHORT",
                "Position Amt": amt,
                "Entry Price": float(pos["entryPrice"]),
                "Mark Price": float(pos["markPrice"]),
                "Unrealized PnL": float(pos["unRealizedProfit"]),
                "Leverage": pos.get("leverage", "N/A")
            })

    return open_positions

from bot.client import get_binance_client
from bot.validators import (validate_quantity, validate_price, validate_side, validate_order_type)
from bot.logging_config import logger
from binance.exceptions import BinanceAPIException

client = get_binance_client()
# client.futures_change_leverage(symbol="BTCUSDT", leverage=10)


def place_market_order(symbol, side, quantity):
    try:
        validate_side(side)
        validate_quantity(quantity)

        logger.info(f"Placing MARKET {side} order: {symbol} {quantity}")
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        logger.info(f"Response: {response}")
        return response
    
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {e.message}")
        raise
    except Exception as e:
        logger.error(f"Exception while placing market order: {e}")
        raise


def place_limit_order(symbol, side, quantity, price):
    try:
        validate_side(side)
        validate_quantity(quantity)
        validate_price(price)

        logger.info(f"Placing LIMIT {side} {symbol} {quantity} @ {price}")
        response= client.futures_create_order(
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
        logger.error(f"Binance API error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

def set_leverage(symbol, leverage):
    try:
        client.futures_change_leverage(
            symbol=symbol,
            leverage=leverage
        )
        logger.info(f"Leverage set to {leverage}x for {symbol}")
    except Exception as e:
        logger.error(f"Failed to set leverage: {e}")
        raise


def get_futures_balance():
    """
    Fetches the USDT balance from the futures account.
    """
    balances = client.futures_account_balance()
    for asset in balances:
        if asset["asset"] == "USDT":
            return {
                "balance": float(asset["balance"]),
                "available": float(asset["availableBalance"])
            }
    return {"balance": 0.0, "available": 0.0}

def get_mark_price(symbol):
    """
    Fetch current mark price for a Futures symbol
    """
    data = client.futures_mark_price(symbol=symbol)
    return float(data["markPrice"])

def get_open_positions():
    """
    Fetch all open Futures positions (non-zero positionAmt)
    """
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

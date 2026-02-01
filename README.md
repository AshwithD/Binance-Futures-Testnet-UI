# 📈 Binance Futures Testnet Trading Dashboard

A Streamlit-based web application to place and manage **Binance USDT-M Futures Testnet** trades.
The app allows users to place MARKET and LIMIT orders, control leverage, view margin details,
check live mark prices, and monitor open positions — all in a simple UI.

🔗 **Live Demo**:  
https://binance-futures-testnet-ui.streamlit.app/

---

## 🚀 Features

- Place **MARKET** and **LIMIT** Futures orders
- **BUY / SELL** support
- Adjustable **Leverage (1x – 20x)**
- Live **Mark Price** display
- View **Available Margin** and **Total Balance**
- Monitor **Open Positions**
- Input validation and minimum notional checks
- Secure API key handling using Streamlit Secrets
- Uses **Binance Futures Testnet** (no real money)

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **python-binance**
- **Binance Futures Testnet API**

---

## 📦 Project Structure

```

Binance-Futures-Testnet-UI/
│
├── app.py
├── bot/
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
├── requirements.txt
├── .gitignore
└── README.md

````

---

## ⚙️ Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/AshwithD/Binance-Futures-Testnet-UI.git
cd Binance-Futures-Testnet-UI
````

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set environment variables

Create a `.env` file:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

> These must be **Binance Futures Testnet** API keys.

---

## ☁️ Deployment

The app is deployed using **Streamlit Cloud**.
API keys are securely stored using **Streamlit Secrets** 

---

## ⚠️ Disclaimer

This project is for **educational and demonstration purposes only**.

* Uses **Binance Futures Testnet**
* No real funds are involved
* Do **NOT** use real (mainnet) API keys

---

## 👤 Author

**Ashwith D**

````

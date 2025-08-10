pip install fastapi uvicorn yfinance matplotlib

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yfinance as yf
import matplotlib.pyplot as plt
import os

app = FastAPI(title="Stock Chart API")

# Allow any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CHART_FILE = "chart.png"

@app.get("/chart/{symbol}")
def get_stock_chart(symbol: str):
    symbol = symbol.upper().strip()
    try:
        data = yf.download(symbol, period="6mo", interval="1d")
        if data.empty:
            raise HTTPException(status_code=404, detail="No data found for symbol")

        plt.figure(figsize=(10,5))
        plt.plot(data.index, data['Close'], label="Close Price", color="blue")
        plt.title(f"{symbol} - Last 6 Months Daily Close")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(CHART_FILE)
        plt.close()

        return FileResponse(CHART_FILE, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chart: {e}")

import json
import asyncio
import websockets
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

# WebSocket: Indices
@app.websocket("/ws/indices")
async def indices_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Replace with your NSE indices fetch logic
            data = {"index": "NIFTY 50", "value": 19800.25}
            await websocket.send_json(data)
            await asyncio.sleep(2)  # send every 2 seconds
    except Exception as e:
        print("Indices WS disconnected:", e)
    finally:
        await websocket.close()

# WebSocket: Quotes for a symbol
@app.websocket("/ws/quotes/{symbol}")
async def quotes_ws(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            # Replace with your NSE symbol fetch logic
            data = {"symbol": symbol.upper(), "price": 2500.45}
            await websocket.send_json(data)
            await asyncio.sleep(2)  # send every 2 seconds
    except Exception as e:
        print(f"Quotes WS disconnected for {symbol}:", e)
    finally:
        await websocket.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

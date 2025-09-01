import asyncio
import json
from fastapi import FastAPI, WebSocket
import uvicorn
from jugaad_data.nse import NSELive

app = FastAPI()
nse = NSELive()


@app.websocket("/ws/indices")
async def ws_indices(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = nse.all_indices()
                await websocket.send_text(json.dumps(data, default=str))
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
            await asyncio.sleep(2)  # adjust refresh interval
    except Exception as e:
        print(f"🔌 Disconnected (indices): {e}")
    finally:
        await websocket.close()


@app.websocket("/ws/quotes/{symbol}")
async def ws_quotes(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            try:
                data = nse.stock_quote(symbol)
                await websocket.send_text(json.dumps(data, default=str))
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
            await asyncio.sleep(2)
    except Exception as e:
        print(f"🔌 Disconnected (quotes): {e}")
    finally:
        await websocket.close()


if __name__ == "__main__":
    # Render expects host=0.0.0.0 and port from $PORT env
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

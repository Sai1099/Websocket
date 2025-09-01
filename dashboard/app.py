import streamlit as st
import json
import asyncio
import websockets

st.set_page_config("PKC Capital", page_icon="📈", layout="wide")
st.title(" Market Dashboard")

# Store data in session state
if 'data' not in st.session_state:
    st.session_state.data = []

async def get_market_data():
    uri = "wss://nselivedata.onrender.com/ws/indices"
    async with websockets.connect(uri) as websocket:
        message = await websocket.recv()
        return json.loads(message)

def display_data(market_data):
    # Show available tickers
    tickers = [item["index"] for item in market_data]
    #st.info(f"📊 Live Tickers: {', '.join(tickers)}")
    
    # Display market data in 3 columns
    cols = st.columns(3)
    
    for i, item in enumerate(market_data):
        with cols[i % 3]:
            price = float(item.get('last', 0))
            change = float(item.get('change', 0))
            
            # Color based on change
            if change > 0:
                st.success(f"**{item['index']}**\n₹{price:,.2f})")
            elif change < 0:
                st.error(f"**{item['index']}**\n₹{price:,.2f}")
            else:
                st.info(f"**{item['index']}**\n₹{price:,.2f}")

# Connect button
if st.button("🔗 Get Live Data"):
    with st.spinner("Connecting..."):
        try:
            data = asyncio.run(get_market_data())
            st.session_state.data = data
            st.success("✅ Connected!")
            display_data(data)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Show stored data if available
if st.session_state.data:
    st.write("---")
    st.subheader("Current Data")
    display_data(st.session_state.data)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="JIGAR'S Trading Journal", layout="wide")

# --- Initialize Session State ---
if "trades" not in st.session_state:
    st.session_state["trades"] = []

# --- Sidebar Navigation ---
menu = ["Add Trade", "View Trades", "Charts", "Summary"]
choice = st.sidebar.radio("📌 Navigate", menu)

# --- Add Trade Page ---
if choice == "Add Trade":
    st.title("➕ Add New Trade")

    with st.form("trade_form"):
        date = st.date_input("📅 Date")
        symbol = st.text_input("📈 Symbol (e.g. NIFTY, BANKNIFTY)")
        market_type = st.selectbox("🌍 Market Type", ["Equity", "Options", "Futures", "Forex", "Crypto"])
        entry_price = st.number_input("💵 Entry Price", min_value=0.0, format="%.2f")
        exit_price = st.number_input("💵 Exit Price", min_value=0.0, format="%.2f")
        quantity = st.number_input("🔢 Quantity", min_value=1, step=1)
        strategy = st.selectbox("🎯 Strategy", ["Breakout", "Reversal", "Scalping", "Swing", "Other"])
        stop_loss = st.number_input("🛑 Stop Loss", min_value=0.0, format="%.2f")
        outcome_summary = st.text_area("📝 Outcome Summary")

        submitted = st.form_submit_button("Save Trade")

        if submitted:
            pnl = (exit_price - entry_price) * quantity
            pnl_pct = ((exit_price - entry_price) / entry_price) * 100 if entry_price > 0 else 0

            trade = {
                "Date": date,
                "Symbol": symbol,
                "Market Type": market_type,
                "Entry": entry_price,
                "Exit": exit_price,
                "Qty": quantity,
                "PnL": pnl,
                "PnL %": pnl_pct,
                "Strategy": strategy,
                "Stop Loss": stop_loss,
                "Outcome": outcome_summary
            }

            st.session_state["trades"].append(trade)
            st.success("✅ Trade saved successfully!")

# --- View Trades Page ---
elif choice == "View Trades":
    st.title("📑 All Trades")

    if st.session_state["trades"]:
        df = pd.DataFrame(st.session_state["trades"])

        # Filters
        st.subheader("🔍 Filter Trades")
        strategy_filter = st.multiselect("Filter by Strategy", df["Strategy"].unique())
        market_filter = st.multiselect("Filter by Market Type", df["Market Type"].unique())

        filtered_df = df.copy()
        if strategy_filter:
            filtered_df = filtered_df[filtered_df["Strategy"].isin(strategy_filter)]
        if market_filter:
            filtered_df = filtered_df[filtered_df["Market Type"].isin(market_filter)]

        st.dataframe(filtered_df, use_container_width=True)

        # Export
        st.download_button("⬇ Download CSV", filtered_df.to_csv(index=False), "trading_journal.csv", "text/csv")
    else:
        st.info("No trades recorded yet.")

# --- Charts Page ---
elif choice == "Charts":
    st.title("📊 Trading Charts")

    if st.session_state["trades"]:
        df = pd.DataFrame(st.session_state["trades"])

        # Daily PnL
        st.subheader("📅 Daily PnL")
        daily_pnl = df.groupby("Date")["PnL"].sum()
        fig, ax = plt.subplots()
        daily_pnl.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        # Strategy-wise Distribution
        st.subheader("🎯 Strategy-wise PnL")
        strategy_pnl = df.groupby("Strategy")["PnL"].sum()
        fig2, ax2 = plt.subplots()
        strategy_pnl.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        st.pyplot(fig2)
    else:
        st.info("No data available for charts.")

# --- Summary Page ---
elif choice == "Summary":
    st.title("📈 Performance Summary")

    if st.session_state["trades"]:
        df = pd.DataFrame(st.session_state["trades"])

        total_trades = len(df)
        total_profit = df["PnL"].sum()
        win_rate = (df[df["PnL"] > 0].shape[0] / total_trades) * 100
        avg_rr = (df["PnL"].mean() / abs(df["Stop Loss"].mean())) if df["Stop Loss"].mean() > 0 else 0
        profit_factor = df[df["PnL"] > 0]["PnL"].sum() / abs(df[df["PnL"] < 0]["PnL"].sum()) if df[df["PnL"] < 0].shape[0] > 0 else float("inf")

        st.metric("📊 Total Trades", total_trades)
        st.metric("💰 Total Profit", f"{total_profit:.2f}")
        st.metric("✅ Win Rate", f"{win_rate:.2f}%")
        st.metric("⚖️ Avg. Reward/Risk", f"{avg_rr:.2f}")
        st.metric("📈 Profit Factor", f"{profit_factor:.2f}")
    else:
        st.info("No trades recorded yet.")

        
            

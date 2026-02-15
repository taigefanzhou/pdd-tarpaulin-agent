import streamlit as st
import pandas as pd

st.set_page_config(page_title="篷布拼多多决策系统", layout="wide")

st.title("篷布拼多多决策 Agent")

st.write("✅ 云端部署成功")

data = {
    "尺寸": ["2x3m", "3x4m", "4x6m"],
    "成本": [12, 18, 35],
    "建议售价": [19.9, 29.9, 59.9],
    "利润空间": ["20%", "25%", "30%"]
}

df = pd.DataFrame(data)

st.subheader("示例 SKU 决策表")
st.dataframe(df)

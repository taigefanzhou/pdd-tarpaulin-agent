import streamlit as st
import pandas as pd

st.set_page_config(page_title="篷布拼多多盈利决策系统", layout="wide")

st.title("篷布拼多多盈利决策 Agent（C 模式）")

# ===== 基础参数 =====
PLATFORM_RATE = 0.02
PAY_RATE = 0.006
ADS_RATE = 0.08
TOTAL_RATE = PLATFORM_RATE + PAY_RATE + ADS_RATE  # 10.6%

# ===== 物流规则 =====
def shipping_by_area(area):
    if area <= 8:
        return 6
    elif area <= 24:
        return 10
    else:
        return 18

# ===== 分层规则 =====
def layer_by_area(area):
    if area <= 8:
        return "引流款"
    elif area <= 24:
        return "主销款"
    else:
        return "利润款"

# ===== 反推售价函数 =====
def calc_price_by_target_profit(cost, shipping, target_profit_rate):
    # 净利润 = 售价 - 成本 - 物流 - 售价*费率
    # 反推售价：
    # 售价*(1-费率) = 成本 + 物流 + 售价*目标净利率
    # 售价 = (成本 + 物流) / (1 - 费率 - 目标净利率)
    return (cost + shipping) / (1 - TOTAL_RATE - target_profit_rate)

# ===== 输入区 =====
st.sidebar.header("参数调整")

cost = st.sidebar.number_input("输入成本（元）", min_value=0.0, value=18.0)
length = st.sidebar.number_input("长度（米）", min_value=0.0, value=3.0)
width = st.sidebar.number_input("宽度（米）", min_value=0.0, value=4.0)

area = length * width
shipping = shipping_by_area(area)
layer = layer_by_area(area)

st.subheader("SKU 基础信息")
st.write(f"面积：{area:.2f} ㎡")
st.write(f"物流成本：{shipping} 元")
st.write(f"自动分层：{layer}")

# ===== 价格计算 =====
breakeven_price = (cost + shipping) / (1 - TOTAL_RATE)

traffic_price = calc_price_by_target_profit(cost, shipping, 0.05)
main_price = calc_price_by_target_profit(cost, shipping, 0.20)
profit_price = calc_price_by_target_profit(cost, shipping, 0.35)

data = {
    "类型": ["保本价", "引流价(5%)", "主销价(20%)", "利润价(35%)"],
    "建议售价": [
        round(breakeven_price, 2),
        round(traffic_price, 2),
        round(main_price, 2),
        round(profit_price, 2),
    ]
}

df = pd.DataFrame(data)

st.subheader("盈利决策价格表")
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.write("费率说明：平台2% + 支付0.6% + 推广8% = 10.6%")

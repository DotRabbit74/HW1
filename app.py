import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import altair as alt
import pandas as pd

# --- CRISP-DM: Business Understanding ---
st.set_page_config(layout="wide")
st.title("互動式簡單線性迴歸分析")
st.markdown("""
本應用程式遵循 **CRISP-DM** 流程，旨在讓使用者透過互動式介面，直觀地了解簡單線性迴歸。
您可以調整參數來生成資料，並觀察模型如何從中學習並找出趨勢線。
""")

# --- CRISP-DM: Data Understanding ---
st.header("1. 資料理解與生成")
st.markdown("請在下方調整參數，以生成您的資料集：")

# Sidebar for user inputs
with st.sidebar:
    st.header("參數設定")
    a_param = st.slider("斜率 (a)", min_value=-5.0, max_value=5.0, value=2.0, step=0.1)
    b_param = st.slider("截距 (b)", min_value=-10.0, max_value=10.0, value=1.0, step=0.5)
    noise_param = st.slider("雜訊 (noise)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
    n_points_param = st.slider("資料點數量", min_value=10, max_value=500, value=100, step=10)

# Generate data based on user input
@st.cache_data
def generate_data(a, b, noise, n_points):
    x = np.linspace(-10, 10, n_points)
    y_true = a * x + b
    y_noisy = y_true + np.random.normal(0, noise, n_points)
    return pd.DataFrame({"x": x, "y": y_noisy, "y_true": y_true})

data_df = generate_data(a_param, b_param, noise_param, n_points_param)

# Display data chart
st.subheader("生成的資料散佈圖")
scatter_chart = alt.Chart(data_df).mark_circle(size=60, opacity=0.7).encode(
    x='x',
    y='y',
    tooltip=['x', 'y']
).interactive()

st.altair_chart(scatter_chart, use_container_width=True)


# --- CRISP-DM: Data Preparation ---
st.header("2. 資料準備")
st.markdown("資料已自動準備成模型可接受的格式 (特徵 X 與目標 y)。")
with st.expander("查看準備好的資料"):
    st.dataframe(data_df[['x', 'y']].head())


# --- CRISP-DM: Modeling ---
st.header("3. 模型建立")
st.markdown("我們使用 Scikit-learn 的 `LinearRegression` 模型來擬合資料。")

# Prepare data for scikit-learn
X = data_df[['x']]
y = data_df['y']

# Fit the model
model = LinearRegression()
model.fit(X, y)

# Get model coefficients
a_fit = model.coef_[0]
b_fit = model.intercept_

st.markdown(f"模型已訓練完成！")


# --- CRISP-DM: Evaluation ---
st.header("4. 模型評估")
st.markdown("我們將模型的預測結果與原始資料進行比較。")

# Create regression line dataframe
regression_line = pd.DataFrame({
    'x': data_df['x'],
    'y_pred': model.predict(X)
})

# Create line chart
line_chart = alt.Chart(regression_line).mark_line(color='red').encode(
    x='x',
    y='y_pred'
)

# Combine scatter and line chart
final_chart = (scatter_chart + line_chart).properties(
    title="模型評估：原始資料 vs. 迴歸線"
)

st.altair_chart(final_chart, use_container_width=True)

st.subheader("評估結果")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="模型找出的斜率 (a')", value=f"{a_fit:.2f}", delta=f"{a_fit - a_param:.2f} (與真實值的差異)")
with col2:
    st.metric(label="模型找出的截距 (b')", value=f"{b_fit:.2f}", delta=f"{b_fit - b_param:.2f} (與真實值的差異)")

r_squared = model.score(X, y)
st.metric(label="R-squared (決定係數)", value=f"{r_squared:.3f}")
st.markdown("R-squared 衡量了模型對資料變異性的解釋程度，值越接近 1 代表擬合效果越好。")


# --- CRISP-DM: Deployment ---
st.header("5. 部署")
st.markdown("""
這個應用程式本身就是部署的成果！您可以持續調整左側邊欄的參數，
並即時觀察各階段的結果變化，這有助於加深對線性迴歸的理解。

**如何分享或部署？**
1.  將此專案上傳到 GitHub。
2.  登入 [Streamlit Community Cloud](https://share.streamlit.io/)。
3.  點擊 "New app"，連結到您的 GitHub 儲存庫，然後點擊 "Deploy!"。
""")

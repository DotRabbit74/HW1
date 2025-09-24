# 專案建構流程計畫書：互動式簡單線性迴歸分析

## 專案目標
建立一個 Python Web 應用程式，用於解決簡單線性迴歸問題 (y = ax + b)，並遵循 CRISP-DM (Cross-Industry Standard Process for Data Mining) 的六個步驟。應用程式需提供互動式介面，讓使用者調整參數、生成資料、訓練模型並視覺化結果，同時清楚展示每個階段的過程與說明。

## 技術棧
*   **Web 框架:** Streamlit
*   **資料處理:** NumPy, Pandas
*   **機器學習:** Scikit-learn
*   **資料視覺化:** Altair (透過 Streamlit 內建圖表功能)

---

## 建構流程 (依據 CRISP-DM 階段)

### 1. 業務理解 (Business Understanding)
*   **目標:** 確立專案的商業目標，即建立一個互動式工具，幫助使用者直觀地理解簡單線性迴歸的原理、參數對資料的影響，以及模型如何從帶有雜訊的資料中學習趨勢。
*   **需求分析:**
    *   使用者應能透過介面調整線性迴歸模型的真實參數 (斜率 `a`、截距 `b`)、資料的雜訊程度 (`noise`) 和資料點數量 (`number of points`)。
    *   應用程式必須清晰地展示 CRISP-DM 的各個階段，並提供相應的說明。
    *   最終結果不僅包含程式碼和模型輸出，還需包含詳細的過程說明和視覺化呈現。
*   **實作步驟:**
    *   在 `app.py` 中設定 Streamlit 頁面標題和簡要的專案介紹，說明其 CRISP-DM 基礎。
*   **預期輸出:** 專案目標聲明、功能列表、`app.py` 的初始標題和說明文字。

### 2. 資料理解 (Data Understanding)
*   **目標:** 設計資料生成機制，並提供互動式介面讓使用者探索不同參數下生成的資料分佈。
*   **實作步驟:**
    *   **參數介面:** 在 Streamlit 側邊欄 (或主介面) 中，使用 `st.slider` 或 `st.number_input` 建立以下參數的輸入控制項：
        *   `a_param` (斜率): 範圍例如 -5.0 到 5.0。
        *   `b_param` (截距): 範圍例如 -10.0 到 10.0。
        *   `noise_param` (雜訊標準差): 範圍例如 0.0 到 10.0。
        *   `n_points_param` (資料點數量): 範圍例如 10 到 500。
    *   **資料生成函數:** 編寫一個 Python 函數 (`generate_data`)，接收上述參數。該函數將：
        *   生成等間隔的 `x` 值 (例如，使用 `np.linspace` 從 -10 到 10)。
        *   計算真實的 `y_true = a_param * x + b_param`。
        *   在 `y_true` 上添加高斯雜訊 (`np.random.normal(0, noise_param, n_points_param)`) 得到 `y_noisy`。
        *   將 `x` 和 `y_noisy` 組織成 Pandas DataFrame。
    *   **資料視覺化:** 使用 Altair 或 Streamlit 內建的 `st.altair_chart` 繪製 `x` 和 `y_noisy` 的散佈圖，讓使用者直觀地看到資料分佈。
*   **預期輸出:** 互動式參數輸入介面、資料生成邏輯 (`generate_data` 函數)、顯示原始資料散佈圖的 Streamlit 元件。

### 3. 資料準備 (Data Preparation)
*   **目標:** 將生成的資料轉換為 Scikit-learn 模型所需的標準輸入格式。
*   **實作步驟:**
    *   從 Pandas DataFrame 中提取特徵 `X` (需為二維陣列，例如 `data_df[['x']]`) 和目標 `y` (需為一維陣列，例如 `data_df['y']`)。
    *   由於資料是直接生成的且結構簡單，此階段主要為格式化，無需複雜的清理或轉換。
    *   在 Streamlit 介面中簡要說明此階段的自動化處理。
*   **預期輸出:** 格式化後的特徵 `X` 和目標 `y` 變數，Streamlit 介面上的資料準備說明。

### 4. 模型建立 (Modeling)
*   **目標:** 使用簡單線性迴歸演算法訓練模型，以找出最能擬合生成資料的趨勢線。
*   **實作步驟:**
    *   **模型選擇:** 導入 `sklearn.linear_model.LinearRegression`。
    *   **模型訓練:** 實例化 `LinearRegression` 模型，並使用 `model.fit(X, y)` 方法對準備好的資料進行訓練。
    *   **模型參數獲取:** 訓練完成後，從模型中獲取學習到的斜率 (`model.coef_[0]`) 和截距 (`model.intercept_`)。
*   **預期輸出:** 訓練完成的線性迴歸模型實例、模型學習到的斜率和截距，Streamlit 介面上的模型訓練完成提示。

### 5. 模型評估 (Evaluation)
*   **目標:** 評估訓練模型的性能，並將模型的預測結果與原始資料進行視覺化比較。
*   **實作步驟:**
    *   **預測:** 使用訓練好的模型對特徵 `X` 進行預測，得到模型的預測值 `y_pred`。
    *   **視覺化:** 在原始資料的散佈圖上，疊加繪製一條代表模型預測的迴歸線 (`x` vs `y_pred`)。
    *   **指標計算:** 計算模型的 R-squared 分數 (`model.score(X, y)`)，以量化模型的擬合優度。
    *   **結果展示:**
        *   在 Streamlit 介面中顯示模型學習到的斜率 (`a_fit`) 和截距 (`b_fit`)，並與使用者設定的真實值 (`a_param`, `b_param`) 進行比較，顯示差異。
        *   顯示計算出的 R-squared 值，並簡要解釋其意義。
*   **預期輸出:** 包含原始資料點和迴歸線的綜合散佈圖、模型評估指標 (R-squared)、模型學習到的參數與真實參數的比較結果。

### 6. 部署 (Deployment)
*   **目標:** 將上述所有功能整合到一個完整的 Streamlit Web 應用程式中，並提供部署到 Streamlit Cloud 或其他平台的指南。
*   **實作步驟:**
    *   將所有 CRISP-DM 階段的程式碼邏輯整合到單一的 `app.py` 檔案中。
    *   確保 Streamlit 的 `st.header`, `st.subheader`, `st.markdown` 等元素被有效利用，以清晰地標示和解釋每個 CRISP-DM 階段。
    *   建立 `requirements.txt` 檔案，列出所有必要的 Python 套件及其版本 (`streamlit`, `numpy`, `pandas`, `scikit-learn`, `altair`)。
    *   建立 `.gitignore` 檔案，排除不應提交到版本控制的檔案和目錄 (例如 `.venv/`, `__pycache__/`, `.streamlit/`)。
    *   編寫 `README.md` 檔案，提供專案簡介、如何本地運行應用程式的說明，以及如何部署到 Streamlit Cloud 的步驟。
*   **預期輸出:** 完整的 `app.py`、`requirements.txt`、`.gitignore`、`README.md` 檔案，以及在 `app.py` 中包含的部署說明。

---

**後續步驟:**
1.  確認 `app.py`、`requirements.txt`、`.gitignore`、`README.md` 檔案已成功建立。
2.  指導使用者如何在本地運行 Streamlit 應用程式。
3.  指導使用者如何將專案上傳至 GitHub 並部署到 Streamlit Cloud。

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 New Dashboard")

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["📈 Dashboard", "🤖 Prediksi"])

# =========================
# TAB 1: VISUALISASI
# =========================
with tab1:
    st.header("Visualisasi Data")

    df = pd.read_csv("data/data_mapping.csv")

    st.write("Preview Data:")
    st.dataframe(df.head())


# =========================
# TAB 2: PREDIKSI
# =========================
with tab2:
    st.header("Prediksi Model")

    # model = joblib.load("model.pkl")

    st.write("Input Data:")

    age = st.number_input("inputt", 17, 60)

    if st.button("Prediksi"):
        input_data = pd.DataFrame({
            'age': [age]
        })

        # pred = model.predict(input_data)

        # st.success(f"Hasil Prediksi: {pred[0]}")
        st.success(f"Hasil Prediksi: ???")
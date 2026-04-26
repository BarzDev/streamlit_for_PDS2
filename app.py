import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import joblib

st.set_page_config(page_title="Dashboard", layout="wide")
df = pd.read_csv("data/data_mapping.csv")

data_column = {
    "Course": "Study Program",
    "Daytime_evening_attendance": "Study Schedule",
    "Marital_status": "Marital Status",
    "Application_mode": "Admission Path"
}
colors = ["#ff6b6b", "#ffd166", "#06d6a0"]

# =========================
# FUNCTION
# =========================
def pivot(df, column):
    return df.groupby([column, 'Status']).size().unstack(fill_value=0).sort_values(by='Dropout', ascending=True)

def plot_pivot(df, column, label):
    df_piv = pivot(df, column)

    fig, ax = plt.subplots(figsize=(8,6))
    df_piv.plot(kind='barh', stacked=True, ax=ax, color=colors)

    ax.set_title(f'Value Count Status by {label}')
    ax.set_xlabel('Jumlah')
    ax.set_ylabel(column)

    return fig

def plot_percentage(df, column, label):
    df_piv = pivot(df, column)
    df_pct = df_piv.div(df_piv.sum(axis=1), axis=0)

    fig, ax = plt.subplots(figsize=(8, 6))
    df_pct.plot(kind='barh', stacked=True, ax=ax, color=colors)

    ax.set_title(f'Percentage Status by {label}')
    ax.set_xlabel('Percentage')
    ax.set_ylabel(column)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    return fig

st.title("📊 New Dashboard")

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["📈 Dashboard", "🤖 Prediksi"])


# =========================
# TAB 1: Dashboard
# =========================
with tab1:

    total = df['Status'].count()
    dropout = df[df['Status'] == 'Dropout']['Status'].count()
    enrolled = df[df['Status'] == 'Enrolled']['Status'].count()
    graduate = df[df['Status'] == 'Graduate']['Status'].count()
    dropout_pct = (dropout / total) * 100
    enrolled_pct = (enrolled / total) * 100
    graduate_pct = (graduate / total) * 100


    col_left, col_right = st.columns([1, 1])

    # =========================
    # KIRI: METRICS
    # =========================
    with col_left:
        st.markdown("### 📊 Summary")

        st.metric("Total data", int(total))

        c1, c2, c3, c4 = st.columns([1, 1, 1, 3])

        c1.metric("Dropout", int(dropout))
        c2.metric("Enrolled", int(enrolled))
        c3.metric("Graduate", int(graduate))

    # =========================
    # KANAN: PIE CHART
    # =========================
    with col_right:
        fig, ax = plt.subplots(figsize=(3, 2)) 

        labels = ["Dropout", "Enrolled", "Graduate"]
        sizes = [dropout, enrolled, graduate]

        wedges, texts, autotexts = ax.pie(
            sizes,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            radius=0.8,                    
            textprops={'fontsize': 8}    
        )

        ax.axis('equal')

        for t in autotexts:
            t.set_color("white")       
            t.set_fontsize(8)

        ax.legend(
            wedges,
            labels,
            loc="center left",          
            bbox_to_anchor=(1, 0.5),   
            fontsize=8,
            frameon=False
        )

        st.pyplot(fig)




    selected_column = st.selectbox(
    "Select Variable",
    options=list(data_column.keys()),
    format_func=lambda x: data_column[x]
)
    label = data_column[selected_column]

    col_pivot, col_pivot_percentage = st.columns(2)
    col_detail, col_detail_percentage = st.columns(2)

    
 
    with col_pivot:
        fig = plot_pivot(df,selected_column, label)
        st.pyplot(fig)

    with col_pivot_percentage:
        fig = plot_percentage(df,selected_column, label)
        st.pyplot(fig)

    sort_col = 'Dropout' 
    df_piv = pivot(df, selected_column)

    sorted_index = df_piv.sort_values(by=sort_col, ascending=False).index

    summary_df = df_piv.loc[sorted_index].copy()
    summary_df["Total"] = summary_df.sum(axis=1)

    summary_pct = df_piv.loc[sorted_index].div(
        df_piv.loc[sorted_index].sum(axis=1), axis=0
    ) * 100
    
    with col_detail:
        st.dataframe(summary_df, use_container_width=True)

    with col_detail_percentage:
        st.dataframe(summary_pct.round(1), use_container_width=True)



# =========================
# TAB 2: Predict
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
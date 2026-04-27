import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import joblib

st.set_page_config(page_title="Portofolio", layout="wide")

# ========================
# LOAD DATA
# ========================
df = pd.read_csv("data/data_mapping.csv")
model = joblib.load("model/rf_model.pkl")
scaler = joblib.load("model/scaler.pkl")   


data_column = {
    "Course": "Study Program",
    "Daytime_evening_attendance": "Study Schedule",
    "Marital_status": "Marital Status",
    "Tuition_fees_up_to_date": "Tuition Payment Status",
    "Debtor": "Outstanding Debt Status"
}
colors = ["#ff6b6b", "#ffd166", "#06d6a0"]

course_name_to_code = {
    "Advertising and Marketing Management": 9670,
    "Agronomy": 9003,
    "Animation and Multimedia Design": 171,
    "Basic Education": 9853,
    "Biofuel Production Technologies": 33,
    "Communication Design": 9070,
    "Equinculture": 9130,
    "Informatics Engineering": 9119,
    "Journalism and Communication": 9773,
    "Management": 9147,
    "Management (evening)": 9991,
    "Nursing": 9500,
    "Oral Hygiene": 9556,
    "Social Service": 9238,
    "Social Service (evening)": 8014,
    "Tourism": 9254,
    "Veterinary Nursing": 9085
}


# =========================
# FUNCTION LIST
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

st.title("🎓 Jaya-Jaya Institute Student Academic Analysis")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "🤖 Prediksi", "🗂️ Raw Data"])


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
    # METRICS
    # =========================
    with col_left:
        st.markdown("### 📊 Summary")

        st.metric("Total data", int(total))

        c1, c2, c3, c4 = st.columns([1, 1, 1, 3])

        c1.metric("Dropout", int(dropout))
        c2.metric("Enrolled", int(enrolled))
        c3.metric("Graduate", int(graduate))

    # =========================
    # PIE CHART
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

# =========================
# ANALIZE
# =========================

    selected_column = st.selectbox(
    "Select Variable",
    options=list(data_column.keys()),
    format_func=lambda x: data_column[x]
)
    label = data_column[selected_column]

    # ========================
    # LAYOUT
    # ========================
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


    # ========================
    # QUARTILE
    # ========================
    df['Sem1_Quartile'] = pd.qcut(
        df['Curricular_units_1st_sem_grade'],
        q=4,
        labels=['Q1', 'Q2', 'Q3', 'Q4']
    )

    df['Sem2_Quartile'] = pd.qcut(
        df['Curricular_units_2nd_sem_grade'],
        q=4,
        labels=['Q1', 'Q2', 'Q3', 'Q4']
    )

    # ========================
    # DISTRIBUSI (%)
    # ========================
    sem1_dist = pd.crosstab(df['Sem1_Quartile'], df['Status'], normalize='index') * 100
    sem2_dist = pd.crosstab(df['Sem2_Quartile'], df['Status'], normalize='index') * 100

    # ========================
    # LAYOUT
    # ========================
    st.subheader("Academic Performance and Student Status")
    col_sem1, col_sem2 = st.columns(2)

    # ========================
    # SEMESTER 1
    # ========================
    colors = {
        "Dropout": "#ff6b6b",
        "Enrolled": "#ffd166",
        "Graduate": "#06d6a0"
    }

    with col_sem1:
        st.subheader("📘 Semester 1")

        fig1, ax1 = plt.subplots(figsize=(5, 4))
        for col in sem1_dist.columns:
            ax1.plot(
                sem1_dist.index,
                sem1_dist[col],
                marker='o',
                label=col,
                color=colors.get(col, "#333333")
            )

            for x, y in zip(sem1_dist.index, sem1_dist[col]):
                ax1.text(x, y, f'{y:.1f}%', ha='center', fontsize=7)

        ax1.set_xlabel('Quartile')
        ax1.set_ylabel('Persentase (%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        st.pyplot(fig1)

    # ========================
    # SEMESTER 2 
    # ========================
    with col_sem2:
        st.subheader("📗 Semester 2")

        fig2, ax2 = plt.subplots(figsize=(5, 4))

        for col in sem2_dist.columns:
            ax2.plot(
                sem2_dist.index,
                sem2_dist[col],
                marker='o',
                label=col,
                color=colors.get(col, "#333333")
            )

            for x, y in zip(sem2_dist.index, sem2_dist[col]):
                ax2.text(x, y, f'{y:.1f}%', ha='center', fontsize=7)

        ax2.set_xlabel('Quartile')
        ax2.set_ylabel('Persentase (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        st.pyplot(fig2)

    sem1_range = df.groupby('Sem1_Quartile')['Curricular_units_1st_sem_grade'].agg(['min', 'max'])
    sem2_range = df.groupby('Sem2_Quartile')['Curricular_units_2nd_sem_grade'].agg(['min', 'max'])

    # ========================
    # LAYOUT
    # ========================
    col_value_sem1, col_value_sem2 = st.columns(2)
    # ---------- Value Semester 1 ----------
    with col_value_sem1:
        st.write("Grade Quartile Value")
        st.dataframe(sem1_range, use_container_width=True)

    # ---------- Value Semester 2 ----------
    with col_value_sem2:
        st.write("Grade Quartile Value")
        st.dataframe(sem2_range, use_container_width=True)

    sem1_group = df.pivot_table(
        values='Curricular_units_1st_sem_grade',
        index='Sem1_Quartile',
        columns='Status',
        aggfunc='count'
    )

    sem2_group = df.pivot_table(
        values='Curricular_units_2nd_sem_grade',
        index='Sem2_Quartile',
        columns='Status',
        aggfunc='count'
    )
    col_group_sem1, col_group_sem2 = st.columns(2)

    with col_group_sem1:
        st.write("Quartile Count")
        st.dataframe(sem1_group, use_container_width=True)

    with col_group_sem2:
        st.write("Quartile Count")    
        st.dataframe(sem2_group, use_container_width=True)


# =========================
# TAB 2: Predict
# =========================
with tab2:
    # ========================
    # MAPPING
    # ========================
    binary_map = {
        1: "Yes",
        0: "No"
    }

    target_label_map = {
        0: "Dropout",
        1: "Enrolled",
        2: "Graduate"
    }

    # ========================
    # UI
    # ========================

    # ========================
    # INPUT FORM (ONLY FEATURES)
    # ========================
    st.subheader("🎓 Academic")
    col_left, col_right = st.columns(2)

    with col_left:
        st.write("📊 Semester 1")
        cu_1st_enrolled = st.number_input("Enrolled (Sem 1)", 0, 30)
        cu_1st_approved = st.number_input("Approved (Sem 1)", 0, 30)
        cu_1st_grade = st.number_input("Grade (Sem 1)", 0.0, 20.0)

    with col_right:
        st.write("📊 Semester 2")
        cu_2nd_enrolled = st.number_input("Enrolled (Sem 2)", 0, 30)
        cu_2nd_approved = st.number_input("Approved (Sem 2)", 0, 30)
        cu_2nd_grade = st.number_input("Grade (Sem 2)", 0.0, 20.0)

    st.subheader("🎓 Course")
    selected_course = st.selectbox("🎓 Course", list(course_name_to_code.keys()))
    course_code = course_name_to_code[selected_course]

    st.subheader("💰 Financial")
    tuition = st.selectbox("Tuition Up To Date", list(binary_map.values()))
    debtor = st.selectbox("Debtor", list(binary_map.values()))

    # ========================
    # CONVERT INPUT → NUMERIC
    # ========================
    def reverse_map(mapping, value):
        return list(mapping.keys())[list(mapping.values()).index(value)]

    input_data = {
        'Curricular_units_2nd_sem_enrolled': cu_2nd_enrolled,
        'Curricular_units_2nd_sem_approved': cu_2nd_approved,
        'Curricular_units_2nd_sem_grade': cu_2nd_grade,

        'Curricular_units_1st_sem_enrolled': cu_1st_enrolled,
        'Curricular_units_1st_sem_approved': cu_1st_approved,
        'Curricular_units_1st_sem_grade': cu_1st_grade,

        'Course': course_code,
        'Tuition_fees_up_to_date': reverse_map(binary_map, tuition),
        'Debtor': reverse_map(binary_map, debtor)
    }

    df_input = pd.DataFrame([input_data])

    # ========================
    # PASTIKAN URUTAN FITUR SAMA
    # ========================
    feature_order = [
        'Curricular_units_2nd_sem_enrolled',
        'Curricular_units_2nd_sem_approved',
        'Curricular_units_2nd_sem_grade',
        'Curricular_units_1st_sem_enrolled',
        'Curricular_units_1st_sem_approved',
        'Curricular_units_1st_sem_grade',
        'Course',
        'Tuition_fees_up_to_date',
        'Debtor'
    ]

    df_input = df_input[feature_order]

    # ========================
    # PREDICT
    # ========================
    if st.button("🔮 Predict"):
        df_scaled = scaler.transform(df_input)
        
        pred = model.predict(df_scaled)[0]
        proba = model.predict_proba(df_scaled)[0]

        result = target_label_map[pred]

        # warna
        if result == "Dropout":
            color = "red"
        elif result == "Enrolled":
            color = "orange"
        else: 
            color = "green"

        st.markdown(f"<h3 style='color:{color}'>🎯 Predict Result: {result}</h3>", unsafe_allow_html=True)

        # tampilkan probability
        st.write("Probability")
        st.write({
            "Dropout": round(proba[0], 2),
            "Enrolled": round(proba[1], 2),
            "Graduate": round(proba[2], 2)
        })


# =========================
# TAB 3: Raw Data
# =========================
with tab3:
    st.header("Raw Data")
    st.dataframe(df, use_container_width=True)

st.markdown(
    """
    <hr>
    <p style='text-align:center; color:gray; font-size:16px;'>
        © 2026 Fakhrul_Akbar | Submission Dicoding Student Perfomance Analysis
    </p>
    """,
    unsafe_allow_html=True
)
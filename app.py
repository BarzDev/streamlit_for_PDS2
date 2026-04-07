import streamlit as st
import pandas as pd
import joblib

# ========================
# LOAD MODEL
# ========================
model = joblib.load("model/rf_model.pkl")
scaler = joblib.load("model/scaler.pkl")   

# ========================
# MAPPING
# ========================

application_mode_map = {
    1: "1st phase - general contingent",
    2: "Ordinance No. 612/93",
    5: "1st phase - special contingent (Azores)",
    7: "Holders of other higher courses",
    10: "Ordinance No. 854-B/99",
    15: "International student",
    16: "Special contingent (Madeira)",
    17: "2nd phase - general contingent",
    18: "3rd phase - general contingent",
    26: "Different Plan",
    27: "Other Institution",
    39: "Over 23 years old",
    42: "Transfer",
    43: "Change of course",
    44: "Technological specialization diploma",
    51: "Change of institution/course",
    53: "Short cycle diploma",
    57: "International change"
}

attendance_map = {
    1: "Daytime",
    0: "Evening"
}

gender_map = {
    1: "Male",
    0: "Female"
}

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
st.title("🎓Jaya-Jaya Institute Student Status Prediction")
st.write("Enter student data to predict status")

# ========================
# INPUT FORM
# ========================

st.subheader("📊 Academic")
cu_2nd_approved = st.number_input("2nd Sem Approved", 0, 30)
cu_2nd_grade = st.number_input("2nd Sem Grade", 0.0, 20.0)
cu_1st_approved = st.number_input("1st Sem Approved", 0, 30)
cu_1st_grade = st.number_input("1st Sem Grade", 0.0, 20.0)

st.subheader("💰 Financial")
tuition = st.selectbox("Tuition Up To Date", list(binary_map.values()))
scholarship = st.selectbox("Scholarship", list(binary_map.values()))
debtor = st.selectbox("Debtor", list(binary_map.values()))

st.subheader("👤 Demographics")
age = st.number_input("Age", 15, 70)
gender = st.selectbox("Gender", list(gender_map.values()))

st.subheader("📚 Activities")
cu_2nd_enrolled = st.number_input("2nd Sem Enrolled", 0, 30)
cu_1st_enrolled = st.number_input("1st Sem Enrolled", 0, 30)

st.subheader("📄 Background")
admission_grade = st.number_input("Admission Grade", 0.0, 200.0)
prev_grade = st.number_input("Previous Qualification Grade", 0.0, 200.0)
application_mode = st.selectbox("Application Mode", list(application_mode_map.values()))
attendance = st.selectbox("Attendance", list(attendance_map.values()))

# ========================
# CONVERT INPUT → NUMERIC
# ========================

def reverse_map(mapping, value):
    return list(mapping.keys())[list(mapping.values()).index(value)]

input_data = {
    'Curricular_units_2nd_sem_approved': cu_2nd_approved,
    'Curricular_units_2nd_sem_grade': cu_2nd_grade,
    'Curricular_units_1st_sem_approved': cu_1st_approved,
    'Curricular_units_1st_sem_grade': cu_1st_grade,

    'Tuition_fees_up_to_date': reverse_map(binary_map, tuition),
    'Scholarship_holder': reverse_map(binary_map, scholarship),
    'Debtor': reverse_map(binary_map, debtor),

    'Age_at_enrollment': age,
    'Gender': reverse_map(gender_map, gender),

    'Curricular_units_2nd_sem_enrolled': cu_2nd_enrolled,
    'Curricular_units_1st_sem_enrolled': cu_1st_enrolled,

    'Admission_grade': admission_grade,
    'Previous_qualification_grade': prev_grade,
    'Application_mode': reverse_map(application_mode_map, application_mode),
    'Daytime_evening_attendance': reverse_map(attendance_map, attendance)
}

df_input = pd.DataFrame([input_data])
df_scaled = scaler.transform(df_input) 
# ========================
# PREDICT
# ========================
if st.button("🔮 Predict"):
    
    pred = model.predict(df_scaled)[0]
    result = target_label_map[pred]

    if result == "Dropout":
        color = "red"
    elif result == "Enrolled":
        color = "orange"
    else: 
        color = "green"

    st.markdown(f"<h3 style='color:{color}'>🎯 Predict Result: {result}</h3>", unsafe_allow_html=True)


st.markdown(
    """
    <hr>
    <p style='text-align:center; color:gray; font-size:16px;'>
        © 2026 Fakhrul_Akbar | Submission Dicoding Studeng Perfomance Analysis
    </p>
    """,
    unsafe_allow_html=True
)
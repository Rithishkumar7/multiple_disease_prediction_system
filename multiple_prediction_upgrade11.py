

import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Enhanced Disease Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load models (update paths as needed)
try:
    # Assuming models are in the same directory as the script
    diabetes = pickle.load(open("trained_diabetes.model", 'rb'))
    heart = pickle.load(open("heart_disease.pkl", 'rb'))
    parkinson = pickle.load(open("parkinson_disease.pkl", 'rb'))
except FileNotFoundError:
    st.error("⚠️ Model files not found. Please ensure 'trained_diabetes.model', 'heart_disease.pkl', and 'parkinson_disease.pkl' are in the same directory as the script.")
    st.stop()

# Configure page


st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .risk-critical {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .risk-high {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .risk-moderate {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .risk-low {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .recommendation-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    /* Sidebar specific styling: yellow background and black text for titles/markdown */
    div[data-testid="stSidebar"] {
        background-color: #FFEB3B !important; /* yellow */
    }
    div[data-testid="stSidebar"] .markdown-text-container h2,
    div[data-testid="stSidebar"] .markdown-text-container h1,
    div[data-testid="stSidebar"] .markdown-text-container p {
        color: #000000 !important; /* black text for sidebar titles and content */
    }
</style>
""", unsafe_allow_html=True)
# ...existing code...
with st.sidebar:
    st.markdown("## 🏥 Navigation")
    selected = option_menu(
        "Multiple Disease Prediction",
        ['🩺 Dashboard', '🍯 Diabetes', '❤️ Heart Disease', '🧠 Parkinson\'s'],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#FFEB3B"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee", "color": "black"},
            "nav-link-selected": {"background-color": "#02ab21", "color": "black"},
        }
    )
# ...existing code...

# Severity Assessment Functions
def assess_diabetes_severity(pregnancies, glucose, bp, bmi, age, prediction_prob):
    """Assess diabetes severity based on input parameters and prediction probability"""
    risk_factors = 0
    
    # Analyze individual risk factors
    if glucose > 200:
        risk_factors += 3
    elif glucose > 140:
        risk_factors += 2
    elif glucose > 100:
        risk_factors += 1
        
    if bmi > 35:
        risk_factors += 2
    elif bmi > 30:
        risk_factors += 1
        
    if bp > 140:
        risk_factors += 1
        
    if age > 65:
        risk_factors += 1
    elif age > 45:
        risk_factors += 0.5
        
    if pregnancies > 5:
        risk_factors += 1
    
    # Determine severity
    if prediction_prob > 0.8 and risk_factors >= 4:
        return "CRITICAL", "🚨", "#f44336"
    elif prediction_prob > 0.6 or risk_factors >= 3:
        return "HIGH", "⚠️", "#ff9800"
    elif prediction_prob > 0.4 or risk_factors >= 2:
        return "MODERATE", "⚡", "#9c27b0"
    else:
        return "LOW", "✅", "#4caf50"

def assess_heart_severity(age, cp, trestbps, chol, thalach, prediction_prob):
    """Assess heart disease severity"""
    risk_factors = 0
    
    if age > 65:
        risk_factors += 2
    elif age > 55:
        risk_factors += 1
        
    if cp == 0:  # Typical angina
        risk_factors += 2
    elif cp == 1:  # Atypical angina
        risk_factors += 1
        
    if trestbps > 160:
        risk_factors += 2
    elif trestbps > 140:
        risk_factors += 1
        
    if chol > 300:
        risk_factors += 2
    elif chol > 240:
        risk_factors += 1
        
    if thalach < 100:
        risk_factors += 2
    elif thalach < 120:
        risk_factors += 1
    
    if prediction_prob > 0.8 and risk_factors >= 4:
        return "CRITICAL", "🚨", "#f44336"
    elif prediction_prob > 0.6 or risk_factors >= 3:
        return "HIGH", "⚠️", "#ff9800"
    elif prediction_prob > 0.4 or risk_factors >= 2:
        return "MODERATE", "⚡", "#9c27b0"
    else:
        return "LOW", "✅", "#4caf50"

def assess_parkinson_severity(prediction_prob):
    """Assess Parkinson's disease severity"""
    if prediction_prob > 0.8:
        return "HIGH", "⚠️", "#ff9800"
    elif prediction_prob > 0.6:
        return "MODERATE", "⚡", "#9c27b0"
    else:
        return "LOW", "✅", "#4caf50"

# Recommendation Functions
def get_diabetes_recommendations(severity, glucose, bmi):
    """Get personalized diabetes recommendations"""
    recommendations = {
        "immediate": [],
        "short_term": [],
        "lifestyle": [],
        "monitoring": []
    }
    
    if severity == "CRITICAL":
        recommendations["immediate"] = [
            "🚨 Seek IMMEDIATE emergency medical attention",
            "📞 Call emergency services or go to ER",
            "💊 Check if you have emergency medication available"
        ]
    elif severity == "HIGH":
        recommendations["immediate"] = [
            "📞 Schedule urgent appointment with doctor within 24-48 hours",
            "🩺 Consider visiting urgent care if primary doctor unavailable"
        ]
        
    if glucose > 140:
        recommendations["lifestyle"].extend([
            "🥗 Follow a strict diabetic diet (low carb, high fiber)",
            "🚶‍♀️ Engage in 30 minutes of moderate exercise daily",
            "💧 Stay well hydrated with water"
        ])
        
    if bmi > 30:
        recommendations["lifestyle"].extend([
            "⚖️ Focus on gradual weight loss (1-2 lbs per week)",
            "🍽️ Consider portion control and meal planning"
        ])
        
    recommendations["monitoring"] = [
        "📊 Monitor blood glucose levels regularly",
        "🩺 Schedule HbA1c test every 3-6 months",
        "👁️ Regular eye examinations",
        "🦶 Daily foot care and inspection"
    ]
    
    return recommendations

def get_heart_recommendations(severity, age, bp, chol):
    """Get personalized heart disease recommendations"""
    recommendations = {
        "immediate": [],
        "short_term": [],
        "lifestyle": [],
        "monitoring": []
    }
    
    if severity == "CRITICAL":
        recommendations["immediate"] = [
            "🚨 Seek IMMEDIATE cardiac evaluation",
            "📞 Contact cardiologist or emergency services",
            "💊 Have nitroglycerin available if prescribed"
        ]
    elif severity == "HIGH":
        recommendations["immediate"] = [
            "🏥 Schedule cardiology consultation within 1 week",
            "📋 Get ECG and stress test"
        ]
        
    if bp > 140:
        recommendations["lifestyle"].extend([
            "🧂 Reduce sodium intake (<2300mg/day)",
            "🏃‍♂️ Regular aerobic exercise (150 min/week)"
        ])
        
    if chol > 240:
        recommendations["lifestyle"].extend([
            "🥑 Heart-healthy diet (Mediterranean style)",
            "🚭 Quit smoking if applicable",
            "🍷 Limit alcohol consumption"
        ])
        
    recommendations["monitoring"] = [
        "📈 Regular blood pressure monitoring",
        "🩸 Lipid panel every 3-6 months",
        "⚖️ Weight management tracking",
        "💊 Medication adherence if prescribed"
    ]
    
    return recommendations

def get_parkinson_recommendations(severity):
    """Get personalized Parkinson's recommendations"""
    recommendations = {
        "immediate": [],
        "short_term": [],
        "lifestyle": [],
        "monitoring": []
    }
    
    if severity == "HIGH":
        recommendations["immediate"] = [
            "🧠 Schedule neurologist consultation",
            "📋 Get comprehensive neurological assessment"
        ]
    elif severity == "MODERATE":
        recommendations["short_term"] = [
            "👨‍⚕️ Discuss symptoms with primary care physician",
            "📝 Keep symptom diary"
        ]
        
    recommendations["lifestyle"] = [
        "🏃‍♀️ Regular exercise (especially balance training)",
        "🎵 Consider music or dance therapy",
        "🧘‍♀️ Stress management techniques",
        "😴 Maintain good sleep hygiene"
    ]
    
    recommendations["monitoring"] = [
        "📊 Track symptom progression",
        "💊 Monitor medication effects if prescribed",
        "🏥 Regular follow-ups with healthcare team"
    ]
    
    return recommendations

# Display Functions
def display_severity_assessment(severity, icon, color, disease_name):
    """Display severity assessment with styling"""
    st.markdown(f"""
    <div class="risk-{severity.lower()}">
        <h3>{icon} {disease_name} Risk Level: {severity}</h3>
    </div>
    """, unsafe_allow_html=True)

def display_recommendations(recommendations, title):
    """Display recommendations in organized sections"""
    st.markdown(f"### 📋 {title}")
    
    if recommendations["immediate"]:
        st.markdown("#### 🚨 Immediate Actions")
        for rec in recommendations["immediate"]:
            st.markdown(f"- {rec}")
            
    if recommendations["short_term"]:
        st.markdown("#### 📅 Short-term Actions (1-7 days)")
        for rec in recommendations["short_term"]:
            st.markdown(f"- {rec}")
            
    if recommendations["lifestyle"]:
        st.markdown("#### 🌟 Lifestyle Recommendations")
        for rec in recommendations["lifestyle"]:
            st.markdown(f"- {rec}")
            
    if recommendations["monitoring"]:
        st.markdown("#### 📊 Monitoring & Follow-up")
        for rec in recommendations["monitoring"]:
            st.markdown(f"- {rec}")

def create_risk_gauge(risk_percentage, title):
    """Create a risk gauge visualization"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgreen"},
                {'range': [25, 50], 'color': "yellow"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🏥 Navigation")
    selected = option_menu(
        "Multiple Disease Prediction",
        ['🩺 Dashboard', '🍯 Diabetes', '❤️ Heart Disease', '🧠 Parkinson\'s'],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

# Dashboard
if selected == "🩺 Dashboard":
    st.markdown('<h1 class="main-header">🏥 Health Prediction Dashboard</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🍯 Diabetes Prediction
        Predict diabetes risk based on key health indicators including glucose levels, BMI, and family history.
        """)
        
    with col2:
        st.markdown("""
        ### ❤️ Heart Disease Prediction  
        Assess cardiovascular risk using comprehensive cardiac health parameters and lifestyle factors.
        """)
        
    with col3:
        st.markdown("""
        ### 🧠 Parkinson's Prediction
        Analyze voice and motor symptoms to assess Parkinson's disease probability.
        """)
    
    st.markdown("---")
    
    # Health Tips Section
    st.markdown("### 💡 Daily Health Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.info("🥗 **Nutrition Tip**: Include at least 5 servings of fruits and vegetables in your daily diet.")
        st.info("🏃‍♀️ **Exercise Tip**: Aim for 150 minutes of moderate aerobic activity per week.")
        
    with tips_col2:
        st.info("😴 **Sleep Tip**: Maintain 7-9 hours of quality sleep for optimal health.")
        st.info("🧘‍♀️ **Wellness Tip**: Practice stress management through meditation or deep breathing.")

# Diabetes Prediction
elif selected == "🍯 Diabetes":
    st.markdown('<h1 class="main-header">🍯 Diabetes Risk Assessment</h1>', unsafe_allow_html=True)
    
    # Input form
    with st.form("diabetes_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, value=0)
            glucose = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=100)
            blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=200, value=80)
            
        with col2:
            skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)
            insulin = st.number_input("Insulin Level (μU/mL)", min_value=0, max_value=900, value=80)
            bmi = st.number_input("BMI", min_value=10.0, max_value=70.0, value=25.0, step=0.1)
            
        with col3:
            pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.5, step=0.01)
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
        
        submitted = st.form_submit_button("🔍 Analyze Diabetes Risk", use_container_width=True)
    
    if submitted:
        try:
            # Make prediction
            prediction = diabetes.predict([[pregnancies, glucose, blood_pressure, skin_thickness, 
                                            insulin, bmi, pedigree, age]])
            prediction_proba = diabetes.predict_proba([[pregnancies, glucose, blood_pressure, skin_thickness, 
                                                         insulin, bmi, pedigree, age]])[0]
            
            # Get severity assessment
            severity, icon, color = assess_diabetes_severity(pregnancies, glucose, blood_pressure, bmi, age, prediction_proba[1])
            
            # Display results
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_severity_assessment(severity, icon, color, "Diabetes")
                
                if prediction[0] == 1:
                    st.error(f"⚠️ **High Risk of Diabetes Detected** (Confidence: {prediction_proba[1]:.1%})")
                else:
                    st.success(f"✅ **Low Risk of Diabetes** (Confidence: {prediction_proba[0]:.1%})")
                
                # Get and display recommendations
                recommendations = get_diabetes_recommendations(severity, glucose, bmi)
                display_recommendations(recommendations, "Diabetes Management Recommendations")
                
            with col2:
                # Risk gauge
                risk_fig = create_risk_gauge(prediction_proba[1] * 100, "Diabetes Risk %")
                st.plotly_chart(risk_fig, use_container_width=True)
                
                # Risk factors breakdown
                st.markdown("#### 📊 Risk Factors Analysis")
                factors = []
                if glucose > 140: factors.append("High Glucose")
                if bmi > 30: factors.append("High BMI")
                if blood_pressure > 140: factors.append("High BP")
                if age > 45: factors.append("Age Factor")
                if pregnancies > 3: factors.append("Multiple Pregnancies")
                
                for factor in factors:
                    st.warning(f"⚠️ {factor}")
                    
                if not factors:
                    st.success("✅ No major risk factors detected")
            
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

# Heart Disease Prediction
elif selected == "❤️ Heart Disease":
    st.markdown('<h1 class="main-header">❤️ Heart Disease Risk Assessment</h1>', unsafe_allow_html=True)
    
    with st.form("heart_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=50)
            sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
            cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3], 
                               format_func=lambda x: ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"][x])
            trestbps = st.number_input("Resting Blood Pressure (mmHg)", min_value=80, max_value=250, value=120)
            chol = st.number_input("Serum Cholesterol (mg/dL)", min_value=100, max_value=600, value=200)
            
        with col2:
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1], 
                               format_func=lambda x: "No" if x == 0 else "Yes")
            restecg = st.selectbox("Resting ECG", options=[0, 1, 2],
                                   format_func=lambda x: ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"][x])
            thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150)
            exang = st.selectbox("Exercise Induced Angina", options=[0, 1],
                                 format_func=lambda x: "No" if x == 0 else "Yes")
            
        with col3:
            oldpeak = st.number_input("ST depression induced by exercise", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
            slope = st.selectbox("Slope of peak exercise ST segment", options=[0, 1, 2],
                                 format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x])
            ca = st.selectbox("Number of major vessels colored by fluoroscopy", options=[0, 1, 2, 3])
            thal_map = {
            3: "Normal",
            6: "Fixed Defect",
            7: "Reversible Defect"
            }
        
            thal = st.selectbox(
            "Thalassemia",
            options=list(thal_map.keys()),
            format_func=lambda x: thal_map[x]
            )
        
        submitted = st.form_submit_button("🔍 Analyze Heart Disease Risk", use_container_width=True)
    
    if submitted:
        try:
            # Make prediction
            prediction = heart.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            prediction_proba = heart.predict_proba([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])[0]
            
            # Get severity assessment
            severity, icon, color = assess_heart_severity(age, cp, trestbps, chol, thalach, prediction_proba[1])
            
            # Display results
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_severity_assessment(severity, icon, color, "Heart Disease")
                
                if prediction[0] == 1:
                    st.error(f"⚠️ **High Risk of Heart Disease Detected** (Confidence: {prediction_proba[1]:.1%})")
                else:
                    st.success(f"✅ **Low Risk of Heart Disease** (Confidence: {prediction_proba[0]:.1%})")
                
                # Get and display recommendations
                recommendations = get_heart_recommendations(severity, age, trestbps, chol)
                display_recommendations(recommendations, "Heart Health Management Recommendations")
                
            with col2:
                # Risk gauge
                risk_fig = create_risk_gauge(prediction_proba[1] * 100, "Heart Disease Risk %")
                st.plotly_chart(risk_fig, use_container_width=True)
                
                # Risk factors breakdown
                st.markdown("#### 📊 Risk Factors Analysis")
                factors = []
                if age > 55: factors.append("Age Factor")
                if cp in [0, 1]: factors.append("Chest Pain")
                if trestbps > 140: factors.append("High BP")
                if chol > 240: factors.append("High Cholesterol")
                if thalach < 120: factors.append("Low Max HR")
                if exang == 1: factors.append("Exercise Angina")
                
                for factor in factors:
                    st.warning(f"⚠️ {factor}")
                    
                if not factors:
                    st.success("✅ No major risk factors detected")
                    
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

# Parkinson's Disease Prediction
elif selected == "🧠 Parkinson's":
    st.markdown('<h1 class="main-header">🧠 Parkinson\'s Disease Risk Assessment</h1>', unsafe_allow_html=True)
    
    st.info("ℹ️ This assessment uses voice and motor function parameters. Please consult with a neurologist for comprehensive evaluation.")
    
    with st.form("parkinson_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Voice Frequency Parameters**")
            MDVP_Fo = st.number_input("MDVP:Fo(Hz)", min_value=0.0, max_value=300.0, value=150.0, step=0.1)
            MDVP_Fhi = st.number_input("MDVP:Fhi(Hz)", min_value=0.0, max_value=400.0, value=200.0, step=0.1)
            MDVP_Flo = st.number_input("MDVP:Flo(Hz)", min_value=0.0, max_value=200.0, value=100.0, step=0.1)
            MDVP_Jitter = st.number_input("MDVP:Jitter(%)", min_value=0.0, max_value=1.0, value=0.01, step=0.001)
            MDVP_Jitter_Abs = st.number_input("MDVP:Jitter(Abs)", min_value=0.0, max_value=0.1, value=0.0001, step=0.00001)
            MDVP_RAP = st.number_input("MDVP:RAP", min_value=0.0, max_value=0.5, value=0.01, step=0.001)
            MDVP_PPQ = st.number_input("MDVP:PPQ", min_value=0.0, max_value=0.5, value=0.01, step=0.001)
            Jitter_DDP = st.number_input("Jitter:DDP", min_value=0.0, max_value=1.0, value=0.03, step=0.001)
            
        with col2:
            st.markdown("**Shimmer Parameters**")
            MDVP_Shimmer = st.number_input("MDVP:Shimmer", min_value=0.0, max_value=1.0, value=0.03, step=0.001)
            MDVP_Shimmer_dB = st.number_input("MDVP:Shimmer(dB)", min_value=0.0, max_value=5.0, value=0.3, step=0.01)
            Shimmer_APQ3 = st.number_input("Shimmer:APQ3", min_value=0.0, max_value=1.0, value=0.015, step=0.001)
            Shimmer_APQ5 = st.number_input("Shimmer:APQ5", min_value=0.0, max_value=1.0, value=0.02, step=0.001)
            MDVP_APQ = st.number_input("MDVP:APQ", min_value=0.0, max_value=1.0, value=0.025, step=0.001)
            Shimmer_DDA = st.number_input("Shimmer:DDA", min_value=0.0, max_value=1.0, value=0.045, step=0.001)
            NHR = st.number_input("NHR", min_value=0.0, max_value=1.0, value=0.02, step=0.001)
            HNR = st.number_input("HNR", min_value=0.0, max_value=50.0, value=20.0, step=0.1)
            
        with col3:
            st.markdown("**Other Parameters**")
            RPDE = st.number_input("RPDE", min_value=0.0, max_value=1.0, value=0.5, step=0.001)
            DFA = st.number_input("DFA", min_value=0.0, max_value=1.0, value=0.7, step=0.001)
            spread1 = st.number_input("spread1", min_value=-10.0, max_value=10.0, value=-5.0, step=0.1)
            spread2 = st.number_input("spread2", min_value=-10.0, max_value=10.0, value=0.2, step=0.01)
            D2 = st.number_input("D2", min_value=0.0, max_value=5.0, value=2.0, step=0.01)
            PPE = st.number_input("PPE", min_value=0.0, max_value=1.0, value=0.2, step=0.001)
        
        submitted = st.form_submit_button("🔍 Analyze Parkinson's Risk", use_container_width=True)
    
    if submitted:
        try:
            # Prepare input data for prediction
            input_data = [
                MDVP_Fo, MDVP_Fhi, MDVP_Flo,
                MDVP_Jitter, MDVP_Jitter_Abs, MDVP_RAP, MDVP_PPQ, Jitter_DDP,
                MDVP_Shimmer, MDVP_Shimmer_dB, Shimmer_APQ3, Shimmer_APQ5, MDVP_APQ, Shimmer_DDA,
                NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE
            ]
            
            prediction = parkinson.predict([input_data])
            prediction_proba = parkinson.predict_proba([input_data])[0]
            
            # Get severity assessment
            severity, icon, color = assess_parkinson_severity(prediction_proba[1])
            
            # Display results
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_severity_assessment(severity, icon, color, "Parkinson's Disease")
                
                if prediction[0] == 1:
                    st.error(f"⚠️ **High Risk of Parkinson's Disease Detected** (Confidence: {prediction_proba[1]:.1%})")
                else:
                    st.success(f"✅ **Low Risk of Parkinson's Disease** (Confidence: {prediction_proba[0]:.1%})")
                
                # Get and display recommendations
                recommendations = get_parkinson_recommendations(severity)
                display_recommendations(recommendations, "Parkinson's Disease Management Recommendations")
                
            with col2:
                # Risk gauge
                risk_fig = create_risk_gauge(prediction_proba[1] * 100, "Parkinson's Risk %")
                st.plotly_chart(risk_fig, use_container_width=True)
                
                # Information box
                st.markdown("#### 📋 Important Notes")
                st.info("""
                🔬 **Voice Analysis**: This assessment analyzes voice patterns and motor function indicators.
                
                👨‍⚕️ **Professional Consultation**: Always consult with a neurologist for proper diagnosis.
                
                📊 **Early Detection**: Early intervention can significantly improve quality of life.
                """)
                
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

# Footer with additional features
st.markdown("---")

# Emergency Contacts Section
st.markdown("### 🚨 Emergency Contacts")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🚑 Emergency Services**
    - Emergency: 911
    - Poison Control: 1-800-222-1222
    """)

with col2:
    st.markdown("""
    **🏥 Health Resources**
    - CDC: 1-800-CDC-INFO
    - Health Info: 1-800-336-4797
    """)

with col3:
    st.markdown("""
    **💊 Medication Support**
    - Drug Info: 1-800-FDA-1088
    - Pharmacy Help: 1-800-MEDICARE
    """)

# Health Tips and Educational Content
with st.expander("📚 Health Education & Tips"):
    tab1, tab2, tab3, tab4 = st.tabs(["🍯 Diabetes", "❤️ Heart Health", "🧠 Neurological", "🌟 General Wellness"])
    
    with tab1:
        st.markdown("""
        ### Diabetes Prevention & Management
        
        **🥗 Dietary Guidelines:**
        - Choose complex carbohydrates over simple sugars
        - Include fiber-rich foods (vegetables, whole grains)
        - Monitor portion sizes and meal timing
        - Stay hydrated with water instead of sugary drinks
        
        **🏃‍♀️ Exercise Recommendations:**
        - 150 minutes of moderate aerobic activity weekly
        - Include strength training 2-3 times per week
        - Monitor blood glucose before and after exercise
        - Consider post-meal walks to help control blood sugar
        
        **📊 Monitoring:**
        - Regular blood glucose testing
        - HbA1c testing every 3-6 months
        - Annual eye and foot examinations
        - Blood pressure and cholesterol checks
        """)
    
    with tab2:
        st.markdown("""
        ### Heart Disease Prevention
        
        **❤️ Heart-Healthy Habits:**
        - Follow Mediterranean or DASH diet
        - Limit saturated and trans fats
        - Reduce sodium intake (<2,300mg/day)
        - Include omega-3 rich foods (fish, nuts)
        
        **🚭 Lifestyle Modifications:**
        - Quit smoking and avoid secondhand smoke
        - Limit alcohol consumption
        - Manage stress through relaxation techniques
        - Maintain healthy weight (BMI 18.5-24.9)
        
        **📈 Regular Monitoring:**
        - Blood pressure checks
        - Cholesterol screening
        - Regular cardiac check-ups
        - ECG and stress tests as recommended
        """)
    
    with tab3:
        st.markdown("""
        ### Neurological Health
        
        **🧠 Brain Health:**
        - Engage in mental stimulation (puzzles, reading)
        - Social engagement and community involvement
        - Regular physical exercise
        - Adequate sleep (7-9 hours nightly)
        
        **🎵 Parkinson's Specific:**
        - Music and dance therapy
        - Speech therapy exercises
        - Balance and coordination training
        - Medication adherence and timing
        
        **⚠️ Warning Signs:**
        - Tremors or shaking
        - Slowness of movement
        - Stiffness or rigidity
        - Balance problems
        """)
    
    with tab4:
        st.markdown("""
        ### General Wellness Tips
        
        **🌟 Daily Habits:**
        - Maintain consistent sleep schedule
        - Practice stress management techniques
        - Stay socially connected
        - Regular health screenings
        
        **🥗 Nutrition Basics:**
        - Eat a variety of colorful fruits and vegetables
        - Choose whole grains over refined grains
        - Include lean proteins in your diet
        - Limit processed and packaged foods
        
        **🏃‍♀️ Physical Activity:**
        - Find activities you enjoy
        - Start slowly and gradually increase intensity
        - Include both cardio and strength training
        - Listen to your body and rest when needed
        """)

# Risk Calculator Section
with st.expander("🧮 Additional Health Calculators"):
    calc_tab1, calc_tab2 = st.tabs(["BMI Calculator", "Blood Pressure Category"])
    
    with calc_tab1:
        st.markdown("### BMI Calculator")
        col1, col2 = st.columns(2)
        with col1:
            height_ft = st.number_input("Height (feet)", min_value=1, max_value=8, value=5)
            height_in = st.number_input("Height (inches)", min_value=0, max_value=11, value=8)
        with col2:
            weight_lbs = st.number_input("Weight (pounds)", min_value=50, max_value=500, value=150)
        
        if st.button("Calculate BMI"):
            height_inches = (height_ft * 12) + height_in
            height_meters = height_inches * 0.0254
            weight_kg = weight_lbs * 0.453592
            bmi = weight_kg / (height_meters ** 2)
            
            st.metric("Your BMI", f"{bmi:.1f}")
            
            if bmi < 18.5:
                st.info("Category: Underweight")
            elif bmi < 25:
                st.success("Category: Normal weight")
            elif bmi < 30:
                st.warning("Category: Overweight")
            else:
                st.error("Category: Obese")
    
    with calc_tab2:
        st.markdown("### Blood Pressure Category")
        systolic = st.number_input("Systolic BP (top number)", min_value=70, max_value=250, value=120)
        diastolic = st.number_input("Diastolic BP (bottom number)", min_value=40, max_value=150, value=80)
        
        if st.button("Check BP Category"):
            if systolic < 120 and diastolic < 80:
                st.success("Normal: Less than 120/80 mmHg")
            elif systolic < 130 and diastolic < 80:
                st.info("Elevated: 120-129 systolic and less than 80 diastolic")
            elif (systolic >= 130 and systolic < 140) or (diastolic >= 80 and diastolic < 90):
                st.warning("High Blood Pressure (Hypertension Stage 1): 130-139 systolic or 80-89 diastolic")
            elif systolic >= 140 or diastolic >= 90:
                st.error("High Blood Pressure (Hypertension Stage 2): 140 or higher systolic or 90 or higher diastolic")
            else:
                st.error("Hypertensive Crisis: Higher than 180 systolic and/or higher than 120 diastolic. Seek emergency medical attention.")





# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 14:15:17 2025

@author: rithi
"""

import pickle
import streamlit as slt
from streamlit_option_menu import option_menu;
diabetes=pickle.load(open("trained_diabetes.model",'rb'))
heart=pickle.load(open("heart_disease.pkl",'rb'))
parkinson=pickle.load(open("parkinson_disease.pkl",'rb'))
with slt.sidebar:
    
    selected=option_menu("MULTIPLE DISEASE PREDICTION",['DIABETES_PREDICTION','HEART_DISEASE_PREDICTION','PARKINSON_PREDICTION'],default_index=0 )
    
    
    
    
    
if selected=="DIABETES_PREDICTION":
    
    slt.title("DIABETES DISEASE PREDICTION")
    
    Pregnancies=(slt.text_input("enter the number of pregnancies"))
    Glucose=(slt.text_input("enter the number of glucose"))
    BloodPressure=(slt.text_input("enter the number of blood pressure"))
    SkinThickness=(slt.text_input("enter the number of skinthickness"))
    Insulin=(slt.text_input("enter the number of insulin level"))
    BMI=(slt.text_input("enter the BMI"))
    DiabetesPedigreeFunction=(slt.text_input("enter the pedigree_function"))
    Age=(slt.text_input("enter the AGE"))
    try:
        Pregnancies=float(Pregnancies)
        Glucose=float(Glucose)
        BloodPressure=float(BloodPressure)
        SkinThickness=float(SkinThickness)
        Insulin=float(Insulin)
        BMI=float(BMI)
        DiabetesPedigreeFunction=float(DiabetesPedigreeFunction)
        Age=float(Age)
    except ValueError:
        print("enter all fieldss correctly")
        
    
    diab=" "
    
    if slt.button('TEST'):
        diabetic=diabetes.predict([[Pregnancies	,Glucose,	BloodPressure,	SkinThickness,Insulin,	BMI,	DiabetesPedigreeFunction,	Age]])
        if(diabetic[0]==1):
            diab="the person is diabetic"
            
        else:
            diab="the person is healthy"
    slt.success(diab)
    
    
    
    
    
    
    
    
if selected=="HEART_DISEASE_PREDICTION":
    slt.title("HEART DISEASE PREDICTION")
    
    age =  (slt.text_input("Enter the age"))
    sex =  (slt.text_input("Enter the sex (0 = female, 1 = male)"))
    cp =  (slt.text_input("Enter chest pain type (0: typical angina, 1: atypical angina, 2: non-anginal pain, 3: asymptomatic)"))
    trestbps =  (slt.text_input("Enter the resting blood pressure (trestbps)"))
    chol =  (slt.text_input("Enter the serum cholesterol (chol)"))
    fbs =  (slt.text_input("Is fasting blood sugar > 120 mg/dl? (1 = True, 0 = False)"))
    restecg =  (slt.text_input("Enter resting electrocardiographic result (0: normal, 1: ST-T wave abnormality, 2: left ventricular hypertrophy)"))
    thalach =  (slt.text_input("Enter the maximum heart rate achieved (thalach)"))
    exang =  (slt.text_input("Is there exercise induced angina? (1 = Yes, 0 = No)"))
    oldpeak = (slt.text_input("Enter the depression induced by exercise relative to rest (oldpeak)"))
    slope =  (slt.text_input("Enter the slope of the peak exercise ST segment (0: upsloping, 1: flat, 2: downsloping)"))
    ca =  (slt.text_input("Enter the number of major vessels colored by fluoroscopy (0-3)"))
    thal =  (slt.text_input("Enter the thalassemia (3: normal, 6: fixed defect, 7: reversible defect)"))
    try:
        age = float(age)    # Ensure the value is a float
        sex = int(sex)      # Ensure the value is an integer
        cp = int(cp)        # Ensure the value is an integer
        trestbps = float(trestbps)  # Ensure the value is a float
        chol = float(chol)        # Ensure the value is a float
        fbs = int(fbs)      # Ensure the value is an integer
        restecg = int(restecg)  # Ensure the value is an integer
        thalach = float(thalach)  # Ensure the value is a float
        exang = int(exang)  # Ensure the value is an integer
        oldpeak = float(oldpeak)  # Ensure the value is a float
        slope = int(slope)  # Ensure the value is an integer
        ca = int(ca)        # Ensure the value is an integer
        thal = int(thal)    # Ensure the value is an integer

    except:
        print("enterr ")
    heart_disease = ""
    
     
    if slt.button('TEST'):
         # Make prediction using the heart disease model
        heart_result = heart.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
        if heart_result[0] == 1:
            heart_disease = "The person is likely to have heart disease."
        else:
             heart_disease = "The person is not likely to have heart disease."
     
    slt.success(heart_disease)
        
     
    
if selected=="PARKINSON_PREDICTION":
    slt.title("PARKINSON DISEASE PREDICTION")
     
    # User inputs for Parkinson's disease prediction using text_input and type-casting
    MDVP_Fo = (slt.text_input("Enter MDVP:Fo(Hz)"))
    MDVP_Fhi = (slt.text_input("Enter MDVP:Fhi(Hz)"))
    MDVP_Flo = (slt.text_input("Enter MDVP:Flo(Hz)"))
    MDVP_Jitter = (slt.text_input("Enter MDVP:Jitter(%)"))
    MDVP_Jitter_Abs = (slt.text_input("Enter MDVP:Jitter(Abs)"))
    MDVP_RAP = (slt.text_input("Enter MDVP:RAP"))
    MDVP_PPQ = (slt.text_input("Enter MDVP:PPQ"))
    Jitter_DDP = (slt.text_input("Enter Jitter:DDP"))
    MDVP_Shim = (slt.text_input("Enter MDVP:Shimmer"))
    MDVP_Shim_dB = (slt.text_input("Enter MDVP:Shimmer(dB)"))
    Shimmer_APQ3 = (slt.text_input("Enter Shimmer:APQ3"))
    Shimmer_APQ5 = (slt.text_input("Enter Shimmer:APQ5"))
    MDVP_APQ = (slt.text_input("Enter MDVP:APQ"))
    Shimmer_DDA = (slt.text_input("Enter Shimmer:DDA"))
    NHR = (slt.text_input("Enter NHR"))
    HNR = (slt.text_input("Enter HNR"))
    RPDE = (slt.text_input("Enter RPDE"))
    DFA = (slt.text_input("Enter DFA"))
    spread1 = (slt.text_input("Enter spread1"))
    spread2 = (slt.text_input("Enter spread2"))
    D2 = (slt.text_input("Enter D2"))
    PPE = (slt.text_input("Enter PPE"))
    try:
       MDVP_Fo = float(MDVP_Fo) if MDVP_Fo else 0.0
       MDVP_Fhi = float(MDVP_Fhi) if MDVP_Fhi else 0.0
       MDVP_Flo = float(MDVP_Flo) if MDVP_Flo else 0.0
       MDVP_Jitter = float(MDVP_Jitter) if MDVP_Jitter else 0.0
       MDVP_Jitter_Abs = float(MDVP_Jitter_Abs) if MDVP_Jitter_Abs else 0.0
       MDVP_RAP = float(MDVP_RAP) if MDVP_RAP else 0.0
       MDVP_PPQ = float(MDVP_PPQ) if MDVP_PPQ else 0.0
       Jitter_DDP = float(Jitter_DDP) if Jitter_DDP else 0.0
       MDVP_Shim = float(MDVP_Shim) if MDVP_Shim else 0.0
       MDVP_Shim_dB = float(MDVP_Shim_dB) if MDVP_Shim_dB else 0.0
       Shimmer_APQ3 = float(Shimmer_APQ3) if Shimmer_APQ3 else 0.0
       Shimmer_APQ5 = float(Shimmer_APQ5) if Shimmer_APQ5 else 0.0
       MDVP_APQ = float(MDVP_APQ) if MDVP_APQ else 0.0
       Shimmer_DDA = float(Shimmer_DDA) if Shimmer_DDA else 0.0
       NHR = float(NHR) if NHR else 0.0
       HNR = float(HNR) if HNR else 0.0
       RPDE = float(RPDE) if RPDE else 0.0
       DFA = float(DFA) if DFA else 0.0
       spread1 = float(spread1) if spread1 else 0.0
       spread2 = float(spread2) if spread2 else 0.0
       D2 = float(D2) if D2 else 0.0
       PPE = float(PPE) if PPE else 0.0
    except ValueError :
       print("Erro Please ensure all inputs are numeric values.")
    
    parkinson_result = ""
    
    if slt.button('TEST'):
        # Make prediction using the Parkinson model
        parkinson_prediction = parkinson.predict([[MDVP_Fo, MDVP_Fhi, MDVP_Flo, MDVP_Jitter, MDVP_Jitter_Abs, MDVP_RAP, MDVP_PPQ, Jitter_DDP, MDVP_Shim, MDVP_Shim_dB, 
                                                   Shimmer_APQ3, Shimmer_APQ5, MDVP_APQ, Shimmer_DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]])
        if parkinson_prediction[0] == 1:
            parkinson_result = "The person is likely to have Parkinson's disease."
        else:
            parkinson_result = "The person is not likely to have Parkinson's disease."
    
    slt.success(parkinson_result)
    

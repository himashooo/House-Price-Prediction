import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("House_price_model.pkl")
zip_info = joblib.load("zip_info.pkl")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: white;
    text-align: center;
}

.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    background-color: #27ae60;
    color: white;
    font-size: 22px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #219150;
}

[data-testid="stMetric"] {
    background-color: #1e1e1e;
    border-radius: 12px;
    padding: 10px;
}

div[data-baseweb="select"] > div {
    background-color: #1e1e1e;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🏠 House Price Predictor")
st.markdown(
    "<h4 style='text-align:center;'>Predict the value of your dream home</h4>",
    unsafe_allow_html=True
)

# ---------------- CENTER IMAGE ----------------
left, center, right = st.columns([1.3,3,1])

with center:
    st.image(
        "https://images.unsplash.com/photo-1568605114967-8130f3a36994",
        width=700
    )

st.divider()

# ---------------- INPUTS ----------------
col1, col2 = st.columns(2)

with col1:
    bedrooms = st.number_input("🛏 Bedrooms", 1, 10, 3)
    bathrooms = st.number_input("🛁 Bathrooms", 1.0, 10.0, 2.0)
    floors = st.number_input("🏢 Floors", 1, 5, 1)
    grade = st.slider("⭐ Grade", 1, 13, 7)
    condition = st.slider("🔧 Condition", 1, 5, 3)
    waterfront = st.selectbox("🌊 Waterfront", [0, 1])

with col2:
    sqft_living = st.number_input(
        "📐 Living Area (sqft)",
        500,
        10000,
        1800
    )

    sqft_above = st.number_input(
        "🏠 Sqft Above",
        0,
        10000,
        1500
    )

    sqft_basement = st.number_input(
        "⬇ Basement Area",
        0,
        5000,
        300
    )

    sqft_living15 = st.number_input(
        "🏘 Neighborhood Living Area",
        500,
        10000,
        1500
    )

    view = st.slider("👀 View", 0, 4, 0)

st.divider()

# ---------------- LOCATION ----------------
st.subheader("📍 Select Location")

zipcode = st.selectbox(
    "Zipcode",
    sorted(zip_info.index)
)

# Automatically fetch coordinates
lat = zip_info.loc[zipcode, "lat"]
long = zip_info.loc[zipcode, "long"]

st.write(
    f"📍 Latitude: **{lat:.4f}** | Longitude: **{long:.4f}**"
)

st.divider()

# ---------------- PREDICT ----------------
if st.button("💰 Predict House Price"):

    new_house = pd.DataFrame({
        'bedrooms': [bedrooms],
        'bathrooms': [bathrooms],
        'sqft_living': [sqft_living],
        'floors': [floors],
        'waterfront': [waterfront],
        'view': [view],
        'condition': [condition],
        'grade': [grade],
        'sqft_above': [sqft_above],
        'sqft_basement': [sqft_basement],
        'zipcode': [zipcode],
        'lat': [lat],
        'long': [long],
        'sqft_living15': [sqft_living15]
    })

    prediction = model.predict(new_house)

    st.markdown(
        f"""
        <div style="
        background: linear-gradient(135deg,#11998e,#38ef7d);
        padding:35px;
        border-radius:20px;
        text-align:center;
        color:white;
        font-size:35px;
        font-weight:bold;
        box-shadow:0px 0px 20px rgba(0,255,150,0.3);">

        🏡 Estimated House Price

        <br><br>

        ${prediction[0]:,.2f}

        </div>
        """,
        unsafe_allow_html=True
    )

    st.balloons()

st.markdown("---")

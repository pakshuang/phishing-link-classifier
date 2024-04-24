import streamlit as st
import validators

from functions import load_encoder, load_model, load_scaler, preprocess_url

# Load models
encoder = load_encoder("models/encoder_model.pkl")
scaler = load_scaler("models/scaler_model.pkl")
random_forest_model = load_model("models/random_forest_model.pkl")
extra_trees_model = load_model("models/extra_trees_model.pkl")

st.title("Phishing Link Checker")
st.write("This app uses machine learning models to predict whether a URL is legitimate or a phishing link.")
st.write("To view the data dashboard, click [here](https://3vxc23-naman-agrawal.shinyapps.io/shiny_app/)")
url = st.text_input("Enter a URL:")
if st.button("Check URL"):
    if not validators.url(url, skip_ipv6_addr=True, skip_ipv4_addr=True, may_have_port=False):
        st.write("Please enter a valid URL.")
        st.stop()

    if "https://" in url:
        url = url.replace("https://", "")

    # Preprocess the URL
    data = preprocess_url(url, encoder, scaler)

    # Make predictions
    rf_result = random_forest_model.predict(data)
    et_result = extra_trees_model.predict(data)

    st.write("Random Forest Model Prediction:", "Legitimate" if rf_result[0] else "Phishing")
    st.write("Extra Trees Model Prediction:", "Legitimate" if et_result[0] else "Phishing")

import pickle

import pandas as pd
import streamlit as st
import tldextract
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import category_encoders as ce

@st.cache_resource
def load_encoder(path):
    with open(path, 'rb') as f:
        encoder = pickle.load(f)
    return encoder

@st.cache_resource
def load_scaler(path):
    with open(path, 'rb') as f:
        scaler = pickle.load(f)
    return scaler

@st.cache_resource
def load_model(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model

selected_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 37, 41, 42]

def preprocess_url(url, encoder, scaler):
    # Preprocess the URL
    data = pd.DataFrame([url], columns=['url'])
    data['url_length'] = data['url'].apply(len)

    # Add features to capture the proportion of specific characters in the URL
    characters = ["%","&","-",".","/","0","1","2","3","4","5","6","7","8","9", "=", "_", "b", "c", "g", "l", "o", "p", "s", "w", "x"]
    for char in characters:
        data[f"proportion_{char}"] = data['url'].apply(lambda url: url.count(char)/len(url))

    # Add features to indicate whether specific redirection parameters are present in the URL
    redirection_params = ["redirect=", "redirect_uri=", "return=", "returnUrl=", "return_to=", "rurl=", "destination=", "continue=", "next=", "callback=", "url=", "target=", "goto=", "forward=", "redirect_to="]
    for param in redirection_params:
        data[f"contains_{param}"] = data['url'].apply(lambda url: param in url)

    # Extract the domain extension
    data['domain_extension'] = data['url'].apply(lambda url: tldextract.extract(url).suffix)

    # Drop the url column
    data = data.drop(columns=['url'])

    # Encode the domain extension
    data = encoder.transform(data)

    # Scale the features
    data = scaler.transform(data)

    # Select only the columns used in the model
    data = data[:, selected_columns]

    return data
    
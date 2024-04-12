import streamlit as st
import validators

st.title('Phishing Link Checker')
url = st.text_input('Enter a URL to check:')
if st.button('Check URL'):
    if not validators.url(url):
        st.write('Please enter a valid URL.')
        st.stop()
    # Code to predict and display results
    # result = model.predict([url])
    result = True
    st.write('This URL is:', 'Phishing' if result else 'Safe')
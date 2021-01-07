# command : streamlit run main.py

import streamlit as st
from text_cleaning import Text

st.title('Text Cleaning')

st.markdown(
    '<span><i>Cleaning transforms text into a more digestible form so that machine learning algorithms can perform better</i></span>',
    unsafe_allow_html=True)
st.text('')
st.text('')
text = st.text_area('Input your text:')

st.text('')
options = st.multiselect('Select option(s) to perform',
                         ['Remove special characters',
                          'Remove words with length less than 3',
                          'Remove stop words',
                          'Remove hyperlinks',
                          'Expand contractions',
                          'Remove numbers',
                          'Remove repeated characters',
                          'Spelling correction',
                          'Perform lemmatization'
                          ], key='options')

st.text('')
if st.button('Submit', key="submit"):

    return_text = Text().cleaning(text, options)
    import time

    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)

    st.markdown(
        '<b> Output: </b>' + '<span style="color:green; font-size:16px" >' + return_text + '</span>',
        unsafe_allow_html=True)

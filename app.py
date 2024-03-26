from dotenv import load_dotenv
load_dotenv() ## load all hte envinorment variable

import streamlit as st
import os
from PIL import Image
import  PyPDF2 as pdf
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response

def get_gemini_response(input):
    model = genai.GenerativeModel("models/gemini-1.0-pro-001")
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

input_prompt = """
Hey Act like a skilled or very experienced ATS(application tracking stystem)
with a deep understanding of tech field,software engineering,data science,data analysis and big data engineer. Your ask is to evaluate the resume based on the given
job description. You must consider the job market is very competitive and you should provide best assistance for improving their resumes.
Assign the percentage matching based on Job description and the messing keywords with high accuracy

resume:{text}
description: {jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","profile summary":""}}

"""

## Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job description")
uploaded_file = st.file_uploader("Upload your Resume",type="pdf",help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        # ... (Resume text extraction code remains the same)
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))

        # Extract data from the response string 
        response_dict = eval(response)  # Convert the string into a dictionary

        # Format the output nicely
        st.subheader("JD Match:")
        st.write(response_dict["JD Match"])  # Display the JD match percentage

        st.subheader("Missing Keywords:")
        for keyword in response_dict["MissingKeywords"]:
            st.write(keyword)  # Display each missing keyword on a new line

        st.subheader("Profile Summary:")
        st.write(response_dict["profile summary"])  # Display the profile summary
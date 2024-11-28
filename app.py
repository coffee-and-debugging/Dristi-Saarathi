import streamlit as st
from PIL import Image
import pyttsx3
import pytesseract  
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from gtts import gTTS
import tempfile
import config
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

GEMINI_API_KEY = st.secrets["api_keys"]["api_key"]
# GEMINI_API_KEY = config.api_key
llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)
engine = pyttsx3.init()

st.markdown(
    """
    <style>
     .main-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-top: -20px;
        text-decoration: underline;
     }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">दृष्टि सारथी </div>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
        .centered {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            
        }
        MediumSlateBlue
    </style>
    <div class="centered">
        <span style="color:orange">हजुरको </span><span style="color:MediumSlateBlue">साथी</span> <span style="color:orange">अनि </span><span style="color:orange">हजुरको </span> <span style="color:Fuchsia">सहयात्री</span>
    </div>
    """, 
    unsafe_allow_html=True
)
st.sidebar.image(
    r"C:\Users\adhik\Downloads\#LMS\Playground\Langchain\assets\logo\logo.png",
    width=250
)

st.sidebar.title("About App")
st.sidebar.markdown(
    """
    **🔎 Features**
    - **🌄 Describe Image**: Descriptive analysis of an image.
    - **📝 Retrive Text**: OCR to extract the text from an image.
    - **🔊 (TTS) Text-to-Speech**: AI reads text aloud.

    🎲 **How it helps**:
    Helps visually impaired individuals by describing scenes, reading text aloud, and making content more accessible through speech.
    
    🤖 **Powered by**:
    - **Tesseract OCR** for text extraction.
    - **pyttsx3** for text-to-speech.
    - **Gemini-1.5-pro model** for scene understanding.
    """
)

st.sidebar.write(
    "🎯 Instructions:\n"
    "1. Upload an image to start.\n"
    "2. Choose a feature to interact with\n"
    "3. Enjoy the response"
)


def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    tts = gTTS(text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        return tmp_file.name

def generate_scene_description(input_prompt, image_data):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_prompt, image_data[0]])
    output = response.text
    
    if output:
        audio_path = text_to_speech(output)
        return output, audio_path
    return output, None


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")
    

st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

st.markdown("<h3 class='feature-header'>Features:</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

scene_button = col1.button("🌄 Describe Image")
ocr_button = col2.button("📝 Extract Text")
tts_button = col3.button("🔊 Text-to-Speech")

input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
NOTE: you dont have to write (Here is a description of the image for a visually impaired individual)
"""

if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Generating scene description..."):
            description, audio_path = generate_scene_description(input_prompt, image_data)
            st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
            st.write(description)
            if audio_path:
                st.audio(audio_path, format="audio/mp3", start_time=0)
                st.download_button(
                    label="Download Audio",
                    data=open(audio_path, "rb").read(),
                    file_name="scene_description.mp3",
                    mime="audio/mp3"
                )

    if ocr_button:
        with st.spinner("Extracting text from the image..."):
            text = extract_text_from_image(image)
            st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Extracted Text", text, height=150)

    if tts_button:
        with st.spinner("Converting text to speech..."):
            text = extract_text_from_image(image)
            if text.strip():
                audio_path = text_to_speech(text)
                st.success("Conversion Completed!")
                st.audio(audio_path, format="audio/mp3", start_time=0)
                st.download_button(
                    label="Download Speech",
                    data=open(audio_path, "rb").read(),
                    file_name="extracted_text.mp3",
                    mime="audio/mp3"
                )
            else:
                st.warning("No text found to convert.")

st.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Gemini-1.5-pro LLM ⛓️‍💥</strong> | UNIQUE ADHIKARI |</p>
    </footer>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Gemini-1.5-pro LLM<br>⛓️‍💥<br></strong> | UNIQUE ADHIKARI |</p>
    </footer>
    """,
    unsafe_allow_html=True,
)

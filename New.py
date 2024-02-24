import streamlit as st
import openai

openai.api_key='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'
import tempfile
import os
from googletrans import Translator
translator = Translator()

def translate_audio(audio_file):
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(audio_file.name)[1], delete=False) as temp_audio_file:
        temp_audio_file.write(audio_file.read())
        temp_audio_file_path = temp_audio_file.name
        
    with open(temp_audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.translate(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
        segments = transcript["segments"]

        segment_list = []

        for segment in segments:
         start_time = segment["start"]
         end_time = segment["end"]
         text = segment["text"]
         segment_list.append([start_time, end_time, text])
    
    os.unlink(temp_audio_file_path)  # Delete temporary file
    print(segment_list)
    
    return segment_list

# Function to translate text from English to Arabic using Google Translate
def translate_to_arabic(text):
    translator = Translator()
    translated_texts_ar = []
    for j,i in enumerate(text):
     translated_text_ar = translator.translate(i[2], src='en', dest='ar').text
     translated_texts_ar.append([i[0],i[1],translated_text_ar])
    print(translated_texts_ar)
    return translated_texts_ar

# Streamlit UI
def main():
    st.title("Tamil Audio/Video Translation")

    # File upload
    uploaded_file = st.file_uploader("Upload an audio or video file (.mp3, .wav, .mp4, .avi)", type=["mp3", "wav", "mp4", "avi"])
    
    if uploaded_file is not None:
        if uploaded_file.type.startswith('audio/') or uploaded_file.type.startswith('video/'):
            st.audio(uploaded_file, format='audio/mp3')
            
            translation_language = st.selectbox("Select Translation Language:", ["English", "Arabic"])

            if st.button(f"{translation_language} Translation"):
                with st.spinner(f"Translating to {translation_language}..."):
                    if translation_language == "English":
                        transcription = translate_audio(uploaded_file)
                        for i in transcription:
                          st.write("Timestamp: (",i[0],"-", i[1],"): ",i[2])
                    elif translation_language == "Arabic":
                        transcription = translate_to_arabic(translate_audio(uploaded_file))
                        
                        for i,j in enumerate(transcription):
                          st.write("Timestamp: (",j[0],"-", j[1],"): ",j[2])
                    st.success("Translation completed:")
        else:
            st.error("Please upload an audio or video file.")

if __name__ == "__main__":
    main()


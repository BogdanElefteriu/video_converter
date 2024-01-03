import streamlit as st
import shutil
import io
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

import moviepy.editor as moviepy


def convert_to_mp4(file_path):
    print(f"Converting {file_path}")

    clip = moviepy.VideoFileClip(file_path)
    video_with_new_audio = clip.set_audio(moviepy.AudioFileClip(file_path)) 
    video_with_new_audio.write_videofile(f"{file_path.split('.')[0]}.mp4", fps=60, audio_codec="aac")

if not "temp_file" in st.session_state:
    st.session_state['temp_file'] = ''

if not "download" in st.session_state:
    st.session_state['download'] = False

if not "convert" in st.session_state:
    st.session_state['convert'] = False


st.title("Conversie video la formatul MP4")

    
file = st.file_uploader(label="Uploadeaza fisierul")
temporary_location = "temp_conversion.mp4"

if file:
    st.write(f"Ai incarcat fisierul: {file.name}")


if file:
    convert = st.button("Converteste video-ul")
    if st.session_state.download:
        os.remove(temporary_location)
        st.session_state.download = False

    if convert:
        st.session_state.convert = True
        g = io.BytesIO(file.read())  ## BytesIO Object
    
        with open(temporary_location, 'wb') as out:  ## Open temporary file as bytes
            out.write(g.read())  ## Read bytes into file

        # close file
        out.close()

        with st.spinner("Conversia este in curs de procesare..."):
            convert_to_mp4(temporary_location)


tabs =  st.tabs(["Video convertit"])
with tabs[0]:
    if type(file) is not type(None):
        if os.path.exists(temporary_location):
            if st.session_state.convert:
                st.video(temporary_location)

                if st.download_button(label = "Descarca video-ul",
                                        file_name=f"{file.name.split('.')[0]}.mp4",
                                        data = open(temporary_location, "rb")):
                    st.session_state.download = True
                    st.rerun()


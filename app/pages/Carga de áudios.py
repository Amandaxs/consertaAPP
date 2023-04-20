import streamlit as st
import os.path
import pathlib
from pydub import AudioSegment
import pydub
from pathlib import Path

#st.set_page_config(page_icon='🔁')

st.write("""
# Use esta aba para fazer o upload dos áudios!
""")

if st.session_state["authentication_status"] is False:
    st.error('Por favor, volte a página inicial e entre com as credenciais corretas.')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, volte a página inicial e entre com as credenciais corretas.')
elif st.session_state["authentication_status"]:
    #authenticator.logout('Logout', 'main')
    #st.write(f'Welcome *{st.session_state["name"]}*')

    st.write("""
    O modelo foi treinado com os seguintes ruídos:  **Caminhão, Caminhão fora de estrada, Perfuratriz, Escavadeira, Trator Esteira, Peneira e CAT**. Por isso, é necessário que o arquivo enviado como ruído industrial pertença a uma dessas categorias. Também é possível testar o aplicativo com ruídos de comunidade.
    
    """)

    def upload_and_save_wavfiles(save_dir: str) :
        """ limited 200MB, you could increase by `streamlit run foo.py --server.maxUploadSize=1024` """
        uploaded_files = st.file_uploader("Os áudios a serem carregados, devem ter duração de 1 minuto e estarem no formato .wav ou .MP3.  Para enviar mais de um arquivo, utilize a tecla shift.", type=['wav','mp3'] ,accept_multiple_files=True)
        save_paths = []
        for uploaded_file in uploaded_files:
            if uploaded_file is not None:
                if uploaded_file.name.endswith('wav'):
                    audio = pydub.AudioSegment.from_wav(uploaded_file)
                    file_type = 'wav'
                elif uploaded_file.name.endswith('mp3'):
                    audio = pydub.AudioSegment.from_mp3(uploaded_file)
                    file_type = 'mp3'

                save_path = Path(save_dir) / uploaded_file.name
                save_paths.append(save_path)
                audio.export(save_path, format=file_type)
        return save_paths

    def display_wavfile(wavpath):
        audio_bytes = open(wavpath, 'rb').read()
        file_type = Path(wavpath).suffix
        st.audio(audio_bytes, format=f'app/audios/{file_type}', start_time=0)


    files = upload_and_save_wavfiles('app/audios')

    for wavpath in files:
        display_wavfile(wavpath)



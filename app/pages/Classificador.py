import streamlit as st
import os
import pathlib
from os import listdir
from os.path import isfile, join,basename
import classifyer as c
import utils_treat_data as ut
import os
import numpy as np
import matplotlib.pyplot as plt
import os.path
from pathlib import Path
from matplotlib.ticker import FuncFormatter
import streamlit as st
from selenium import webdriver
import pandas as pd
import time
import json
from datetime import datetime
import pathlib
import glob
import sys
sys.path.append(".")
import faker
import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By
import time
import datetime as dt

from selenium import webdriver



st.write("""
# Classificação do ruído selecionado
""")


if st.session_state["authentication_status"] is False:
    st.error('Por favor, volte a página inicial e entre com as credenciais corretas.')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, volte a página inicial e entre com as credenciais corretas.')
elif st.session_state["authentication_status"]:
    #authenticator.logout('Logout', 'main')
    #st.write(f'Welcome *{st.session_state["name"]}*') 

    parent_path = pathlib.Path(__file__).parent.parent.resolve()
    data_path = os.path.join(parent_path, "audios")
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    option = st.sidebar.selectbox('Escolha o ruído a ser classificado', onlyfiles)
    file_location=os.path.join(data_path, option)
    # use `file_location` as a parameter to the main script

    audio_name = os.path.basename(file_location)

    model_name = 'model1500 epochs - 90 batch_size - 0.002 learning_rate - 0.9 beta_1 - 0.999 beta_2 - 0.01 decay(train3).h5'
    pasta = 'app/audios/'
    pasta_salvar_audios = 'app/cutted_audio/'
    src = pasta + audio_name + '.mp3'
    dest = pasta + audio_name + '.wav'

    audio_loc = pasta + audio_name
    ## parameters 
    threshold = 0.7
    max_consec = 50

    ###########
    try:
        ut.adjust_audio_mp3(src,dest)
    except:
        print('not an mp3 file')

    audio = c.get_audio(audio_name, audio_folder = pasta, add_wav = False)

    c.multiple_split(audio =audio,
                    qtde_split = 6,
                    filename_save=audio_name,
                    save_folder = pasta_salvar_audios)

    lista_audios = c.get_audio_split(audio_name = audio_name, folder = pasta_salvar_audios )


    #st.caption(audio_name)

    model = c.get_model(model_name)


    lista_audios = c.get_audio_split(audio_name = audio_name, folder = pasta_salvar_audios )
    consecutives  = c.get_all_predictions_consecutives(model = model, list_of_audios = lista_audios,threshold = threshold, print = False)
    consecutivess = ''.join(str(x) for x in consecutives)
    res = c.second_classifier(consecutives, limit = max_consec)
    if res == 1:
        classific = 'Ruído industrial'
        classificacao = "<span style='color:red'> Ruído industrial </span>"
    else:
        classific = 'Ruído não industrial'
        classificacao = "<span style='color:green'> Ruído não industrial </span>"





    def display_wavfile(wavpath):
        audio_bytes = open(wavpath, 'rb').read()
        file_type = Path(wavpath).suffix
        st.audio(audio_bytes, format=f'audios/{file_type}', start_time=0)

    st.markdown("###  " + 
                classificacao, 
                unsafe_allow_html=True)

    display_wavfile(audio_loc)




    lista_n = []
    for i in lista_audios:
        #st.markdown("- **" + i + "**")
        predictions = c.get_prediction(model = model,filename = i, print=False)
        ll= predictions[0,:,0].tolist()[50:]
        lista_n.append(ll)
        #ax1, ax2 = fig.subplots(2, 1, sharey=True,sharex=True)
        # fig = plt.figure(figsize=[8.4, 1.5]) 
        # ax1 = fig.subplots(1)
        # ax1.plot(ll)
        # ax1.set_ylim([0, 1.05])
        # ax1.set_ylabel('probability')
        #plt.ylabel('Probability')
        # st.pyplot(fig)
        # nn = c.number_of_consecutives(predictions = predictions, threshold = threshold)
        # N_consecutivess = '-'.join(str(x) for x in nn)
        # st.markdown("Especificação de quantidade de pontos consecutivos acima do limiar de " + str(threshold) + " : " + N_consecutivess)
    lista_n = sum(lista_n, [])
    lista_n_rounded = [ round(elem, 2) for elem in lista_n ]





    ###############################################################
    ###############################################################
    option = st.radio("**Você concorda com a classificacão dada pelo modelo?**",
                  ['Sim',
                   'Não'],
                   horizontal=True)
    user_input = st.text_input("**Espaço livre para observações**", "",help="É preciso aperta a tecla enter, para que o texto seja registrado")

    st.text(user_input)

    #st.write('You selected:', option)



    if st.button('enviar resposta', help="Clique aqui para enviar as resposta, isso pode demorar alguns segundos"):
        f = faker.Faker()
        nome = st.session_state["name"]

        url = "https://docs.google.com/forms/d/e/1FAIpQLSeAM5UOdZkDfXVf9jazaBMHgtBzh0AZpNiCs80_wmqORDkemA/viewform?usp=sf_link"
        import os, sys

        #@st.experimental_singleton
        @st.cache_resource
        def installff():
          os.system('sbase install geckodriver')
          os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

        _ = installff()
        from selenium import webdriver
        from selenium.webdriver import FirefoxOptions
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)

        driver.get(url)
        time.sleep(2)

        usuario = driver.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        usuario.send_keys(nome)

        data = driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input' )
        data.send_keys(str(dt.datetime.now()))

        resp = driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input' )
        resp.send_keys(classific)

        tec_concorda = driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input' )
        tec_concorda.send_keys(option)

        observacoes = driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[2]/textarea' )
        observacoes.send_keys(user_input)

        probabilidades = driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input' )
        probabilidades.send_keys(str(lista_n_rounded))

        consecutivos = driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input' )
        consecutivos.send_keys(consecutivess)

        submit = driver.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        submit.click()


        st.write("""Enviado com sucesso""")


################################################################
#################################################################

    if st.checkbox('Ver Detalhes'):
        fig = plt.figure(figsize=[8, 2.5]) 
        ax1 = fig.subplots(1)
        ax1.plot(lista_n)
        ax1.set_ylim([0, 1.05])
        ax1.set_xlim([0,1200])
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        ax1.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0f} seg'.format(x/20)))
        ax1.xaxis.set_major_locator(plt.MaxNLocator(12))
        plt.title('Gráfico da probabilidade do ruído ser industrial ao longo do tempo')
        #ax1.tick_params(axis='x', which='minor', labelsize=10)
        ax1.tick_params(axis='both', which='major', labelsize=8) 
        st.pyplot(fig) 

        st.markdown("**Para que um áudio seja classificado como ruido industrial, é preciso que, por pelos menos 2 segundos, ele apresente uma probabilidade maior que 70%.**") 

        st.markdown("A classificação é feita, separando o áudio carregado em áudios menores de 10 segundos. Nos primeiros instantes de cada áudio menor, o modelo está começando a identificar o padrão e ainda não coloca nenhuma probabilidade associada. Por isso é esperado que a cada 10 segundos haja algumas probabilidades perto de 0.")

        
        # st.markdown("##### O resultado considera um limiar de " + 
        #             str(threshold * 100) + 
        #             """% e uma quantidade de """ +
        #             str(max_consec) +
        #             " valores consecutivos acima do limiar " 
        #             ,unsafe_allow_html=True)
        
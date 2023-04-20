import streamlit as st
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
#import streamlit_authenticator as stauth

#### user authenticator

names = ["testedev","TestesDTI", "TecnicosVale1","TecnicosVale2","TecnicosVale3","TecnicosVale4","TecnicosVale5","TecnicosVale6"]
usernames = ["testedev","TestesDTI", "TecnicosVale1","TecnicosVale2","TecnicosVale3","TecnicosVale4","TecnicosVale5","TecnicosVale6"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

credenciais = {
    "usernames":{
        usernames[0]:{
            "name":names[0],
            "password":hashed_passwords[0]
        },
        usernames[1]:{
            "name":names[1],
            "password":hashed_passwords[1]
        },
        usernames[2]:{
            "name":names[2],
            "password":hashed_passwords[2]
        },
        usernames[3]:{
            "name":names[3],
            "password":hashed_passwords[3]
        },
        usernames[4]:{
            "name":names[4],
            "password":hashed_passwords[4]
        },
        usernames[5]:{
            "name":names[5],
            "password":hashed_passwords[5]
        },
        usernames[6]:{
            "name":names[6],
            "password":hashed_passwords[6]
        },
        usernames[7]:{
            "name":names[7],
            "password":hashed_passwords[7]
        }
    }
}

authenticator = stauth.Authenticate(credentials=credenciais,cookie_name=  "audio_classificator2", key = "abcdef", cookie_expiry_days=7)


name, authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("nome de usuario ou senha incorretos")
if authentication_status == None:
    st.warning("insira seu nome de usuario e senha")
if authentication_status == True:

    st.write("""
    # Classificação de ruídos

    **Este App é destinado a demonstração do modelo de classificação de ruido**



    ### Sobre o modelo e os dados
    * Modelos Utilizados:
        * Rede Neural: Uma rede neural é um método de inteligência artificial que, inspirada pelo cérebro humano, ensina o computador a processar dados e tomar decisões.
        * Modelo lógico: Um modelo lógico consiste num modelo que observa os dados e, através de uma regra estabelecida, toma uma decisão.
    * Como a classificação é feita:
        * A classificação é feita a partir da combinação de dois modelos:
            * Inicialmente, uma rede neural nos dá a probabilidade de termos algum ruído industrial durante vários instantes do tempo.
            * Em seguida o modelo lógico utiliza o resultado da rede neural e classifica como industrial aqueles ruídos que, por pelo menos 2 segundos, apresentem probabilidade maior que 70% de ser um ruído industrial .
    * Ruídos industriais utilizados
        * Os dados que temos atualmente são referentes aos seguintes tipos de ruido idustrial:
            * Caminhão
            * Caminhão fora de estrada
            * Perfuratriz 
            * Escavadeira
            * Trator Esteira
            * Peneira
            * Cat
        * Como o modelo foi treinado com estes dados, espera-se que ele seja capaz de identificar estes ruídos.
        * Caso seja feito o upload de um ruído industrial que esteja fora dos ruídos citados acima, o modelo o classificará como ruído proveniente da comunidade.  
        * Caso hajam outras fontes de ruido industrial, é importante que elas sejam disponibilizadas para que possamos retreinar o modelo para que ele seja capaz de identificá-los e classifica-los como ruído industrial. 
    * Resultado final da Classificação:
        * Ao final de todo o processo da classificação, temos uma classificação binária do ruído como industrial ou não industrial.
        * Os ruídos que estiverem dentro das categorias citadas acima, serão classificados com "Ruído industrial".
        * Os outros ruídos serão classificados como "Ruído não industrial"

        
    ## Instruções para o uso do aplicativo   
    * O upload do arquivo deverá ser feito na aba "Upload de áudios"
    * Na aba "Classificador" os áudios carregador ficarão disponíveis para seleção.
    * Escolha o áudio no seletor presente na barra lateral a esquerda da tela e a classificação do áudio será exibida.
    * Logo abaixo existem dois campos para coleta de feedback.
        * No primeiro deve-se marcar se concorda ou não com a classificação feita pelo modelo.
        * No segundo, caso queira, pode colocar alguma observação sobre o áudio ou a classificação.
    * Após preenchimento dos campos, clique no botão "Enviar resposta" e aguarda a confirmação de que a resposta foi enviada. 
    * É importante frisar que o envio da respósta é de extrema importância para medir o sucesso do modelo desenvolvido.
    * Para ver mais detalhes, como o gráfico gerado pelo modelo, selecione a opção "Ver Detalhes".
    * Para classificar um novo áudio, basta selecioná-lo na barra lateral e seguir os mesmos passos.
        
    """)

    authenticator.logout("Logout","sidebar")
    #st.sidebar.title(f"welcome {name}")

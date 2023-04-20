from keras.models import load_model
import keras
import os
from pydub import AudioSegment
#import math
from td_utils import *
import os
import numpy as np



def get_model(model_name, folder = "dados/models/" ) -> keras.engine.functional.Functional:
    """"
    This function read the previously saved model from the 'models' folder and return thekeras.model object.

    Parameters
    ----------
    model_name:    The name of the model to be loaded.

    folder:        The path to the folder that contains the model, by default, the models are searched in the './models/' folder.

    Returns
    -------

    keras.engine.functional.Functional
    The function returns the keras model, previously saved.
    
    """
    try:
        modelo = load_model( folder + model_name)
        return modelo
    except:
        print("Couldn't load the model, please check the name an if the model is saved in the" + folder  + "folder.")

    

def get_audio(audio_name, audio_folder = 'app/audios/', add_wav = True) :
    """"
    This function read an audio using the pydub package, to extract the audio and transform in an AudioSegment object .

    Parameters
    ----------
    audio_name:    The name of the audio to be classified.

    audio_folder:  he path to the folder that contains the audio to be classified.

    Returns
    -------

    pydub.audio_segment.AudioSegment
    The function returns the AudioSegment object.
    """
    if add_wav == True:
        path_audio = audio_folder + audio_name + '.wav'
        audio = AudioSegment.from_file(path_audio)
        return audio
    else:
        path_audio = audio_folder + audio_name 
        audio = AudioSegment.from_file(path_audio)
        return audio

def get_duration(audio)-> float:
    """"
    This function read an audio and return it's duration in seconds.

    Parameters
    ----------
    audio:    And AudioSegment object.

    Returns
    -------
    float
    The function returns the time of the audio in seconds.
    """
    return audio.duration_seconds 

def single_split(audio,from_min,to_min, split_filename, filename,save_folder):
    """"
    This cut an audio in the time requested, and save in folder.

    Parameters
    ----------
    audio:                  The audio to be cutted.
    from_min:               The second of start.
    to_min:                 The second of the end.
    split_filename:         The name to identify the splitted fil.
    filename:               The name of the audio.
    save_folder:            The path to the folder to save the splitted audio. 
    

    Returns
    -------
    pydub.audio_segment.AudioSegment, str
    an audio object with the cutted audio and the path to te saved audio
    
    """
    t1 = from_min * 60 * 1000
    t2 = to_min * 60 * 1000
    split_audio = audio[t1:t2]
    path_save = save_folder + filename +'_cutted_' + split_filename + '.wav' 
    if get_duration(split_audio) == 10.2:
        split_audio.export(path_save , format = 'wav')
    elif get_duration(split_audio) == 9:
        path_complemento = 'app/ruido_complementar.wav'
        comp = AudioSegment.from_wav(path_complemento)
        split_audio = split_audio + comp
        split_audio.export(path_save , format = 'wav')
    return (split_audio,path_save)



def multiple_split(audio,qtde_split,filename_save,save_folder):
    """"
    get an audio ,split in smaller audios of 10 seconds and save the splitted audios in a specifyed folder. 
    If the as audio have 9 seconds, some background is added in the last one, if the audio hs les then 9 seconds, the smaller audio is is no saved.

    Parameters
    ----------
    audio:              The audio to be cutted .         
    qtde_split:         The maximum quantity of splits of the audio.
    filename_save:      The name of the audio to be included in the split name
    save_folder:        The folder to save the cutted files

    Returns
    -------
    a list of pydub.audio_segment.AudioSegment
    A list with the cutted audios
    """
    audios = list()
    #total_mins = math.ceil(get_duration(audio)/qtde_split)
    for i in range(0,qtde_split):
        split_fn  = '_split_' + str(i)
        begin_time =  0.17 * i  ## O 0.17 indica 10 segundos
        end_time = begin_time +  0.17
        som,filename = single_split(audio,begin_time,end_time,split_fn,filename_save,save_folder)
        audios.append(som)
        #print(get_duration(som))
        
    return audios



def get_audio_split(audio_name, folder):
    """"
    This function get a list of audio files in a folder the have the giver name as part of the name of the file.
    Parameters
    ----------
    audio_name:   The name of the audio to be searched.      
    folder:       The folder that contains the files.
    Returns
    -------
    list
    Return a list with all audio files names that have the given name
    """
    
    word = audio_name + '_cutted_'
    audios = []
    for filename in os.listdir(folder):
        if (filename.endswith("wav")) & (word  in filename):
            audio = folder + filename
            audios.append(audio)
    return audios



#################

def get_prediction(model,filename, print):
    """"
    This function receives the model object and the name of the file to return the predictions.
    The argument 'print', defines if the plot of the prediction will be shown or not. 
    ----------
    model:          The previously trained model.      
    filename:        The name of the file to be analysed by the model.
    print:          True for show the plots.

    Returns
    -------
    list
    Return an array with the predictions
    """
    x = graph_spectrogram(filename)
    # the spectrogram outputs (freqs, Tx) and we want (Tx, freqs) to input into the model
    x  = x.swapaxes(0,1)
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x)
    if print == True:
        plt.subplot(2, 1, 2)
        plt.plot(predictions[0,:,0])
        plt.ylabel('probability')
        plt.show()
    return predictions



############

def number_of_consecutives(predictions, threshold):
    """"
    Get the array of predtions and return the number os consecutive times, that the probability is up to threshold.
    
    ----------
    predictions:      The array of predictions.   
    threshold:        The limiar of probability.


    Returns
    -------
    list
    Return a list with the total of the consecutive steps for each time the probability is up to threshhold
    """
    Ty = predictions.shape[1]
    steps = []
    consecutive_timesteps = 0
    consecutive_timesteps_old = 0
    for i in range(Ty):
        consecutive_timesteps_old = consecutive_timesteps
        if predictions[0,i,0] > threshold:
            consecutive_timesteps += 1
        else: 
            consecutive_timesteps = 0
        if (consecutive_timesteps == 0) & (consecutive_timesteps_old != 0)  :
            steps.append(consecutive_timesteps_old)
        if i == Ty-1:
            steps.append(consecutive_timesteps)
    return steps


############

def get_all_predictions_consecutives(model,list_of_audios,threshold, print = False):
    """"
    Pass over a list of audios, predict them and return the list of lists with th consecutive tim steps in each prediction.
    
    ----------
    model:                  The previously saved models.   
    lis_of_audios:          The lidt of audios to be classified.
    print:                  True for seen the plots


    Returns
    -------
    list
    Return a list with the total of the consecutive steps for each time the probability is up to threshhold
    """
    list = []
    for i in list_of_audios:
        predictions = get_prediction(model,i, print)
        cons = number_of_consecutives(predictions = predictions, threshold = threshold)
        list.append(cons)
    return list



#########################def second_classifier(consecutives, limit):
def second_classifier(consecutives, limit):
    consecutives  = [item for items in consecutives  for item in items]
    if all(v == 0 for v in consecutives):
        print('OnlyZeros')
        resumo = 0
    else:
        print('NonZeros')
        consec = [i for i in consecutives if i != 0] 
        resumo = np.sum(consec)

    print(resumo)

    if resumo >= limit:
        result =  1
    else:
        result = 0

    print(result)
    return(result)
import tweepy
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

consumer_key = 'XRtIm1Mnhk3ktpacwMzeGz1V0'
consumer_secret = 'kQoQpgLNsgGJ5VBPEqs3II92BvjeriXOdLWAVoeoY84t30TNgE'
access_token = '1633497956-vgq9BrDZmihmPPHexldU9oObEchUbhbChonPwYu'
access_token_secret = 'mFA16Mz93Iz4WTcoADchemO8lzPC4SB1fgaamWejkohVA'

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, retry_count=3, retry_delay=5, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def main():
    start_time = time.time()
    if len(sys.argv) > 1:
        num = sys.argv[1]
    else:
        num = 10
    df = pd.read_csv('../gen/nodos_{}noticias.csv'.format(num))
    df = df[df.name != 'SuspendedAccount']
    edgesDict = {}
    total = len(df['name'])
    for i, screen_name in enumerate(df['name']):
        followers = get_followers_page(screen_name)
        edgesDict[screen_name] = str(followers)
        print("{}:\tRestantes: {}\tTiempo Transcurrido: {}".format(i, total-i, time.time() - start_time))
        edges = pd.DataFrame.from_dict(edgesDict,orient='index')
        csv_file = '../gen/edges/intermediates/edges_{}users.csv'.format(i+1)
        edges.to_csv(csv_file)
        follower_csv(csv_file)

    
    edges = pd.DataFrame.from_dict(edgesDict,orient='index')
    edges.to_csv('../gen/edges/edges_1.csv')
    follower_csv('../gen/edges/edges_1_final.csv')
    print("--- %s seconds ---" % (time.time() - start_time))


####    FUNCTIONS    ####

def follower_csv(path):
    df = pd.read_csv(path)
    df = df.rename(columns={"Unnamed: 0": "screen_name", "0": "followers_ids"})
    ids = df['followers_ids'][0]
    ids = ids.split(',')
    for i,v in enumerate(ids):
        ids[i] = v.strip()
    ids[0] = ids[0].replace("[", "")
    ids[-1] = ids[-1].replace("]", "")
    df.to_csv(path)

def save_to_csv(index, name_dict):
    df = pd.DataFrame(list(name_dict.items()), columns=['name', 'weight'])
    df.rename(columns={0:"id"}) #Adding an index column
    df.index.name = "id"
    df.to_csv('../gen/nodos_{}noticias.csv'.format(index))

def get_tweet_status(tweet_id):
    '''
    Devuelve un objeto status con todos los datos de un tweet
    '''
    return api.get_status(tweet_id)

def get_user_by_id(id):
    '''
    Devuelve un objeto user a traves del id del user
    '''
    return api.get_user(id)

def get_screen_name(id):
    try:
        user = get_user_by_id(id)
        screen_name = user.screen_name
        return screen_name
    except tweepy.TweepError as e:
        return ('SuspendedAccount')    
    
    
def get_screen_name_from_tweet(tweet_id):
    try:
        status = api.get_status(tweet_id)
        user = get_user_by_id(status.user.id)
        screen_name = user.screen_name
        return screen_name
    except tweepy.TweepError as e:
        return ('SuspendedAccount')    

def get_followers_page(screen_name):
    '''
    Devuelve los ids de los usuarios que sigue un user, screen_name es el nombre de usuario sin el '@'
    ej @NelsonMandela -> NelsonMandela
    '''
    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
        ids.extend(page)
        time.sleep(30)
    return ids

def get_followers_limited(screen_name, total):
    '''
    Devuelve los ids de los usuarios que sigue un user, screen_name es el nombre de usuario sin el '@'
    ej @NelsonMandela -> NelsonMandela
    Obtiene solo un numero de ids de usuarios indicado en el parametro total
    '''
    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).items(total):
        ids.append(page)
    return ids

def get_followers_from_tweet_id(tweet_id, total = 0):
    '''
    Pasandole el id de un tweet obtenemos todos sus seguidores,
    se le puede pasar el parametro total y obtener solamente un numero concreto de ids
    '''
    user_id = get_tweet_status(tweet_id).user.id
    screen_name = get_user_by_id(user_id).screen_name
    if total == 0:
        followers_ids = get_followers_page(screen_name)
    else:
        followers_ids = get_followers_limited(screen_name,total)
    return followers_ids
    
    

def get_tweets(num_noticias):
    '''
    Le pasamos el numero de noticias de las cuales queremos obtener los tweets_ids
    Con el DataFrame de Pandas separamos los tweets de una misma noticia
    Devuelve un array de [titulos, array(tweets_ids)]
    '''
    df = pd.read_csv('../data/politifact_fake.csv') 
    #Esto se puede cambiar por otro dataset (ej: ../data/politifact_real.csv), pero de momento trabajamos con este
    df['tweet_ids'][0].split('\t')
    
    titulo = []
    tweets = []
    i = 0
    
    for tweet in df['tweet_ids']:
        if i < num_noticias:
            array_tweets = str(tweet).split('\t')
            #Se puede cambiar a que tenga al menos 5 o 10 tweets para probar
            if(len(array_tweets) > 1 and len(array_tweets) < 2000): #Solo si tiene algun tweet lo añadimos, 1 elemento es NaN
                tweets.append(array_tweets)
                titulo.append(df['title'][i])
                i = i+1
    noticias = [titulo, tweets]
    return noticias 

if __name__== "__main__" :
    main()

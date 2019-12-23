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

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def main():
    if get_screen_name_from_tweet('937349434668498944') == "SuspendedAccount":
        exit()

    list_noticias = [1,5,10,20,50,100,366,367,368]
    start_time = time.time()
    noticias = get_tweets(num_noticias=int(sys.argv[1]))
    name_dict = {}

    for i,v in enumerate(noticias[1]):
        if i in list_noticias:
            save_to_csv(i, name_dict)
            print(i,"--- %s seconds ---" % (time.time() - start_time))
        for j, t in enumerate(v):
            name = get_screen_name_from_tweet(str(t))
            if name in name_dict:
                name_dict[name] += 1
            else:
                name_dict[name] = 1
        

    df = pd.DataFrame(list(name_dict.items()), columns=['name', 'weight'])
    df.rename(columns={0:"id"}) #Adding an index column
    df.index.name = "id"
    df.to_csv('./output/nodos_{}noticias.csv'.format(len(noticias[0])))
    print("--- %s seconds ---" % (time.time() - start_time))


####    FUNCTIONS    ####
def save_to_csv(index, name_dict):
    df = pd.DataFrame(list(name_dict.items()), columns=['name', 'weight'])
    df.rename(columns={0:"id"}) #Adding an index column
    df.index.name = "id"
    df.to_csv('./gen/nodos_{}noticias.csv'.format(index))

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
    for page in tweepy.Cursor(api.followers_ids, screen_name="OfeliasHeaven").pages():
        ids.extend(page)
        #time.sleep(60)
    return ids

def get_followers_limited(screen_name, total):
    '''
    Devuelve los ids de los usuarios que sigue un user, screen_name es el nombre de usuario sin el '@'
    ej @NelsonMandela -> NelsonMandela
    Obtiene solo un numero de ids de usuarios indicado en el parametro total
    '''
    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name="OfeliasHeaven").items(total):
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
    df = pd.read_csv('./data/politifact_fake.csv') 
    #Esto se puede cambiar por otro dataset (ej: ./data/politifact_real.csv), pero de momento trabajamos con este
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
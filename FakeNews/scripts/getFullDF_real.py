#Test to check if the df is building correctly
import pandas as pd
import tweepy

consumer_key = 'XRtIm1Mnhk3ktpacwMzeGz1V0'
consumer_secret = 'kQoQpgLNsgGJ5VBPEqs3II92BvjeriXOdLWAVoeoY84t30TNgE'
access_token = '1633497956-vgq9BrDZmihmPPHexldU9oObEchUbhbChonPwYu'
access_token_secret = 'mFA16Mz93Iz4WTcoADchemO8lzPC4SB1fgaamWejkohVA'

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_tweet_status(tweet_id):
    '''
    Devuelve un objeto status con todos los datos de un tweet
    '''
    try:
        return api.get_status(tweet_id)
    except tweepy.TweepError as e:
        f = open("../output/fulldf_logR.txt", "a")
        f.write(str(e))
        f.write('\n')
        f.close()
        return 'SuspendedAccount'

df_out = pd.DataFrame(columns=['tweet_ids','created_at','favorite_count','retweet_count', 'id_noticia', 'index', 'screen_name','user_created_at','followers', 'friends','verified' ])
df = pd.read_csv('../data/politifact_real.csv')
intermediate = [5,10,50,100,200]
index = 0
total = len(df['tweet_ids'])
for i,v in enumerate(df['tweet_ids']):
    if not isinstance(v, float): #Comprueba que tenga mas de 1 elemento, si solo tiene un elemento python lo considera un float
        news = v.split('\t')
    for j in range(len(news)):
        status = get_tweet_status(news[j])
        if len(news) > 1 and status != 'SuspendedAccount': #Si hay mas de un tweet y el tweet no es de una cuenta suspendida lo añadimos al df
            df_out.loc[index] = [str(news[j]), status.created_at.strftime('%Y%m%d%H%M%S'),str(status.favorite_count),str(status.retweet_count),str(df['id'][i]),str(i), str(status.user.screen_name), status.user.created_at.strftime('%Y%m%d%H%M%S'),str(status.user.followers_count), str(status.user.friends_count),str(status.user.verified)]
            index += 1
    print("---- added news {}/{} ----".format(i+1, total))
    if i in intermediate:
        print("--- intermediate step {} ----".format(i))
        df_out.to_csv('../gen/edges/intermediates/full_pf_real_{}.csv'.format(i))

df_out.to_csv('../gen/full_pf_real.csv')
print("All news added, csv generated...")
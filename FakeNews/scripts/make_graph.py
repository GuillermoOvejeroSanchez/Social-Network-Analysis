import pandas as pd

df = pd.read_csv('../gen/full_df_fake.csv',index_col = 0)

news_df = pd.DataFrame(columns=['source','target','created_at_source','created_at_target','news_id'])
#news_df = news_df.append({'source':, 'target':,'created_at':,'news_id':}, ignore_index=True)
n_news = len(df['index'].value_counts())
total = 0
for n in range(n_news):
    df_filtered = df.loc[(df['index'] == n) & (df['retweet_count'] > 0)]
    df_filtered = df_filtered.reset_index()
    if len(df_filtered) < 1000:
        total += len(df_filtered)
        print("Total:{}/{}\tTweets:{}/{}".format(n,n_news,len(df_filtered),total))
        for i in range(len(df_filtered)):
            for j in range(i+1,len(df_filtered)):
                source = str(df_filtered['screen_name'][i])
                target = str(df_filtered['screen_name'][j])
                created_at_s = str(df_filtered['created_at'][i])
                created_at_t = str(df_filtered['created_at'][j])
                news_id = str(n)
                news_df = news_df.append({'source':source, 'target':target,'created_at_source':created_at_s,'created_at_target':created_at_t,'news_id':news_id}, ignore_index=True)

news_df.rename(columns={0:"id"}) #Adding an index column
news_df.index.name = "id"
news_df.to_csv('../gen/grafo_same_news/aristas_noticia_less1000rt.csv')

df_filtered = df.loc[(df['index'] < n_news) & (df['retweet_count'] > 0)]
df_filtered.rename(columns={0:"number"}) #Adding an index column
df_filtered.index.name = "number"
df_filtered.rename(columns={'screen_name':"Id"}, inplace=True) #Adding an index column
df_filtered.to_csv('../gen/grafo_same_news/nodos_aristas_noticia_less1000rt.csv')
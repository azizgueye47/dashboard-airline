import streamlit as st 
import pandas as pd 
import numpy as np
import plotly.express  as px
from wordcloud import WordCloud , STOPWORDS
import matplotlib.pyplot as plt
st.title('Sentiment Analysis of Twitter about US Airline')
st.sidebar.title('Sentiment Analysis of Twitter about US Airline')
st.markdown("This application is a streamlit dashbaorh to Analys sentiment twitter 🐦")
st.sidebar.markdown("This application is a streamlit dashbaorh to Analys sentiment twitter 🐦")

url ="https://raw.githubusercontent.com/satyajeetkrjha/kaggle-Twitter-US-Airline-Sentiment-/master/Tweets.csv"
@st.cache_data(persist=True)
def load_data():
    data=pd.read_csv(url)
    data['tweet_created']=pd.to_datetime(data['tweet_created'])
    return data

data=load_data()

st.sidebar.subheader("Show random tweet")
random_tweet=st.sidebar.radio('sentiment',('positive','neutral','negative'))
st.sidebar.markdown(
    data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0, 0]
)


st.sidebar.markdown("### Number of tweets by sentiment")

select=st.sidebar.selectbox('visualization type ',['Histogram','Pie chart'] ,key='1')
sentiment_count=data['airline_sentiment'].value_counts()
sentiment_count=pd.DataFrame({'Sentiment':sentiment_count.index,'tweet':sentiment_count.values})

if not st.sidebar.checkbox('Hide',True):
    st.markdown("### Number of tweets by sentiment")
    if select=='Histogram' :
        fig=px.bar(sentiment_count,x='Sentiment',y='tweet', color='tweet')
        st.plotly_chart(fig)
    else :
        fig=px.pie(sentiment_count ,values='tweet',names='Sentiment')
        st.plotly_chart(fig)
        
              
data= data.dropna(subset=['tweet_coord'])

# Séparer 'tweet_coord' en 'latitude' et 'longitude'
data[['latitude', 'longitude']] = data['tweet_coord'].str.strip('[]').str.split(',', expand=True)

# Convertir latitude et longitude en valeurs numériques
data['latitude'] = pd.to_numeric(data['latitude'])
data['longitude'] = pd.to_numeric(data['longitude'])

# Supprimer la colonne originale 'tweet_coord'
data.drop(columns=['tweet_coord'], inplace=True)       
        
st.sidebar.subheader('When and Where are user tweet from')
hour =st.sidebar.slider('Hour of day',max_value=23)
modified_data=data[data['tweet_created'].dt.hour==hour]
if not st.sidebar.checkbox('close', value=True,key='5'):
    st.markdown("### tweet location based on the time of day")
    st.markdown("%i tweets beetween %i:00 and %i:00" % (len(modified_data),hour ,(hour+1)%24))
    st.map(modified_data,latitude='tweet_coord')
st.sidebar.subheader('Breakdown airline tweets by sentiment')
choise =st.sidebar.multiselect('Pick airline' ,('US Airways','United','American','Southwest'
                                                ,'Delta','Virgin America'),key=0)

if len(choise):
    choise_data=data[data.airline.isin(choise)]
    fig_choise=px.histogram(choise_data,x='airline' , y='airline_sentiment',
                            histfunc='count',color='airline_sentiment',facet_col='airline_sentiment'
                            ,labels={'airline_sentiment':'tweets'},height=800)
    st.plotly_chart(fig_choise)
    
st.sidebar.header('Word Cloud')
word_sentiment=st.sidebar.radio('Display word cloud for what sentiment ?',('positive','neutral','negative'))
if not st.sidebar.checkbox('Close',True,key='3'):    
    st.header('Word cloud for %s sentiment' % (word_sentiment))
    df=data[data['airline_sentiment']==word_sentiment]
    words=' '.join(df['text'])
    process_word=' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word !='RT'])
    wordcloud=WordCloud(stopwords=STOPWORDS,background_color='white',height=640,width=800).generate(process_word)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(plt)
    
    
    
    
    
    

        
    
        
        
    


import tweepy
import re
from textblob import TextBlob

#token api twitter
api_key = ""
api_secret_key = ""
access_token = ""
access_token_secret = ""

#otentikasi api
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#melakukan pencarian query vaksin, bahasa indo, jumlah 100
hasilSearch = api.search(q="vaksin", lang="id", count=100)

hasilAnalisis = []

#membuang properties yang tdk dibutuhkan
for tweet in hasilSearch:
  tweet_properties = {}
  tweet_properties["tanggal"] = tweet.created_at
  tweet_properties["user"] = tweet.user.screen_name
  tweet_properties["isi"] = tweet.text
  tweet_clean = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet.text).split())

#analisisnya pake textblob  
  analysis = TextBlob(tweet_clean)
#translate ke inggris supaya analisis akurat
  try:
    analysis = analysis.translate(to="en")
#melihat berapa tweet yg error (sudah menggunakan bhs inggris)
  except Exception as e:
    print(e)

#klasifikasi sentiment
  if analysis.sentiment.polarity > 0.0:
    tweet_properties["sentimen"] = "positif"
  elif analysis.sentiment.polarity == 0.0:
    tweet_properties["sentimen"] = "netral"
  else:
   tweet_properties["sentimen"] = "negatif"

#penghapusan retweet (maks rt 1)
  if tweet.retweet_count > 0:
    if tweet_properties not in hasilAnalisis:
      hasilAnalisis.append(tweet_properties)
  else:
    hasilAnalisis.append(tweet_properties)

tweet_positif = [t for t in hasilAnalisis if t["sentimen"]=="positif"]
tweet_netral = [t for t in hasilAnalisis if t["sentimen"]=="netral"]
tweet_negatif = [t for t in hasilAnalisis if t["sentimen"]=="negatif"]

#menampilkan hasil akhir
print("Sentiment Analysis")
print("Positif: ", len(tweet_positif), "({} %)".format(100*len(tweet_positif)/len(hasilAnalisis)))
print("Netral: ", len(tweet_netral), "({} %)".format(100*len(tweet_netral)/len(hasilAnalisis)))
print("Negatif: ", len(tweet_negatif), "({} %)".format(100*len(tweet_negatif)/len(hasilAnalisis)))

#menampilkan isi tweet
tweet_netral


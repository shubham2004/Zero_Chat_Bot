import nltk
import string
pre=''
import speech_recognition as sr
from win32com.client import Dispatch
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import requests
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC984c57e10539ffa913799bf55704c6e8"
# Your Auth Token from twilio.com/console
auth_token  = "ddd376e655b3d55c419d572dc8194da7"
url1 = "http://tinywebdb.appinventor.mit.edu/storeavalue"
counter = 1
croppedResponse = ' '
url = 'http://tinywebdb.appinventor.mit.edu/getvalue'
speak = Dispatch("SAPI.SpVoice")
r = sr.Recognizer()
path='D:\projects\chat.txt'
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from train_general import training_data
corpus_words = {}
class_words = {}
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    class_words[c] = []
for data in training_data:
    for word in nltk.word_tokenize(data['sentence']):
        if word not in ["?", "'s"]:
            stemmed_word = stemmer.stem(word.lower())
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1
            class_words[data['class']].extend([stemmed_word])


def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    for word in nltk.word_tokenize(sentence):
        if stemmer.stem(word.lower()) in class_words[class_name]:
            score += (1 / corpus_words[stemmer.stem(word.lower())])
    return score 
def classify(sentence):
    high_class = None
    high_score = 0
    for c in class_words.keys():
        score = calculate_class_score(sentence, c, show_details=False)
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score
while True:
        while len(croppedResponse) > 0:
            values = {'tag' : counter} 
            data = urllib.parse.urlencode(values).encode("utf-8")
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            the_page = str(response.read())
            separatedResponse = the_page.split(',')
            croppedResponse = separatedResponse[2].strip("']").strip('"').strip("\\")
            croppedResponse = croppedResponse[1:]
            croppedResponse = croppedResponse.lower()
            sentence=croppedResponse
            """if 'call' in sentence:
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                to="+918376048185", 
                from_="+14157662257 ",
                body="Hello from Python!")

                print(message.sid)
            """
            #sentence=input('-')
            if(pre!=sentence):
                answer,prob=classify(sentence)
                print(sentence)
                print(prob)
                print(answer)
                speak.Speak(answer)
                answer=str(answer).replace(' ','-')
                
                pre=sentence
                values = {'tag':'2',
                          'value':answer
                                }
                r = requests.post(url = url1, data = values)
                html = r.content
                print(html)
                 
# 
                

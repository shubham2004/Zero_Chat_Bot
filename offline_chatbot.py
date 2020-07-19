import nltk
import string
import math

#from firebase import firebase
#firebase = firebase.FirebaseApplication('https://jyoti-1836c.firebaseio.com/', None)

pre=''
#import speech_recognition as sr
from win32com.client import Dispatch
counter = 1
croppedResponse = ' '
speak = Dispatch("SAPI.SpVoice")
#r = sr.Recognizer()
path='chat.txt'
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
        #result = firebase.get('/question', None)
        result=input('-')
        sentence=result
        if(pre!=sentence):
            answer,prob=classify(sentence)
            #print(sentence)
            prob=(1/(1+math.exp(-1*prob)))
            if(prob>0.1):
                #print(prob)
                print(answer)
                pre=sentence
            else:
                print("i dont know it yet can suggest some good response to this")
                re=input('-')
                training_data.append({"class":re,"sentence": sentence})

            
           
          

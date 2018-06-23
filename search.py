
import glob
import os
import warnings
import textract
import requests
from flask import (Flask, json, Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from gensim.summarization import summarize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from werkzeug import secure_filename

import pdf2txt as pdf
import PyPDF2


from autocorrect import spell

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'Original_Resumes/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class ResultElement:
    def __init__(self, rank, filename):
        self.rank = rank
        self.filename = filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']




import re, string, unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        # print(word)
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    # words = replace_numbers(words)
    words = remove_stopwords(words)
    words = stem_words(words)
    words = lemmatize_verbs(words)
    return words
def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp

def res(jobfile):
    Final_Array = []
    
    def lcs(X, Y):
        try:
            mat = []
            for i in range(0,len(X)):
                row = []
                for j in range(0,len(Y)):
                    if X[i] == Y[j]:
                        if i == 0 or j == 0:
                            row.append(1)
                        else:
                            val = 1 + int( mat[i-1][j-1] )
                            row.append(val)
                    else:
                        row.append(0)
                mat.append(row)
            new_mat = []
            for r in  mat:
                r.sort()
                r.reverse()
                new_mat.append(r)
            lcs = 0
            for r in new_mat:
                if lcs < r[0]:
                    lcs = r[0]
            return lcs
        except:
            return -9999
    
    def spellCorrect(string):
        words = string.split(" ")
        correctWords = []
        for i in words:
            correctWords.append(spell(i))
        return " ".join(correctWords)
    
    def semanticSearch(searchString, searchSentencesList):
        result = None
        searchString = spellCorrect(searchString)
        bestScore = 0
        for i in searchSentencesList:
            score = lcs(searchString, i)
            print(score , i[0:100])
            print("")
            temp = [score]
            Final_Array.extend(temp)
            if score > bestScore:
                bestScore = score
                result = i
        return result
    
    app.config['UPLOAD_FOLDER'] = 'Original_Resumes/'
    app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']





    Resume_Vector = []
    Ordered_list_Resume = []
    Ordered_list_Resume_Score = []
    LIST_OF_FILES = []
    LIST_OF_FILES_PDF = []
    LIST_OF_FILES_DOC = []
    LIST_OF_FILES_DOCX = []
    Resumes_File_Names = []
    Resumes = []
    Temp_pdf = ''
    os.chdir('./Original_Resumes')
    for file in glob.glob('**/*.pdf', recursive=True):
        LIST_OF_FILES_PDF.append(file)
    for file in glob.glob('**/*.doc', recursive=True):
        LIST_OF_FILES_DOC.append(file)
    for file in glob.glob('**/*.docx', recursive=True):
        LIST_OF_FILES_DOCX.append(file)

    LIST_OF_FILES = LIST_OF_FILES_DOC + LIST_OF_FILES_DOCX + LIST_OF_FILES_PDF
    # LIST_OF_FILES.remove("antiword.exe")
    print("This is LIST OF FILES")
    print(LIST_OF_FILES)

    # print("Total Files to Parse\t" , len(LIST_OF_PDF_FILES))
    print("####### PARSING ########")
    for nooo,i in enumerate(LIST_OF_FILES):
        Ordered_list_Resume.append(i)
        Temp = i.split(".")
        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                print("This is PDF" , nooo)
                with open(i,'rb') as pdf_file:
                    read_pdf = PyPDF2.PdfFileReader(pdf_file)
                    # page = read_pdf.getPage(0)
                    # page_content = page.extractText()
                    # Resumes.extend(Temp_pdf)

                    number_of_pages = read_pdf.getNumPages()
                    for page_number in range(number_of_pages): 

                        page = read_pdf.getPage(page_number)
                        page_content = page.extractText()
                        page_content = page_content.replace('\n', ' ')
                        # page_content.replace("\r", "")
                        Temp_pdf = Temp_pdf + str(page_content)
                        # Temp_pdf.append(page_content)
                        # print(Temp_pdf)
                    Resumes.extend([Temp_pdf])
                    Temp_pdf = ''
                    Resumes_File_Names.append(i)
                    # f = open(str(i)+str("+") , 'w')
                    # f.write(page_content)
                    # f.close()
            except Exception as e: print(e)
        if Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":
            print("This is DOC" , i)
                    
            try:
                a = textract.process(i)
                a = a.replace(b'\n',  b' ')
                a = a.replace(b'\r',  b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
                Resumes_File_Names.append(i)
            except Exception as e: print(e)
                
                    
        if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            print("This is DOCX" , i)
            try:
                a = textract.process(i)
                a = a.replace(b'\n',  b' ')
                a = a.replace(b'\r',  b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
                Resumes_File_Names.append(i)
            except Exception as e: print(e)
        # Resumes.extend(textract.process(i))
        if Temp[1] == "ex" or Temp[1] == "Exe" or Temp[1] == "EXE":
            # print("This is EXE" , i)
            pass


    # print("This is length of Resume Vector : " , len(Resumes))
    # # # print(Resumes[1][0:10])
    # for m , i in enumerate(Resumes):
    #     print("This is m : " , m , i[0][0:100])
    #     print("#######################################################################")



    for m,i in enumerate(Resumes):
        Resumes[m] = nltk.word_tokenize(Resumes[m])
        Resumes[m] = normalize(Resumes[m])
        Resumes[m] = ' '.join(map(str, Resumes[m]))

    jobfile = nltk.word_tokenize(jobfile)
    jobfile = normalize(jobfile)
    jobfile = ' '.join(map(str, jobfile))
    # Resumes2 = np.array(Resumes)

    # Resumes2 = Resumes2.ravel()

    # print(len(Resumes))

    # Resumes = ['microsoft is dumb' , 'google is awesome' , 'facebook is cheater']
    print("This is len Resumes : " , len(Resumes))
    os.chdir('../')
        
    print("#############################################################")
    # a = input("Enter String to Search : ")
    print("\n\n")
    print("Printing Scores of all Resumes...")
    print("\n")
    result = semanticSearch(jobfile, Resumes)
    print("\n")
    print("Printing 1 Best Result.....")
    print("\n")
    print (result)
    print("\n\n")
    print("#########################################################")
    print("#########################################################")
    print("#########################################################")
    print("#########################################################")
    print("\n\n")
    print(Final_Array)
    print("This is len Final_Array : " , len(Final_Array))
    print(Resumes_File_Names)
    print("This is len Ordered_list_Resume : " , len(Resumes_File_Names))
    Ordered_list_Resume = Ordered_list_Resume[1:]
    # print(Ordered_list_Resume)

    Z = [x for _,x in sorted(zip(Final_Array,Resumes_File_Names) , reverse=True)]
    flask_return = []
    # for n,i in enumerate(Z):
    #     print("Rankkkkk\t" , n+1, ":\t" , i)

    for n,i in enumerate(Z):
        # print("Rank\t" , n+1, ":\t" , i)
        # flask_return.append(str("Rank\t" , n+1, ":\t" , i))
        name = getfilepath(i)
        #name = name.split('.')[0]
        rank = n
        res = ResultElement(rank, name)
        flask_return.append(res)
        # res.printresult()
        # print(f"Rank{res.rank+1} :\t {res.filename}")
    return flask_return


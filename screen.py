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


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')




class ResultElement:
    def __init__(self, rank, filename):
        self.rank = rank
        self.filename = filename


def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp


def res(jobfile):
    Resume_Vector = []
    Ordered_list_Resume = []
    Ordered_list_Resume_Score = []
    LIST_OF_FILES = []
    LIST_OF_FILES_PDF = []
    LIST_OF_FILES_DOC = []
    LIST_OF_FILES_DOCX = []
    Resumes = []
    Temp_pdf = []
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
                    # Resumes.append(Temp_pdf)

                    number_of_pages = read_pdf.getNumPages()
                    for page_number in range(number_of_pages): 

                        page = read_pdf.getPage(page_number)
                        page_content = page.extractText()
                        page_content = page_content.replace('\n', ' ')
                        # page_content.replace("\r", "")
                        Temp_pdf = str(Temp_pdf) + str(page_content)
                        # Temp_pdf.append(page_content)
                        # print(Temp_pdf)
                    Resumes.extend([Temp_pdf])
                    Temp_pdf = ''
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
            except Exception as e: print(e)
                    
                
        if Temp[1] == "ex" or Temp[1] == "Exe" or Temp[1] == "EXE":
            print("This is EXE" , i)
            pass



    print("Done Parsing.")



    Job_Desc = 0
    LIST_OF_TXT_FILES = []
    os.chdir('../Job_Description')
    f = open(jobfile , 'r')
    text = f.read()
        
    try:
        tttt = str(text)
        tttt = summarize(tttt, word_count=100)
        text = [tttt]
    except:
        text = 'None'

    f.close()

    vectorizer = TfidfVectorizer(stop_words='english')
    # print(text)
    vectorizer.fit(text)
    vector = vectorizer.transform(text)

    Job_Desc = vector.toarray()
    # print("\n\n")
    # print("This is job desc : " , Job_Desc)

    os.chdir('../')
    for i in Resumes:

        text = i
        tttt = str(text)
        try:
            tttt = summarize(tttt, word_count=100) 
            text = [tttt]
            vector = vectorizer.transform(text)

            aaa = vector.toarray()
            Resume_Vector.append(vector.toarray())
        except:
            pass
    # print(Resume_Vector)

    for i in Resume_Vector:

        samples = i
        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(samples) 
        NearestNeighbors(algorithm='auto', leaf_size=30)

        Ordered_list_Resume_Score.extend(neigh.kneighbors(Job_Desc)[0][0].tolist())

    Z = [x for _,x in sorted(zip(Ordered_list_Resume_Score,Ordered_list_Resume))]
    print(Ordered_list_Resume)
    print(Ordered_list_Resume_Score)
    flask_return = []
    # for n,i in enumerate(Z):
    #     print("Rankkkkk\t" , n+1, ":\t" , i)

    for n,i in enumerate(Z):
        # print("Rank\t" , n+1, ":\t" , i)
        # flask_return.append(str("Rank\t" , n+1, ":\t" , i))
        name = getfilepath(i)
        #name = name.split('.')[0]
        rank = n+1
        res = ResultElement(rank, name)
        flask_return.append(res)
        # res.printresult()
        print(f"Rank{res.rank+1} :\t {res.filename}")
    return flask_return


            



if __name__ == '__main__':
    inputStr = input("")
    sear(inputStr)

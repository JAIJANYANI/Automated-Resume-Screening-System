
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import nltk,re
from nltk.corpus import stopwords


# In[2]:

import os,shutil
import sys
import logging
import six
import pdfminer.settings
pdfminer.settings.STRICT = False
import pdfminer.high_level
import pdfminer.layout
from pdfminer.image import ImageWriter


# In[3]:

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline


# In[4]:

stoplist = stopwords.words('english')
stoplist.append('\n')


# In[5]:

skill=open('skills.txt','r')
#print skill.read()


# In[6]:


dir='textresume'
if os.path.exists(dir):
    shutil.rmtree(dir)
os.mkdir(dir)


# In[7]:

#os.path.basename(os.listdir('mlresume')) 
files_no_ext = [".".join(f.split(".")[:-1]) for f in os.listdir('mlresume')]
print(files_no_ext)


# In[8]:

for f in files_no_ext:
    a=open('textresume/'+f+'.txt','a')
    a.close()


# In[9]:

resume_pdf=os.listdir('mlresume')
resume_txt=os.listdir('textresume')


# In[10]:

def extract_text(files=[], outfile=[],
            _py2_no_more_posargs=None,  # Bloody Python2 needs a shim
            no_laparams=False, all_texts=None, detect_vertical=None, # LAParams
            word_margin=None, char_margin=None, line_margin=None, boxes_flow=None, # LAParams
            output_type='text', codec='utf-8', strip_control=False,
            maxpages=0, page_numbers=None, password="", scale=1.0, rotation=0,
            layoutmode='normal', output_dir=None, debug=False,
            disable_caching=False, **other):
    if _py2_no_more_posargs is not None:
        raise ValueError("Too many positional arguments passed.")
    """if not files:
        raise ValueError("Must provide files to work upon!")"""

    # If any LAParams group arguments were passed, create an LAParams object and
    # populate with given args. Otherwise, set it to None.
    if not no_laparams:
        laparams = pdfminer.layout.LAParams()
        for param in ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow"):
            paramv = locals().get(param, None)
            if paramv is not None:
                setattr(laparams, param, paramv)
    else:
        laparams = None

    imagewriter = None
    if output_dir:
        imagewriter = ImageWriter(output_dir)

    """if output_type == "text" and outfile != "-":
        for override, alttype in (  (".htm", "html"),
                                    (".html", "html"),
                                    (".xml", "xml"),
                                    (".tag", "tag"),
                                 (".txt","text")):
            if outfile.endswith(override):
                output_type = alttype"""

    if outfile == []:
        outfp = sys.stdout
        if outfp.encoding is not None:
            codec = 'utf-8'
    else:
        i=0
        for outfi in outfile:
            fname=files[i]
            i+=1
            outfp = open('textresume/'+outfi, "w")
            
            with open('mlresume/'+fname, "rb") as fp:
                pdfminer.high_level.extract_text_to_fp(fp, **locals())
    return 


# In[44]:



output=extract_text(resume_pdf,resume_txt)


# In[45]:

for f in resume_txt:
    file=open('textresume/'+f,'r+')
    data=file.read()
    data=re.sub(r'[^\x00-\x7F]+',' ', data)
    data=data.replace('\n',' ')
    file.seek(0)
    file.write(data)
    


# In[94]:

skill.seek(0)
cv=CountVectorizer(token_pattern = r"(?u)\b\w+\b",stop_words=stoplist)
cv.fit(skill)


# In[95]:

skill.seek(0)
c=cv.transform(skill)
df=pd.DataFrame( columns=cv.get_feature_names())
s1=pd.DataFrame(c.toarray(), columns=cv.get_feature_names())


# In[96]:

for f in os.listdir('textresume'):
    file = open('textresume/'+f,'r')    
    file.seek(0)
    y=cv.transform(file)
    x=y.toarray().sum(axis=0)
    df.loc[len(df)]=x
print df


# In[97]:


skill.seek(0)
tfv=TfidfVectorizer(token_pattern = r"(?u)\b\w+\b",stop_words=stoplist)
tfv.fit(skill)


# In[98]:

print tfv.get_feature_names()


# In[99]:

skill.seek(0)
y=tfv.transform(skill)


# In[100]:

df2=pd.DataFrame(columns=tfv.get_feature_names())
s2=pd.DataFrame(y.toarray(), columns=tfv.get_feature_names())


# In[101]:

for f in os.listdir('textresume'):
    file = open('textresume/'+f,'r')    
    file.seek(0)
    y=tfv.transform(file)
    x=y.toarray().sum(axis=0)
    df2.loc[len(df2)]=x
print df2


# In[141]:

li=[]
for i in range(0,len(df2)):
    li.append((s2.loc[0]*df2.loc[i]).sum())


# In[143]:

rating=dict(zip(os.listdir('mlresume'),li))
rating=sorted(rating.items(), key=lambda x:x[1])
rating=rating[::-1]
print rating


# In[144]:

from gensim.summarization import summarize


# In[149]:

"""k=open('textresume/resume5.txt','r')
sumz = summarize(k.read())
v=open('sumz1.txt','w')
v.write(sumz)
v.close()"""


# In[154]:

"""a=open('sumz1.txt','r')
c=cv.transform(a)
m=pd.DataFrame(columns=cv.get_feature_names())
m.loc[len(m)]=c.toarray().sum(axis=0)
print m"""


# In[138]:




# In[ ]:




# In[ ]:




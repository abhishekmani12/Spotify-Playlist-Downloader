
#installs with pip

#!pip install beautifulsoup4
#!pip install requests
#!pip install selenium

import pandas as pd
import requests
import urllib.request,sys,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver=webdriver.Chrome(r'C:\Users\Abhis\Desktop\chromedriver_win32\chromedriver.exe')

urls=pd.read_excel(r'C:\Users\Abhis\Desktop\black_coffer\20211030 Test Assignment-20220716T084424Z-001\20211030 Test Assignment\Input.xlsx') #convert input link xlsx to a df

urls.count

url=urls["URL"]

#using selenium to extract data from webpage:

textList=[]

for links in url:
    driver.get(links)
    text=driver.find_elements("xpath",'/html/body/div[6]/article/div[2]/div/div[1]/div/div[2]')
        
    for i in range(len(text)):
        textList.append(text[i].text)

len(textList) #check

textdf= pd.DataFrame(columns=['Text'])

textdf['Text']=pd.DataFrame(textList)

textdf

textdf.to_excel(r'C:\Users\Abhis\Desktop\RawTextFile.xlsx') #converting raw text without title to excel -- change path

#COMBINING title and text content

from urllib.parse import urlparse
import os
import pandas as pd
import re

links=pd.read_excel('/content/Input.xlsx')
text=pd.read_excel('/content/RawTextFile.xlsx')

res=[""]*150
i=0

for urls in (links['URL']):
  parsed=urlparse(urls)
  paths=parsed.path
  res[i]=re.sub('\W',' ',paths) #only characters and numbers
  res[i]=re.sub('\s$',"",res[i]) #Remove whitespace at the end of the string
  res[i]=re.sub('\d$',"",res[i]) #remove digit at the end of the string

  res[i]=res[i] + " " + text["Text"][i] #joining title and raw text
  i+=1

textdf=pd.DataFrame(columns=["Text"])
textdf["Text"]=pd.DataFrame(res)  
textdf.to_excel(r'RawText_with_title.xlsx') #converting to excel -- pls change path


#SENTIMENT ANALYSIS:

import pandas as pd
import nltk
import re

#merging the stopwords txt file

StopWList=[]
filelist=["C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/StopWords/StopWords_Auditor.txt",
          "C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/StopWords/StopWords_Currencies.txt",
          "C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/StopWords/StopWords_DatesandNumbers.txt",
          "C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/StopWords/StopWords_Generic.txt",
          "C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/StopWords/StopWords_GenericLong.txt",
          "C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/StopWords/StopWords_Geographic.txt",
          "C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/StopWords/StopWords_Names.txt"]

for i in range(len(filelist)):
    
    file=open(filelist[i],"r")

    for word in file:
    
        stripped_word=word.strip()
        head, sep, tail = stripped_word.partition('|')
        stopword=re.sub('\s',"",head)
        
        StopWList.append(stopword.lower())

    file.close()

textdf=pd.read_excel('C:/Users/Abhis/Desktop/black_coffer/soln/RawText_with_title.xlsx')

nltk.download('stopwords')
from nltk.corpus import stopwords

#adding custom stopwords list to nltk's stopword
stopword=nltk.corpus.stopwords.words('English')
stopword.extend(StopWList)

nltk.download('punkt')
from nltk.tokenize import word_tokenize

textdf['Text']=textdf['Text'].str.lower()
textdf['Text'] = textdf['Text'].apply(lambda x: re.sub('[^A-Za-z0-9 ]', '', x)) #accepting only numbers and alphabets

#tokenizing

texttokendf=pd.DataFrame(columns=['Tokens'])

final_text=[[]]*150

for i in range(len(textdf)):
    tokens=word_tokenize(textdf['Text'][i])
    final_text[i]=[token for token in tokens if not token in stopword]

len(final_text) #check length

#coverting to df
final_textdf=pd.Series(final_text).to_frame('words') #contains list of words (cleaned), textdf is uncleaned but wihtout special characters

negative_words=[]
positive_words=[]

sentiment_list=[negative_words,positive_words]

#fetching positive and negative words .txt file -- pls change path
filelistsentiment=["C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/MasterDictionary/negative-words.txt",
          "C:/Users/Abhis/Desktop/black_coffer/20211030 Test Assignment-20220716T084424Z-001/20211030 Test Assignment/MasterDictionary/positive-words.txt"]

#converting .txt file to list
for i in range(len(filelistsentiment)):
    
    file=open(filelistsentiment[i],"r")

    for word in file:
    
        stripped_word=word.strip()
        #head, sep, tail = stripped_word.partition('|')
        #stopword=re.sub('\s',"",head)
        
        sentiment_list[i].append(stripped_word)
    file.close()

print(len(negative_words),len(positive_words)) #check len

#loop takes long time hence created intermediate outputdf which has positive and negative count in it
for i in range(len(final_text)):
    #count number of positive words
     pos_count=final_textdf['words'].apply(lambda x: len([w for w in x if w in negative_words]))
    #count number of negative words
     neg_count=final_textdf['words'].apply(lambda x: len([w for w in x if w in positive_words]))

outputdf=pd.read_excel(r'C:\Users\Abhis\Desktop\black_coffer\20211030 Test Assignment-20220716T084424Z-001\20211030 Test Assignment\Input.xlsx') #converting pinput file to df -- pls change path

outputdf['POSITIVE COUNT']=pos_count
outputdf['NEGATIVE COUNT']=neg_count

outputdf

#outputdf.to_excel(r'C:\Users\Abhis\Desktop\Output_with_count.xlsx') #saving progress

#outputdf=pd.read_excel(r'C:\Users\Abhis\Desktop\Output_with_count.xlsx')

#calculating polarity and subjectivity score based on pos and neg count 

totalword_count=[]
for i in range(len(final_textdf)): 
    
    totalword_count.append(len(final_textdf['words'][i]))
    
    polarity_score=(outputdf['POSITIVE COUNT']-outputdf['NEGATIVE COUNT'])/((outputdf['POSITIVE COUNT']+outputdf['NEGATIVE COUNT'])+0.000001)
    
    subjectivity_score=(outputdf['POSITIVE COUNT']+outputdf['NEGATIVE COUNT'])/((totalword_count[i])+0.000001)

print(polarity_score,subjectivity_score) #checking

text_punct=pd.read_excel(r'C:/Users/Abhis/Desktop/black_coffer/soln/RawText_with_title.xlsx') #converting a rawtext data with punctuations to df -- pls change path

text_punct #checking

final_textdf['words'] #checking

#from nltk.corpus import cmudict

#cmudic=cmudict.dict()

sentence_count=[]
word_count=[]
avg_sentence_len=[]
words=[]
complex_count=[]
percent_complex=[]
fog_index=[]
cleanword_count=[]
total_slbl_count=[]
slbl_per_word=[]
pronoun_count=[]
avg_word_len=[]


avg_num_words=[]*150
for i in range(len(textdf)):
    
    #calculating avg sentence length

    lst=text_punct['Text'][i].split('.')
    sentence_count.append(len(lst))
    
    avg_sentence_len.append(sum(len(x.split()) for x in lst) / len(lst))  
    
    #removing none in list to calculate word count

    words=(textdf['Text'][i].split(" "))
    twords=[z for z in words if z]
    
    word_count.append(len(twords))
    
    cleanword_count.append(len(final_textdf['words'][i]))
    
    #calculate avg_num_words

    avg_num_words.append(word_count[i]/sentence_count[i])
    
    complexcount=0
    totalcount=0
    charcount=0
    
    #Calculating Syllables:

    for j in range(len(twords)):
        twords[j] = twords[j].lower()
        count=0
        vowels = "aeiouy"
        if twords[j][0] in vowels:
            count += 1
            
        for index in range(1, len(twords[j])):
            
            if twords[j][index] in vowels and twords[j][index - 1] not in vowels:
                
                count += 1
                
        if twords[j].endswith("e") and not twords[j].endswith("le"):
            count -= 1
            
        if count == 0:
            count += 1

        #calculating count of complex words present:

        if count > 2:
            complexcount+=1
            
        totalcount+=count
        
        #calculating number of charcaters present in a given text list

        charcount+=len(twords[j])
        
    #appending respective counts to their lists

    complex_count.append(complexcount)
    complexcount=0
    
    total_slbl_count.append(totalcount)
    totalcount=0
    
    #calculate avg word length

    avg_word_len.append(charcount/word_count[i])
    charcount=0
    
    #calculate syllable per word:

    slbl_per_word.append(total_slbl_count[i]/word_count[i])
    
    #calculate percentage of complex words

    percent_complex.append(complex_count[i]/word_count[i])
    
    #calculate fog_index

    fog_index.append(0.4 * (avg_sentence_len[i] + percent_complex[i]))
    
    #calculate personal pronouns count:

    pronounRegex = re.compile(r'\bi\b|\bwe\b|\bmy\b|\bours\b|\bus\b')
    pronouns=pronounRegex.findall(textdf['Text'][i])
    pronoun_count.append(len(pronouns))

#checking lengths:
print(len(sentence_count),len(word_count),len(avg_num_words),len(avg_sentence_len),len(complex_count),len(percent_complex), len(fog_index),len(cleanword_count),len(slbl_per_word),len(pronoun_count),len(avg_word_len),len(polarity_score),len(subjectivity_score))

#adding the lists as columns for output.xlsx file

Columns=['POLARITY SCORE','SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS','FOG INDEX','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT','WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS','AVG WORD LENGTH']
Datas=[polarity_score,subjectivity_score,avg_sentence_len,percent_complex,fog_index,avg_num_words,complex_count,word_count,slbl_per_word,pronoun_count,avg_word_len]
len(Columns)

len(Datas)

for column, data in zip(Columns,Datas):
    outputdf[column]=data

foutputdf=outputdf.drop(['Unnamed: 0'], axis=1)
foutputdf.to_excel(r'C:\Users\Abhis\Desktop\Final Output.xlsx') #convert to excel -- pls change path
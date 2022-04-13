#!/usr/bin/env python
# coding: utf-8

# In[36]:


#Veuillez entrer les répertoires des fichiers d'entrée et de sortie.
#Pensez à adapter la regex pour remplacer les caractères spéciaux.(Sinon deux regex sont prévu pour les données FFB et YBH)
#Notez bien que vous pouvez paramétrer le choix des tiers du fichier de sortie, 
#Il suffit de mettre en commentaire (#) les tiers dont vous voulez vous passer dans la dernière cellule.
path_in = ('Répertoire des fichiers d entrées')
path_out = ('Répertoire des fichiers de sortie')
path_LeFFF = ('Répertoire du dictionnaire français LeFFF')


# In[15]:


import pympi
import re
import requests
import pandas as pd
from lang_trans.arabic import buckwalter
from farasa.segmenter import FarasaSegmenter
from farasa.pos import FarasaPOSTagger as tagger
from farasa.stemmer import FarasaStemmer
import os


# In[41]:


list_fichier = []
for filename in os.listdir(path_in):
    if filename.endswith('.eaf'):
        list_fichier.append(filename)
list_fichier


# def get_dict_bruit(list_fichier):
#     list_bruit = []
#     dic_bruit={}
#     for fichier in list_fichier:    
# 
#         fichier = path_in+fichier
#         eafob = pympi.Elan.Eaf(fichier)
# 
#         tier_names = eafob.get_tier_names()
#         for tier_name in tier_names:
#             spk = eafob.get_annotation_data_for_tier(tier_name)
# 
#             def list_tuple (tuple_spk):
#                 list_spk = []
#                 for i in tuple_spk:
#                     x = [i[0], i[1], i[2]]
#                     list_spk.append(x)
#                 return list_spk
# 
#             list_spk = list_tuple(spk)
# 
#             #Référencer  les caractères de la transcription (appliquer sur les fichiers dès le debut)
#             for i in list_spk:
#                 p = re.compile(r'\[(.*?)\]')
#                 c = re.compile(r'\{(.*?)\}')
#                 list_bruit.append(''.join(p.findall(i[2])))
#                 list_bruit.append(''.join(c.findall(i[2])))
# 
#             for i in list_bruit:
#                 x = i.split('/')
#                 x = x[0].lstrip('=!')
#                 x = '#'+x
#                 dic_bruit[x] = '['+i+']'
# 
#     return dic_bruit

# dict_bruit = get_dict_bruit(list_fichier)
# dict_bruit

# #Segmentation en token liste de liste
# #Mettre les caractères en minuscule
# def tokenization (list_spk,dict_bruit):
#     list_token = []
#     for key, value in dict_bruit.items():
#         for i in list_spk:
#             h = i[2]
#             #i[2]=h.lower()
#             i[2] = re.sub(value,key, i[2])
#             list_token.append(i[2].split(" "))
#     return list_token   

# In[42]:


def list_tuple (tuple_spk):
    list_spk = []
    for i in tuple_spk:
        x = [i[0], i[1], i[2]]
        list_spk.append(x)
    return list_spk


# In[43]:


#Segmentation en token liste de liste
#Mettre les caractères en minuscule
def tokenization (list_spk):
    list_token = []
    for i in list_spk:
        h = i[2]
        i[2]=h.lower()
        i[2] = re.sub(r"\[(.*?)\]","#bruit",i[2])
        i[2] = re.sub(r"\{(.*?)\}","#bruit",i[2])
        i[2] = re.sub(r"el-","el",i[2])
        list_token.append(re.split("\s|-", i[2]))
        #ou
        #list_token.append(i[2].split(" "))
    return list_token   


# In[44]:


f = open(path_LeFFF, encoding = 'utf-8')
list_fr = []
for i in f:
    list_fr.append(i.rstrip('\n'))


# In[45]:


#Détection de l'alternance codique (pensez à mettre des exceptions pour les tokens qui existent dans les deux langues).
def detect_fr (list_token):
    list_tokenfr=[]
    for j in list_token:
        list_temp= []
        for i in range(0, len(j)):
            if j[i].startswith("#"):
                list_temp.append(j[i])
            elif j[i] == 'b':
                list_temp.append(j[i])
            elif j[i] == 'bi':
                list_temp.append(j[i])
            elif j[i] == 'fi':
                list_temp.append(j[i])
            elif j[i] == 'fil':
                list_temp.append(j[i])
            elif j[i] == 'inti':
                list_temp.append(j[i])
            elif j[i] == 'ma':
                list_temp.append(j[i])
            elif j[i] == 'haka':
                list_temp.append(j[i])
            elif j[i] == 'li':
                list_temp.append(j[i]) 
            elif j[i] == 'ka':
                list_temp.append(j[i])
            elif j[i] == 'w':
                list_temp.append(j[i])
            elif j[i] == 'ya':
                list_temp.append(j[i])
            elif j[i].startswith("\'"):
                list_temp.append(j[i])
            elif "\'" in j[i]:
                x = j[i].split("\'")
                #x[0] = x[0]+"\'"
                for nbsplit in range(0, len(x)):
                    x[nbsplit] = '#'+x[nbsplit]
                    list_temp.append(x[nbsplit])
            elif j[i] in list_fr:
                j[i] = '#'+j[i]
                #print(j[i])
                list_temp.append(j[i])
            else:
                list_temp.append(j[i])
            #print(j[i])
        list_tokenfr.append(list_temp)
    return list_tokenfr


# #Remplacement de caractères spéciaux FBB
# def regex_FBB (list_spk):
#     list_spk_mod=[]
#     for i in (list_spk):
#         list_temp=[]
#         for lignes in i:
#             lignes = lignes.split(" ")
#             for ligne in range(0, len(lignes)):
#                 if lignes[ligne].startswith('#'):
#                     #print(lignes[ligne])
#                     pass
#                 else:
#                     lignes[ligne] = re.sub(r"ž","j",lignes[ligne])
#                     lignes[ligne] = re.sub(r"ḥ","h",lignes[ligne])
#                     lignes[ligne] = re.sub(r"š","ch",lignes[ligne])
#                     lignes[ligne] = re.sub(r"ԑ","3",lignes[ligne])
#                     lignes[ligne] = re.sub(r"ġ","gh",lignes[ligne])
#                     lignes[ligne] = re.sub(r"đ","th",lignes[ligne])
#                     lignes[ligne] = re.sub(r"ď","th",lignes[ligne])
#                     lignes[ligne] = re.sub(r"ŧ","th",lignes[ligne])
#                     lignes[ligne] = re.sub(r"e|é|è|ê","e",lignes[ligne])
#                     lignes[ligne] = re.sub(r"\-","",lignes[ligne])
#                     lignes[ligne] = re.sub(r"ç","s",lignes[ligne])
#                     lignes[ligne] = re.sub(r"x|×","kh",lignes[ligne])
#                     lignes[ligne] = re.sub(r"ù|ü|û","u",lignes[ligne])
#                     lignes[ligne] = re.sub(r"Ö|ö|Ô|ô|Ò|ò|Õ|õ|Ó|ó","o",lignes[ligne])
#                     lignes[ligne] = re.sub(r"à|â|ä","a",lignes[ligne])
#                     lignes[ligne] = re.sub(r"ï|î","i",lignes[ligne])
#                     lignes[ligne] = re.sub(r"\'","",lignes[ligne])
#                     lignes[ligne] = re.sub(r"à","a",lignes[ligne])
#                 list_temp.append(' '.join(lignes))
#         list_spk_mod.append(list_temp)
#     return list_spk_mod

# In[46]:


#Remplacement de caractères spéciaux YBA
def regex_YBA (list_spk):
    list_spk_mod=[]
    for i in (list_spk):
        list_temp=[]
        for lignes in i:
            lignes = lignes.split(" ")
            for ligne in range(0, len(lignes)):
                if lignes[ligne].startswith('#'):
                    #print(lignes[ligne])
                    pass
                else:
                    lignes[ligne] = re.sub(r"ṛ","r",lignes[ligne])
                    lignes[ligne] = re.sub(r"ž","j",lignes[ligne])
                    lignes[ligne] = re.sub(r"ḥ","h",lignes[ligne])
                    lignes[ligne] = re.sub(r"š","ch",lignes[ligne])
                    lignes[ligne] = re.sub(r"ԑ","3",lignes[ligne])
                    lignes[ligne] = re.sub(r"ġ","gh",lignes[ligne])
                    lignes[ligne] = re.sub(r"ṭ","t",lignes[ligne])
                    lignes[ligne] = re.sub(r"đ|ḍ","th",lignes[ligne])
                    lignes[ligne] = re.sub(r"ď","th",lignes[ligne])
                    lignes[ligne] = re.sub(r"ŧ","th",lignes[ligne])
                    lignes[ligne] = re.sub(r"e|é|è|ê","e",lignes[ligne])
                    lignes[ligne] = re.sub(r"\-","",lignes[ligne])
                    lignes[ligne] = re.sub(r"ç|ṣ","s",lignes[ligne])
                    lignes[ligne] = re.sub(r"x|×","kh",lignes[ligne])
                    lignes[ligne] = re.sub(r"ù|ü|û","u",lignes[ligne])
                    lignes[ligne] = re.sub(r"Ö|ö|Ô|ô|Ò|ò|Õ|õ|Ó|ó","o",lignes[ligne])
                    lignes[ligne] = re.sub(r"à|â|ä","a",lignes[ligne])
                    lignes[ligne] = re.sub(r"ï|î","i",lignes[ligne])
                    lignes[ligne] = re.sub(r"\'","",lignes[ligne])
                    lignes[ligne] = re.sub(r"\'","",lignes[ligne])
                    lignes[ligne] = re.sub(r"à","a",lignes[ligne])
                list_temp.append(' '.join(lignes))
        list_spk_mod.append(list_temp)
    return list_spk_mod


# In[47]:


arabic = 'ar-t-i0-und'

import http.client
import json

def request(input, itc):
    conn = http.client.HTTPSConnection('inputtools.google.com')
    conn.request('GET', '/request?text=' + input + '&itc=' + itc + '&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=test')
    res = conn.getresponse()
    return res

def driver(input, itc):
    output = ''
    if ' ' in input:
        input = input.split(' ')
        for i in input:
            res = request(input = i, itc = itc)
            res = res.read()
            if i==0:
                output = str(res, encoding = 'utf-8')[14+4+len(i):-31]
            else:
                output = output + ' ' + str(res, encoding = 'utf-8')[14+4+len(i):-31]
    else:
        res = request(input = input, itc = itc)
        res = res.read()
        output = str(res, encoding = 'utf-8')[14+4+len(input):-31]
    return output
    
def translitteration (list_spk_mod):
    list_spk_trans = []
    for ligne in list_spk_mod:
        list_temp = []
        #print(ligne)
        for mot in ligne:
            if mot.startswith('#'):
                list_temp.append(mot.lstrip('#'))
            else:
                x = driver(mot, arabic)
                list_temp.append(str(x))
        list_spk_trans.append(list_temp)
        #print(list_temp)

    return list_spk_trans


# In[48]:


def delBruit(list_spk_trans):
    for phrase in list_spk_trans:
        while "#bruit" in phrase:
            phrase.remove('#bruit')
    return list_spk_trans


# In[25]:


segmenter = FarasaSegmenter(interactive=True)
parser = tagger(interactive=True)
stemmer = FarasaStemmer(interactive=True)


# In[49]:


def seg(list_spk_trans):
    list_spk_seg = []
    for phrase in list_spk_trans:
        seg = segmenter.segment(' '.join(phrase))
        list_spk_seg.append(seg)
    return list_spk_seg


# In[50]:


def POStag(list_spk_trans):
    list_spk_parsed = []
    for phrase in list_spk_trans:
        pos_tagged = parser.tag(' '.join(phrase))
        list_spk_parsed.append(pos_tagged)
    return list_spk_parsed


# In[51]:


def POStag(list_spk_trans):
    list_spk_parsed = []
    for phrase in list_spk_trans:
        pos_tagged = parser.tag(' '.join(phrase))
        list_spk_parsed.append(pos_tagged)
    return list_spk_parsed


# In[52]:


def lemmatization(list_spk_trans):
    list_spk_stemmed = []
    for phrase in list_spk_trans:
        lemmes = stemmer.stem(' '.join(phrase))
        list_spk_stemmed.append(lemmes)
    return list_spk_stemmed


# In[53]:


def edit_content2(list_spk_parsed, list_spk):
    list_POS = []
    list_token = []
    list_text = []

    for ligne, text in zip(list_spk_parsed, list_spk):
        #list_text_temp = []
        list_POS_temp = []
        list_token_temp = []
        list_token_fr_temp = []

        ligne = re.sub("S/S","",ligne)
        ligne = re.sub("E/E","",ligne)
        ligne = ''.join(ligne)
        ligne = re.sub(r"\s\+","+",ligne)
        ligne = re.sub(r"\+\s","+",ligne)
        ligne = re.sub(r"\s\\s","+",ligne)

        #remplacer les faux départs xxx() par XXX~, la pos par X  
        ligne = re.sub(r" \(/PUNC \)/PUNC","؛",ligne)
        l = ligne.split(" ")
        
        
        for i in list_spk:
            h = i[2]
            i[2]=h.lower()
            i[2] = re.sub(r"\[(.*?)\]","#bruit",i[2])
            i[2] = re.sub(r"el-","el",i[2])
            list_text.append(re.split("\s|-|'", i[2]))
        '''
        for i in list_text:
            for j in i:
                while '' in j:
                    i.remove(j)
        '''
        while '' in l:
            l.remove('')
        while '' in list_text:
            list_text.remove('')

        for i in l:
            POS = re.sub(r"[\u0600-\u06FF\/a-z\?]+","",i)
            TOKEN = re.sub(r"[A-Z\-\/a-z]+","",i)
            TOKEN_fr = re.sub(r"[\u0600-\u06FF\/A-Z\?\-\+]+","",i)
            POS = POS.rstrip("+")
            TOKEN = TOKEN.rstrip("+")
            POS = POS.lstrip("+")
            TOKEN = TOKEN.lstrip("+")
            
            list_POS_temp.append(POS)
            list_token_temp.append(TOKEN)
            list_token_fr_temp.append(TOKEN_fr)

        if len(list_POS_temp) != len(list_token_temp):
            print('error')

        for fr, ar in zip(list_token_fr_temp, list_token_temp):
            if fr != '':
                list_token_temp[list_token_temp.index(ar)] = fr

        list_POS.append(list_POS_temp)
        list_token.append(list_token_temp)

    return list_token, list_POS, list_text
    
    


# In[54]:


def parse_foreign(list_token, list_POS):
    import spacy
    nlp = spacy.load("fr_core_news_sm")

    for list_tokens, list_poss in zip(list_token, list_POS):
        for token, pos in zip(list_tokens, list_poss):
            if token == 'l' or token == 'd' or token == 'c' or token == 's' or token == 'qu' or token == 'm' or token == 't' or token == 'n':
                token_annot = token+"\'"
                token = token+"e"

            if 'FOREIGN' in pos:

                doc = nlp(token)

                for mot in doc:
                    pos_ = mot.pos_
                    '''
                    print(mot.text) 
                    print(mot.lemma_)
                    print(mot.pos_)
                    print(' ')
                    '''
                list_poss[list_poss.index(pos)] = pos_
        list_POS[list_POS.index(list_poss)] = list_poss
    
    return list_token, list_POS


# In[55]:


def listToTuple (list_token):
    # reconversion sous la forme de liste de tuple
    content = []
    for i in list_token:
        tuple_ = (i[0], i[1], i[2])
        content.append(tuple_)
    return content

def make_content(list_token, list_POS, list_lemma, list_spk, list_text):
    POS_content = []
    token_content = []
    lemma_content = []
    text_content = []
    
    for token, pos, lemma, times, text in zip(list_token, list_POS, list_lemma, list_spk, list_text):
        t = ' '.join([str(unit) for unit in token])
        token_content.append([int(times[0]), int(times[1]), t])
        
        p = ' '.join([str(unit) for unit in pos])
        POS_content.append([int(times[0]), int(times[1]), p])
        
        lemma_content.append([int(times[0]), int(times[1]), lemma])
        
        text_content.append([int(times[0]), int(times[1]), text])
    
    for i in list_spk:
        if i[2]=='':
            list_spk.remove(list_spk[list_spk.index(i)])
            
    for i, j, k, l in zip(token_content, POS_content, lemma_content, text_content):
        if i[0]>i[1]:
            end = i[0]
            start = i[1]
            token_content[token_content.index(i)][0] = start
            token_content[token_content.index(i)][1] = end
        if j[0]>j[1]:
            end = j[0]
            start = j[1]
            POS_content[POS_content.index(j)][0] = start
            POS_content[POS_content.index(j)][1] = end
        if k[0]>k[1]:
            end = k[0]
            start = k[1]
            lemma_content[lemma_content.index(k)][0] = start
            lemma_content[lemma_content.index(k)][1] = end
        if l[0]>l[1]:
            end = l[0]
            start = l[1]
            text_content[text_content.index(l)][0] = start
            text_content[text_content.index(l)][1] = end        
        
        if i[0]==i[1] and i[2]=='':
            token_content.remove(token_content[token_content.index(i)])
        if i[0]==i[1]:
            token_content.remove(token_content[token_content.index(i)])
            
        if j[0]==j[1] and j[2]=='':
            POS_content.remove(POS_content[POS_content.index(j)])
        if j[0]==j[1]:
            POS_content.remove(POS_content[POS_content.index(j)])
            
        if k[0]==k[1] and k[2]=='':
            lemma_content.remove(lemma_content[lemma_content.index(k)])
        if k[0]==k[1]:
            lemma_content.remove(lemma_content[lemma_content.index(k)])
            
        if l[0]==l[1] and l[2]=='':
            text_content.remove(text_content[text_content.index(l)])
        if l[0]==l[1]:
            text_content.remove(text_content[text_content.index(l)])
        
        if i[2]=='':
            token_content.remove(token_content[token_content.index(i)])
        if j[2]=='':
            POS_content.remove(POS_content[POS_content.index(j)])
        if k[2]=='':
            lemma_content.remove(lemma_content[lemma_content.index(k)])
        if l[2]=='':
            text_content.remove(text_content[text_content.index(l)])
            
    '''
    for i, j, k, l in zip(token_content, POS_content, lemma_content, text_content):
        if i[2]=='':
            token_content[token_content.index(i)][2] = 'vide'
        if j[2]=='':
            POS_content[POS_content.index(j)][2] = 'vide'
        if k[2]=='':
            lemma_content[lemma_content.index(k)][2] = 'vide'
        if l[2]=='':
            text_content[text_content.index(l)][2] = 'vide'
    '''
    for i in text_content:
        i[2] = ' '.join(i[2])
    
    token_content = listToTuple(token_content)
    POS_content = listToTuple(POS_content)
    lemma_content = listToTuple(lemma_content)
    text_content = listToTuple(text_content)
    
    return token_content, POS_content, lemma_content, text_content


# In[56]:


def detect_error(text_content, token_content, POS_content, list_spk_parsed):
    error_content = []
    
    for i, j, h, k in zip(text_content, token_content, POS_content, list_spk_parsed):
        list_error_temp = []
        
        if len(i[2].split(' ')) != len(h[2].split(' ')):
            if len(i[2].split(' ')) > len(j[2].split(' ')):
                list_error_temp.append(i[0])
                list_error_temp.append(i[1])
                list_error_temp.append('error latin')
                error_content.append(list_error_temp)
            elif len(i[2].split(' ')) < len(j[2].split(' ')):
                list_error_temp.append(i[0])
                list_error_temp.append(i[1])
                list_error_temp.append('error transliteration')
                error_content.append(list_error_temp)   
        '''
        else:
            list_error_temp.append(i[0])
            list_error_temp.append(i[1])
            list_error_temp.append('')
        '''
        token_content = listToTuple(token_content)
    return error_content


# In[57]:


def make_sent_id(text_content):
    list_sent_id = []
    count = 0
    for i in text_content:
        if i[2]!='':
            list_temp = []
            count+=1
            sent_id = fichier.rstrip('A.eaf')+tier_name+'_'+str(count)
            list_temp.append(i[0])
            list_temp.append(i[1])
            list_temp.append(sent_id)
            list_sent_id.append(list_temp)

    sent_id_content = listToTuple(list_sent_id)
    return sent_id_content


# In[58]:


def annotation(tierName, content):
    eafob.add_tier(tierName)
    for i in content:
        t1 = int(i[0])
        t2 = int(i[1])
        value = str(i[2])
        eafob.add_annotation(tierName, t1, t2, value)


# In[59]:


for fichier in list_fichier:
    print('')
    print(fichier)
    fichier_in = path_in + fichier
    eafob = pympi.Elan.Eaf(fichier_in)

    tier_names = eafob.get_tier_names()
    print(list(tier_names))
    
    for tier_name in list(tier_names):
        if tier_name.startswith('#')== False:
            spk = eafob.get_annotation_data_for_tier(tier_name)

            list_spk = list_tuple(spk)

            list_spk_token = tokenization(list_spk)

            #list_trans_fr&ar

            list_spk_token_fr = detect_fr(list_spk_token)
            print(tier_name, ' ok: detect_fr')

            #list_spk_mod = regex_FBB(list_spk_token_fr)
            
            list_spk_mod = regex_YBA(list_spk_token_fr)
            print(tier_name, ' ok: regex')
            
            list_spk_trans = translitteration(list_spk_mod)
            print(tier_name, ' ok: transliteration')

            #list_spk_trans = delBruit(list_spk_trans)

            list_spk_parsed = POStag(list_spk_trans)
            print(tier_name, ' ok: parser')

            list_spk_stemmed = lemmatization(list_spk_trans)
            print(tier_name, ' ok: stemmer')

            #list_token, list_POS = edit_content(list_spk_parsed, list_spk_seg)

            list_token, list_POS, list_text = edit_content2(list_spk_parsed, list_spk)
            print(tier_name, ' ok: edit_content')

            list_token, list_POS = parse_foreign(list_token, list_POS)
            print(tier_name, ' ok: spacy')

            token_content, POS_content, lemma_content, text_content = make_content(list_token, list_POS, list_spk_stemmed, list_spk, list_text)
            print(tier_name, ' ok: make_content')

            error_content = detect_error(text_content, token_content, POS_content, list_spk_parsed)
            
            sent_id_content = make_sent_id(text_content)

            list_ = []
            annotation(tier_name+"_sent_id", sent_id_content)
            annotation(tier_name+"_trans", token_content)
            annotation(tier_name+"_trans_seg", list_)
            annotation(tier_name+"_trans_seg_eval", list_)
            annotation(tier_name+"_POS", POS_content)
            annotation(tier_name+"_POS_seg", list_)
            annotation(tier_name+"_POS_seg_eval", list_)
            annotation(tier_name+"_lemma", lemma_content)
            annotation(tier_name+"_word_based", text_content)       
            annotation(tier_name+"_word_based_seg", list_)
            annotation(tier_name+"_errors", error_content)
        
    fichier = fichier.rstrip(".eaf")
    fichier_out = path_out+fichier
    fichier_out = fichier_out.rstrip(".eaf")
    print(fichier_out)
    
    pympi.Elan.to_eaf(fichier_out+"_annot.eaf", eafob, pretty=True)


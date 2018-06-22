
# coding: utf-8

# In[58]:


import twint
import os
import pandas as pd
import tweepy
import sqlite3
import gensim
import numpy as np
import time
import random
import secrets
import itertools
import re
import requests
from bs4 import BeautifulSoup as bs


# ### PARAMETERS

# In[42]:


maxday=5   #maksimum hari yang di reply.
person_to_follow = 3    #jumlah orang yg di follow


# In[43]:



# In[44]:


import datetime
def is_today(date):
    ckdt = datetime.datetime.strptime(date,'%Y-%m-%d').date()
    if ckdt == datetime.datetime.today().date():
        return True
    return False

def daydiff(date1,date2):
    d0 = datetime.datetime.strptime(date1,'%Y-%m-%d').date()
    d1 = datetime.datetime.strptime(date2,'%Y-%m-%d').date()
    delta = d1 - d0
    return delta.days


# In[45]:


# Configure
def twit_get_username(username,result='result.csv',limit=10,count=10):
    try:
        os.remove(result)
    except Exception as e:
        pass

    c = twint.Config()
    #c.Search = "#maling"
    c.Username= username
    c.Format = ""
    c.Debug = False
    c.Store_csv = True
    # CSV Fieldnames
    #following should be used as fieldnames in a list:
    #id,date,time,timezone,user_id,username,tweet,replies,retweets,likes,hashtags,link
    #c.Custom_csv = ["id", "user_id", "username", "tweet"]
    c.Output = result
    c.Limit=limit
    c.Count=count
    # Run
    twint.Search(c)

    df = pd.read_csv(result)
    return df

def user_follower(username,result='result.csv'):
    try:
        os.remove(result)
    except:
        pass

    c = twint.Config()
    #c.Search = "#maling"
    c.Username= username
    c.Format = ""
    c.Debug = False
    c.Store_csv = True
    # CSV Fieldnames
    #following should be used as fieldnames in a list:
    #id,date,time,timezone,user_id,username,tweet,replies,retweets,likes,hashtags,link
    #c.Custom_csv = ["id", "user_id", "username", "tweet"]
    c.Output = result
    # Run
    output = twint.run.Followers(c)

    df = pd.read_csv(result)
    return df

def user_following(username,result='result.csv'):
    try:
        os.remove(result)
    except:
        pass

    c = twint.Config()
    #c.Search = "#maling"
    c.Username= username
    c.Format = ""
    c.Debug = False
    c.Store_csv = True
    # CSV Fieldnames
    #following should be used as fieldnames in a list:
    #id,date,time,timezone,user_id,username,tweet,replies,retweets,likes,hashtags,link
    #c.Custom_csv = ["id", "user_id", "username", "tweet"]
    c.Output = result
    # Run
    output = twint.run.Following(c)

    df = pd.read_csv(result)
    return df


# ### Connect DB & Routines

# In[46]:


# Create a database in RAM
db = sqlite3.connect(':memory:')
# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect('mydb-tweet')

# Get a cursor object
#cursor = db.cursor()
#cursor.execute('''
#    CREATE TABLE following(id INTEGER PRIMARY KEY, username TEXT,
#                       following TEXT)
#''')
#db.commit()

def db_insert_follower(username, follower_list):
    cursor = db.cursor()
    # Insert user 1
    for i in range(len(follower_list)):
        follower=follower_list[i]
        cursor.execute('''INSERT INTO follower(username, follower)
                          VALUES(?,?)''', (username, follower))
    db.commit()
    
def db_insert_following(username, following_list):
    cursor = db.cursor()
    # Insert user 1
    for i in range(len(following_list)):
        following=following_list[i]
        cursor.execute('''INSERT INTO following(username, following)
                          VALUES(?,?)''', (username, following))
    db.commit()

def db_get_follower(username):
    cursor = db.cursor()
    cursor.execute('''SELECT username, follower FROM follower WHERE username=?''',(username,))
    #user1 = cursor.fetchone() #retrieve the first row
    #print(user1[1]) #Print the first column retrieved(user's name)
    all_rows = cursor.fetchall()
    for row in all_rows:
        # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1}'.format(row[0], row[1]))

def db_get_following(username):
    cursor = db.cursor()
    cursor.execute('''SELECT username, following FROM following WHERE username=?''',(username,))
    #user1 = cursor.fetchone() #retrieve the first row
    #print(user1[1]) #Print the first column retrieved(user's name)
    all_rows = cursor.fetchall()
    for row in all_rows:
        # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1}'.format(row[0], row[1]))

def update():
    # Update user with id 1
    newphone = '3113093164'
    userid = 1
    cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',
     (newphone, userid))

def db_del_follower(username):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM follower WHERE username = ? ''', (username,))
    db.commit()

def db_del_following(username):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM following WHERE username = ? ''', (username,))
    db.commit()


# In[47]:


def db_is_replied(msg_id):
    cursor = db.cursor()
    cursor.execute('''SELECT msg_id, my_id FROM replymsg WHERE msg_id=?''',(msg_id,))
    msg1 = cursor.fetchone() #retrieve the first row
    if msg1:
        return True
    else:
        return False

def db_user_follower_data(user_id):
    cursor = db.cursor()
    cursor.execute('''SELECT follower FROM follower WHERE username=?''',(user_id,))
    msg1 = cursor.fetchone() #retrieve the first row
    if msg1:
        return True
    else:
        return False

def db_user_following_data(user_id):
    cursor = db.cursor()
    cursor.execute('''SELECT following FROM following WHERE username=?''',(user_id,))
    msg1 = cursor.fetchone() #retrieve the first row
    if msg1:
        return True
    else:
        return False

def db_replied_this_id(msg_id,my_id):
    cursor = db.cursor()
    cursor.execute('''INSERT INTO replymsg(msg_id,my_id)
                    VALUES(?,?)''',(msg_id,my_id))
    db.commit()


# ### Routine Logic - tweepy

# In[48]:


def twp_update_status(msg):
    try:
        api.update_status(msg)
        print("Update status to:",msg)
    except Exception as e:
        print("error updating status:",e)
        
def twp_reply_post(msg,replyID):
    try:
        rets = api.update_status(msg, in_reply_to_status_id=replyID)
        print("Update status to:",msg)
        return rets
    except Exception as e:
        print("error updating status:",e)
        
def twp_cool_post(msg, username, userfollower):
    res = twit_get_username(username)
    msgid = res.iloc[postnum].id
    #username = res.iloc[postnum]
    follower = user_following(userfollower)
    import random
    follist = follower['GundalaPutraTop'].values.tolist()
    random.shuffle(follist)
    mention = "@"+follist[0]+" @"+follist[1]+" @"+follist[2]
    msge = str("@")+str(username)+" "+str(msg)+" "+str(mention)
    print("Pesan:",msge, "replyto:",msgid)
    api.update_status(msge, msgid)

def twp_follow(UserIDs):
    for userID in UserIDs:
        try:
            api.create_friendship(userID)
            print("Try to follow:", userID)
        except Exception as e:
            print(e)
            continue


# # Routine BOT - AI

# In[66]:


import keras
import nltk

num_features=300
maxsent=10
w2vmodel="chat_model1-300.w2v"   #filename
tex2vec =  gensim.models.KeyedVectors.load(w2vmodel)

model = keras.models.load_model("model-ep2-100.mdl")

def pred(sentence):
    predictions=model.predict(np.array([swv_ar(twl(sentence))]))
    result=decode(predictions)
    print(result)
    return result

#[tex2vec.most_similar([predictions[0][i]])[0] for i in range(maxsent)]


def remove_unchar(flist):
    try:
        flist.remove("?")
    except:
        pass

def twl(sentence, rempunct=True, flat=True):
    """Tokenize word dari sebuah sentence/kalimat"""
    if not flat:
        sntoken = nltk.sent_tokenize(sentence)
    else:
        sntoken = [sentence]
    for i in range(len(sntoken)):
        tokens = nltk.word_tokenize(sntoken[i])
        if rempunct==True:
            type(tokens)
            text = nltk.Text(tokens)
            type(text)  
            sntoken[i] = [w.lower() for w in text if w.isalpha()]
        else: sntoken[i] = tokens
    if len(sntoken)==1: 
        sntoken = sntoken[0]
        remove_unchar(sntoken)
    for i in sntoken:
        remove_unchar(i)
    if sntoken==[]: sntoken=['yang']
    #print(sntoken)
    return sntoken

def zerolistmaker(n):
    """Membuat list berisi 0, mirip seperti np.zeros"""
    listofzeros = [1] * n
    return listofzeros



def swv_ar(sentence, maxword=maxsent, vecsize=num_features, frontpad=True):
    """Sentence word2vec to array matrices for processing"""
    senarray=[]
    if len(sentence)>=maxsent: 
        print("Sentence overflow:",sentence)
        sentence=sentence[0:maxsent-1]
    if type(sentence[0])==list:
        for i in range(len(sentence)):
            for k in range(len(sentence[i])):
                #print(tex2vec[sentence[i][k]])
                try:
                    senarray.append(tex2vec[sentence[i][k]])
                except Exception as e:
                    print("Problem at phrase:", sentence[i][k])
                    
    else:
        for i in range(len(sentence)):
            try:
                senarray.append(tex2vec[sentence[i]])
            except Exception as e:
                print("Problem at phrase:", sentence[i])
                
    zr=zerolistmaker(num_features)
    #reverse if want to add a padding in front
    if frontpad: senarray.reverse()

    #add the padding
    for i in range(maxword-len(senarray)):     
        senarray.append(zr)

    #reverse again
    if frontpad: senarray.reverse()            
    
    return np.array(senarray)



def rem_list(input):
    remlist=['LePastee','Tertawalah','Campari','Gundik','mastektomi', 'Kerut', 'Ssshh']
    for i in remlist:
        try:
            ind=input.index(i)
            input.pop(ind)
        except:
            pass
    return input

def decode(pred):
    result=[]
    for i in range(maxsent):
        res = tex2vec.wv.similar_by_vector(pred[0][i])[0][0]
        result.append(res)
        result = rem_list(result)
        strj = ' '.join(result)
    return strj


# In[50]:


posmsg = [
    "Ini bagus banget, ",
    "Saya suka banget sama ini, ",
    "Wah asik banget ini yah. ",
    "Bagooooooossssss, ",
    "I love this, ",
    "Kapan nih berita gini?, ",
    "I love this post, ",
    "Postingan yang sangat bermutu, ",
    "Kapan?, ",
    "Terus kasih lagi gan..., ",
    "I like this, ",
    "Lanjuuuut gan, ",
    "Komen yang bermutu, ",
    "Twit ini sadis kerennya, ",
    "He he heh e, ",
    "Lanjoot, "
]

def ranmsg():
    a = random.randint(0,len(posmsg))
    return posmsg[a]


# In[51]:


def get_id_follower(username,count=20):
    result=[]
    maxc=0
    try:
        for user in tweepy.Cursor(api.followers, screen_name=username).items(count):
            maxc += 1
            result.append(user.screen_name)
            if maxc > count:
                break
    except:
        print("Error - get follower")
        result=['aagym']
    return result


# In[52]:


def get_rnd(rlist,count=3):
    result = []
    for i in range(count):
        a1 = random.randint(0,len(rlist)-1)
        result.append(rlist[a1])
    return result


# In[67]:


def replyer(m):
    m_user = m.user.screen_name
    print("Username:",m_user)
    msg_id = m.id
    m_text = m.text
    if not db_is_replied(msg_id):

        flwr = get_id_follower(str(m_user))
        reslt=get_rnd(flwr)
        db_insert_follower(m_user,reslt)
        twp_follow(reslt)
        print("Success adding follower of:", m_user)

        sender="@"+m_user+" "
        msg1 = ranmsg()
        msg2 = pred(m_text)
        msg3 = kaskus_search(m_text)
        tagthem = ' @'+' @'.join(reslt)
        fullmsg = sender+msg1+msg2+","+msg3+" "+tagthem
        print(fullmsg)
        rets = twp_reply_post(fullmsg,str(msg_id))
        #twp_cool_post(fullmsg,m_user,m_user)
        db_replied_this_id(msg_id,str(rets.id))
        db_replied_this_id(str(rets.id),str(rets.id))
    else:
        print("already replied")
        pass


# ### RUTIN KASKUS SEARCH

# In[62]:


def build_structure(string):
    return [' '.join(window) for n in range(len(string)) for
            window in windows(string.split(), n + 1, n)]

def windows(iterable, length=2, overlap=0):
    it = iter(iterable)
    results = list(itertools.islice(it, length))
    while len(results) == length:
        yield results
        results = results[length-overlap:]
        results.extend(itertools.islice(it, length-overlap))

def clean_word(string):
    pattern = re.compile('[\W_]+')
    words = []
    for word in string.split():
        word = re.sub(pattern, ' ', word)
        words.append(word)
    return ' '.join(words)

def make_keywords(string):
    string = clean_word(string.lower())
    keywords = []
    for phrase in build_structure(string):
        if len(list(phrase.split())) >= 1 and len(list(phrase.split())) <= 2:
            if phrase is not None and phrase.strip() != '':
                keywords.append(phrase)
    return secrets.choice(keywords)

def kaskus_search(topic, maxword=25):
    try:
        topic = make_keywords(topic)
        search_url = 'https://www.kaskus.co.id/search?q='

        page = requests.get(search_url+topic)

        sp = bs(page.text,"html.parser")

        #GET THE THREADS LINKS FROM MAIN PAGE
        thrds = []
        for a in sp.findAll("a",href=True):
            if a['href'].find('/thread/') != -1:
                thrds.append(a['href'])

        rsl = []
        for thrd in thrds:
            page = requests.get(thrd)
            sp = bs(page.text,"html.parser")

        #ambil konten di class entry - tapi dari mulai index 2
            rs = sp.findAll('div',{'class': 'entry'})
            for i in range(2,len(rs)):
                tx = rs[i].getText()
                if len(nltk.word_tokenize(tx)) < maxword:
                    rsl.append(tx)

        result=secrets.choice(rsl)
    except:
        result=""
    
    return result


# # TWEEPY INITIALIZE

# In[63]:


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()


    #m = public_tweets[0]


#cool_post("Keren gan wow-mantap","irzaip", "iriantomo")

#contoh sebuah reply
#api.update_status("@iriantomo Status ini bro kerens.", in_reply_to_status_id=1001139203487318016)


# In[64]:


#print(m.user.screen_name)
#print(m.user.followers_count)


# # BALAS SEMUA TWEET DI HOMEPAGE

# In[65]:


for tweet in public_tweets:
    print(tweet.text)
    replyer(tweet)


# ## Kalau mau balas post orang

# In[21]:


def reply_post_user(username, postnum=0):
    posts=api.user_timeline(id=username)
    replyer(posts[postnum])


# # PSEUDO CODE

# id = ambil_id_msg()
# check_msg_di_db()
# liat_user_msg()
# list_follower_usermsg()
# ambil_3_random_follower()
# ambil_random_jawaban()
# ambil_prediksi_twit_user()
# buat_msg()
# post_msg()
# catat_posting_di_db()
# follow_3_user()

# # SANDBOX

# # CLEAN UP  - Don't Forget

# In[22]:


#db.close()


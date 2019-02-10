#!/usr/bin/env python3
import re
import requests
from bs4 import BeautifulSoup
import random 

gen=['action','animation','comedy','documentary','drama','horror','romance','sci-fi']
set1={'01'}
num=[0,1,2,3,4,5,6,7]
for i in range(1,9):
    for j in range(10000):
        l=random.sample(num,i)
        l.sort()
        s=''.join(str(k) for k in l)
        set1.add(s)
print(*set1)
vectors=[]
set1=list(set1)
for i in set1:
    l=[0,0,0,0,0,0,0,0]
    l2=list(i)
    for k in l2:
        l[int(k)]=1
    vectors.append(l)

print(*vectors)

moviec=[[ gen[int(i)] for i in re.findall(r'\d{1}',_)] for _ in set1]

print(*moviec)

for s,k in zip(moviec,range(256)):
    
    r=requests.get(f"https://www.imdb.com/search/title?genres={','.join(s)}&groups=top_250&sort=user_rating,desc")
    soup=BeautifulSoup(r.text)
    final=[(_find('a')['href'].split('/')[2], _.find('a').text) for _ in soup.find('div',{'id':"main"}).findAll('h3', {'class': "lister-item-header"},vectors[k])]

print(*final)




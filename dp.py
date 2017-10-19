import requests
import re
import os
import json
from bs4 import BeautifulSoup
from collections import OrderedDict
import io 
import sys 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

req = requests.Session()
resp = req.get('http://dpchallenge.com/photo_gallery.php')
cate_url = re.findall(r'<li><a href="(.*?)">',resp.text)
clist = re.findall(r'GALLERY_ID(.*?)</a><br><b>',resp.text)
cate_list = [i.split('>')[1].replace('/','') for i in clist]

data=[]
k=0

for i in range(len(cate_list)):
    print(cate_list[i])
    tmp_data=OrderedDict()
    resp1=req.get('http://dpchallenge.com/'+cate_url[i]+"&page=1")
    detail_url=re.findall(r'width="20%"><a href="(.*?)" class="i"><img src="',resp1.text)
    imgurls=re.findall(r'class="i"><img src="(.*?)"',resp1.text)

    resp2=req.get('http://dpchallenge.com'+detail_url[0])
    print(resp2.text.encode('gbk','ignore').decode('utf-8'),file=open('text.html','w'))
    soup=BeautifulSoup(resp2.text,"lxml")
    source_url=soup.find_all('img',{'style':'border: 1px solid black'})[0]['src']
    img = req.get(source_url).content

    with open('data/'+str(k).zfill(8)+'.jpg','wb') as f:
        f.write(img)
    k+=1
    tmp_data['image_name']=str(k).zfill(8)+'.jpg'
    tmp_data['image_url']=source_url

    info=soup.find_all('tr',{'class':'forum-bg1'})
    info_arr=info[0].contents[1].find_all('a')

    tmp_data['information']={}
    tmp_data['information']['challenge']=info_arr[0].contents[0]+" ("+info_arr[1].contents[0]+")"
    tmp_data['information']['collection']=info_arr[2].contents[0]
    tmp_data['information']['camera']=info_arr[3].contents[0]
    tmp_data['information']['lens']=info_arr[4].contents[0]
    date=re.findall(r'<b>Date:</b>(.*?)<br>',resp2.text)
    if any(date):
        tmp_data['information']['date']=date[0].strip()
    else:
        tmp_data['information']['date']=''
    #tmp_data['information']['galleries']=info_arr[5].contents[0]
    tmp_data['information']['galleries']=[i.string for i in info[0].find_all('a',{'href':re.compile(r'/photo_gallery.php\?GALLERY_ID=.*')})]
    #print(re.findall(r'<b>Galleries:</b>(.*?)<br>',resp2.text))
    tmp_data['information']['date_uploaded']=re.findall(r'<b>Date Uploaded:</b>(.*?)<br>',resp2.text)[0].strip()
    #PhotographerComments=info[0].contents[3].contents[0]
    if len(info)>1:
        tmp_data['statistics']={}
        tmp_data['statistics']['place']=info[1].contents[1].contents[2].strip()
        tmp_data['statistics']['avg_all_users']=info[1].contents[1].contents[6].strip()
        tmp_data['statistics']['avg_commenters']=info[1].contents[1].contents[10].strip()
        tmp_data['statistics']['avg_participants']=info[1].contents[1].contents[14].strip()
        tmp_data['statistics']['avg_non_participants']=info[1].contents[1].contents[18].strip()
        tmp_data['statistics']['views_since_voting']=info[1].contents[1].contents[22].strip()
        tmp_data['statistics']['views_during_voting']=info[1].contents[1].contents[26].strip()
        tmp_data['statistics']['votes']=info[1].contents[1].contents[30].strip()
        tmp_data['statistics']['comments_num']=info[1].contents[1].contents[34].strip()
        tmp_data['statistics']['favorites']=info[1].contents[1].contents[38].strip()
    else:
        tmp_data['statistics']={}
        tmp_data['statistics']['place']=''
        tmp_data['statistics']['avg_all_users']=''
        tmp_data['statistics']['avg_commenters']=''
        tmp_data['statistics']['avg_participants']=''
        tmp_data['statistics']['avg_non_participants']=''
        tmp_data['statistics']['views_since_voting']=''
        tmp_data['statistics']['views_during_voting']=''
        tmp_data['statistics']['votes']=''
        tmp_data['statistics']['comments_num']=''
        tmp_data['statistics']['favorites']=''

    comments=[]
    for item in soup.find_all('table',{'class','forum-post'}):
        comments.append(item.contents[0].contents[0].contents[0])
    tmp_data['comments']=comments

    data.append(tmp_data)
    #source_url=re.findall(r'z-index: 1;" /><img src="(.*?)"',resp2.text)
    #info=re.findall(r'<b>Challenge:(.*?)\n',resp2.text)
    #print(info.findall())
    #print(source_url[0])
    if k==2:
        break
print(data)
print(json.dumps(data,sort_keys=False),file=open('data.json','w'))
#print(resp.text.encode('gbk','ignore').decode('utf-8'),file=open('text.html','w'))
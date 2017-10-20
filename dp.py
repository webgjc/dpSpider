import requests
import re
import os
import json
from bs4 import BeautifulSoup
from collections import OrderedDict
import hashlib
import io 
import sys 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
req = requests.Session()
resp = req.get('http://dpchallenge.com/photo_gallery.php',headers=headers)
cate_url = re.findall(r'<li><a href="(.*?)">',resp.text)
clist = re.findall(r'GALLERY_ID(.*?)</a><br><b>',resp.text)
cate_list = [i.split('>')[1].replace('/','') for i in clist]
data=[]
signatures=[]
k=0

for i in range(len(cate_list)):
    print(cate_list[i])
    tmp_data=OrderedDict()
    resp1=req.get('http://dpchallenge.com/'+cate_url[i]+"&page=1",headers=headers)
    detail_url=re.findall(r'width="20%"><a href="(.*?)" class="i"><img src="',resp1.text)
    #imgurls=re.findall(r'class="i"><img src="(.*?)"',resp1.text)
    for item_url in detail_url:
        resp2=req.get('http://dpchallenge.com'+item_url,headers=headers)
        print(resp2.text.encode('gbk','ignore').decode('utf-8'),file=open('text.html','w'))
        soup=BeautifulSoup(resp2.text,"lxml")
        source_url=soup.find_all('img',{'style':'border: 1px solid black'})[0]['src']
        imageSign=hashlib.md5(source_url.encode('utf-8')).hexdigest()
        if imageSign in signatures:
            continue
        else:
            signatures.append(imageSign)
        img = req.get(source_url,headers=headers).content

        with open('data/'+str(k).zfill(8)+'.jpg','wb') as f:
            f.write(img)
        k+=1
        tmp_data['image_name']=str(k).zfill(8)+'.jpg'
        tmp_data['image_url']=source_url

        info=soup.find_all('tr',{'class':'forum-bg1'})
        info_arr=info[0].contents[1].find_all('a')

        tmp_data['information']=OrderedDict()

        challenge=re.findall(r'Challenge:</b>(.*?)<br>',resp2.text)
        if any(challenge):
            tmp_data['information']['challenge']=BeautifulSoup(challenge[0],'lxml').get_text()
        else:
            tmp_data['information']['challenge']=''

        collection=re.findall(r'Collection:</b>(.*?)<br>',resp2.text)
        if any(collection):
            tmp_data['information']['collection']=BeautifulSoup(collection[0],'lxml').get_text()
        else:
            tmp_data['information']['collection']=''

        camera=re.findall(r'Camera:</b>(.*?)<br>',resp2.text)
        if any(camera):
            tmp_data['information']['camera']=BeautifulSoup(camera[0],'lxml').get_text()
        else:
            tmp_data['information']['camera']=''

        lens=re.findall(r'Lens:</b>(.*?)<br>',resp2.text)
        if any(lens):
            tmp_data['information']['lens']=BeautifulSoup(lens[0],'lxml').get_text()
        else:
            tmp_data['information']['lens']=''

        aperture=re.findall(r'Aperture:</b>(.*?)<br>',resp2.text)
        if any(aperture):
            tmp_data['information']['aperture']=BeautifulSoup(aperture[0],'lxml').get_text()
        else:
            tmp_data['information']['aperture']=''

        iso=re.findall(r'ISO:</b>(.*?)<br>',resp2.text)
        if any(iso):
            tmp_data['information']['iso']=BeautifulSoup(iso[0],'lxml').get_text()
        else:
            tmp_data['information']['iso']=''

        shutter=re.findall(r'Shutter:</b>(.*?)<br>',resp2.text)
        if any(shutter):
            tmp_data['information']['shutter']=BeautifulSoup(shutter[0],'lxml').get_text()
        else:
            tmp_data['information']['shutter']=''

        location=re.findall(r'Location:</b>(.*?)<br>',resp2.text)
        if any(location):
            tmp_data['information']['location']=BeautifulSoup(location[0],'lxml').get_text()
        else:
            tmp_data['information']['location']=''

        date=re.findall(r'<b>Date:</b>(.*?)<br>',resp2.text)
        if any(date):
            tmp_data['information']['date']=date[0].strip()
        else:
            tmp_data['information']['date']=''
        #tmp_data['information']['galleries']=info_arr[5].contents[0]
        tmp_data['information']['galleries']=[i.string for i in info[0].find_all('a',{'href':re.compile(r'/photo_gallery.php\?GALLERY_ID=.*')})]
        #print(re.findall(r'<b>Galleries:</b>(.*?)<br>',resp2.text))
        tmp_data['information']['date_uploaded']=re.findall(r'<b>Date Uploaded:</b>(.*?)<br>',resp2.text)[0].strip()

        viewed=re.findall(r'Viewed:</b>(.*?)<br>',resp2.text)
        if any(viewed):
            tmp_data['information']['viewed']=BeautifulSoup(viewed[0],'lxml').get_text()
        else:
            tmp_data['information']['viewed']=''

        comments=re.findall(r'Comments:</b>(.*?)<br>',resp2.text)
        if any(comments):
            tmp_data['information']['comments']=BeautifulSoup(comments[0],'lxml').get_text()
        else:
            tmp_data['information']['comments']=''

        favorites=re.findall(r'Favorites:</b>(.*?)<br>',resp2.text)
        if any(favorites):
            tmp_data['information']['favorites']=BeautifulSoup(favorites[0],'lxml').get_text()
        else:
            tmp_data['information']['favorites']=''
        #PhotographerComments=info[0].contents[3].contents[0]
        if any(re.findall(r'<td nowrap>Statistics</td>',resp2.text)):
            tmp_data['statistics']=OrderedDict()
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
            comments.append(item.contents[0].contents[0].contents[0].strip())
        tmp_data['comments']=comments

        data.append(tmp_data)
        break
        #source_url=re.findall(r'z-index: 1;" /><img src="(.*?)"',resp2.text)
        #info=re.findall(r'<b>Challenge:(.*?)\n',resp2.text)
        #print(info.findall())
        #print(source_url[0])
    if i==9:
        break
#print(data)
print(json.dumps(data,sort_keys=False),file=open('data.json','w'))
#print(resp.text.encode('gbk','ignore').decode('utf-8'),file=open('text.html','w'))
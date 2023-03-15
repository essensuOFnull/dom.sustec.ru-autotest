from bs4 import BeautifulSoup
from os import listdir,path
directory="input"
for filename in listdir(directory):
    f=path.join(directory,filename)
    if path.isfile(f):
        soup=BeautifulSoup(open(f,"r",encoding="utf-8").read(),"html.parser")
        for s in soup.select('script'):s.extract()
        with open(f,'w',encoding='utf-8')as f:f.write(str(soup))
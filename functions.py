#by essensuOFnull
#скрипты могут работать неправильно, я не несу никакой ответственности за это
#чтобы установить необходимые библиотеки введите pip install beautifulsoup4,colorama
from bs4 import BeautifulSoup
from os.path import isfile
from os import listdir
from re import sub
def data_preparation():#создает пустой словарь data или достает уже имеющийся
    if isfile("data/data.py"):
        try:from data.data import data
        except:pass
        if not"data"in locals()or type(data)!=dict:data={}
    else:data={}
    return data
def save_data(data):#сохраняет словарь data в файл БЕЗ ЕБУЧИХ ПРОБЕЛОВ
    with open('data/data.py','w',encoding='utf-8')as f:f.write('data='+sub(r"\s+(?=([^']*'[^']*')*[^']*$)",'',str(data)))
def merge_test_data(test_id,questions,data):#добавляет всю ту инфу о тесте, коей раньше не было, кроме оценки в случае наличия ответа - отсутствие оценки считается за правильность ответа
    if test_id not in data.keys():data[test_id]=questions
    else:
        for key in questions.keys():
            if not key in data[test_id].keys():data[test_id][key]=questions[key]
            else:
                if type(questions[key])==list:#нет подвопросов
                    for i in range(2):
                        for value in questions[key][i]:
                            if value not in data[test_id][key][i]:data[test_id][key][i].append(value)
                    if len(data[test_id][key])>2:#в старой бд есть информация об оценке. иначе ответ считается полностью правильным
                        if len(questions[key])>2:#в новой тоже
                            if data[test_id][key][:1]!=questions[key][:1]:data[test_id][key][2]=-max(abs(data[test_id][key][2]),questions[key][2])#точная оценка неизвестна. минус используется как костыль, обозначающий ≥
                            else:data[test_id][key][2]=questions[key][2]#обновление информации об оценке
                        else:data[test_id][key].pop()#поскольку ныне решено правильно, информация об оценке удаляется
                else:
                    if type(data[test_id][key])!=dict:data[test_id][key]={}
                    for subkey in questions[key].keys():
                        if not subkey in data[test_id][key].keys():data[test_id][key][subkey]=questions[key][subkey]
                        else:
                            for i in range(2):
                                for value in questions[key][subkey][i]:
                                    if value not in data[test_id][key][subkey][i]:data[test_id][key][subkey][i].append(value)
#def content_of(element):return "".join([str(content)for content in element.contents])#возвращает контент элемента как строку. оказалось что при скачивании он может измениться, поэтому это бесполезно блять
def get_essence(element):return element.get_text()if element.find("img")is None else element.find("img")["src"].split("/")[-1].split(".")[0]#возвращает то, чем элемент можно однозначно отличить от других (надеюсь блять)
def open_code(path):return BeautifulSoup(open(path,"r",encoding="utf-8").read(),"html.parser")#открывает файл для парсинга
#def get_test_id(soup):return int(str(soup.find("div",class_="que")).split("-")[1])#возвращает id теста dom.sustec. как оказалось это абсолютно бесполезная инфа
def get_test_name(soup):return soup.find("meta",{"name":"keywords"}).get("content")[8:].split(":")[0].split(" (")[0]#возвращает название теста, сим используемое в качестве id
def get_question_divs(soup):return soup.findAll("div",class_="que")#возвращает список div-ов вопросов
def get_question_id(div):return int(div.get("id").split("-")[2])#возвращает id вопроса
def get_grade(div):#возвращает правильность ответа в виде числа от 0 до 1, либо None если ответ не последовал
    grade=div.find("div",class_="grade").get_text().replace(",",".").split()#получение слов строки о набранных баллах
    if len(grade)==4:#попытка ответить на вопрос была произведена. как я позже заметил эту инфу также можно выдрать из содержащего id вопроса div-а
        if float(grade[1])==float(grade[3]):grade=1#ответ правильный
        elif float(grade[1])!=0:grade=float(grade[1])/float(grade[3])#ответ частично правильный. получение выраженного через число от 0 до 1 процента правильности ответа
        else:grade=0#ответ неправильный
    else:grade=None#ответ на вопрос не последовал
    return grade
def get_question_type(main_div):#принимает контейнер вопроса
    global type_;type_=None
    content=main_div.find(class_="answer")
    if content is None:type_="combobox"
    else:
        if content.name=="table":type_="combobox group"if main_div.find(class_="matchorigin")is None else"drag group"
        else:
            if content.name=="div":
                if content.find("input",{"type":"radio"})is not None:type_="radiobutton"
                else:type_="checkbox"
            elif content.name=="span":type_="textbox"
    if type(type_)==None:print("неизвестный тип вопроса. свяжитесь со мной, мб мне будет не в падлу посмотреть чо вы пытаетесь запихать в мой скрипт, мб я добавлю поддержку этого.")
    else:return type_
def get_subquestions_essence(content):return[get_essence(subcontent.find("p"))for subcontent in content.findAll("td",class_="text")]#возвращает список сути подвопросов
def get_answers_essence(content):#возвращает список сути возможных ответов или подответов, в некоторых случаях словарь
    if type_=="drag group":
        output={}
        for subcontent in content.findAll(class_="matchdrag"):output[int(subcontent["data-id"])]=get_essence(subcontent.find("p"))
        return output
    elif type_ in["combobox group","combobox"]:return[get_essence(option)for option in content.findAll("option")]
    elif type_ in["radiobutton","checkbox"]:return[get_essence(text)for text in content.findAll(class_="ml-1")]
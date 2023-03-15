from functions import*
from sys import argv
from colorama import init,Fore
if len(argv)<2:print("укажите в команде путь до файла, ответы к которому нужно получить, если все ответы нужно вводить на одной странице, или до папки с сайтами страниц в противном случае")
else:
    path=argv[1]
    init()#включение поддержки цветного текста
    R=Fore.RED;G=Fore.GREEN;Gr="\033[38;5;245m";M=Fore.MAGENTA;Y=Fore.YELLOW;W=Fore.WHITE;print()
    def list_to_str(list,c=G):return c+(W+", "+c).join(list)+W#возвращает список, преобразованный в 1 строку через белую запятую
    def get_local_numbers(numbers):return sorted(chr(answers_content.index(sorted(answers_content)[number])+97)for number in numbers)#возвращает список локальных номеров отетов
    if isfile(path):paths=[path]#подразумевается что все ответы нужно вводить на одной странице
    else:
        paths=[]
        for filename in listdir(path):
            f=path+"/"+filename
            if isfile(f):paths.append(f)
        paths.sort(key=lambda x:int(x.split("(")[1].split()[1]))
    data=data_preparation();test_id=get_test_name(open_code(paths[0]))
    if test_id in data.keys():
        number=1
        for f in paths:
            soup=open_code(f)
            for main_div in get_question_divs(soup):
                question_id=get_question_id(main_div);print(Y+str(number)+")"+W,end=" ")
                if question_id in data[test_id].keys():
                    info=data[test_id][question_id]#информация о конкретном вопросе
                    content=main_div.find(class_="answer");question_type=get_question_type(content)
                    if type(info)==dict:#группа combobox-ов
                        print();subnumber=1;questions_content=sorted(get_subquestions_content(content))
                        for subcontent in content.findAll("tr"):
                            print(M+str(subnumber)+"."+W,end=" ")
                            subquestion_number=questions_content.index(content_of(subcontent.find("p")))
                            subinfo=info[subquestion_number]
                            count=[len(subinfo[0]),len(subinfo[1])]
                            answers_content=get_answers_content(subcontent)
                            if count[0]>0:print(("похоже на то, что кто-то решил вас дезинформировать, поскольку в базе данных больше одного номера правильного подответа: "if count[0]>1 else"номер правильного подответа: ")+list_to_str(get_local_numbers(subinfo[0])))
                            else:print("правильный подответ неизвестен. список номеров неправильных подответов: "+list_to_str(get_local_numbers(subinfo[1]),R))
                            subnumber+=1
                    else:
                        count=[len(info[0]),len(info[1])]
                        if count[0]!=0 or count[1]!=0:
                            if question_type=="textbox":#ответ нужно ввести вручную
                                if count[0]>0:print(("похоже на то, что кто-то решил вас дезинформировать, поскольку в базе данных больше одного правильного ответа: "if count[0]>1 else "ответ: ")+list_to_str(info[0]))
                                else:print("правильный ответ неизвестен. список неправильных ответов: "+list_to_str(info[1],R))
                            else:#ответ нужно выбрать из готовых вариантов
                                if question_type=="combobox":answers_content=get_answers_content(main_div)
                                elif question_type in["radiobutton","checkbox"]:answers_content=get_answers_content(content)
                                if question_type in["radiobutton","combobox"]:
                                    if count[0]>0:print(("похоже на то, что кто-то решил вас дезинформировать, поскольку в базе данных больше одного номера правильного ответа: "if count[0]>1 else"номер правильного ответа: ")+list_to_str(get_local_numbers(info[0])))
                                    else:print("правильный ответ неизвестен. список номеров неправильных ответов: "+list_to_str(get_local_numbers(info[1]),R))
                                elif question_type=="checkbox":
                                    if len(info)<3:print("номера правильных ответов: "+list_to_str(get_local_numbers(info[0])))#известен полностью правильный ответ
                                    else:
                                        print("приведенной ниже информации достаточно только для того чтобы ответить на "+Y+str(int(info[2]*100)).replace("-","≥")+"%"+W+" правильно.")
                                        if count[0]!=0:print("номера правильных ответов: "+list_to_str(get_local_numbers(info[0])))
                                        if count[1]!=0:print("номера неправильных ответов: "+list_to_str(get_local_numbers(info[1]),R))
                        else:print(Gr+"в базе данных нет никакой информации по данному вопросу.")
                else:print(Gr+"похоже на то, что информация об этом вопросе была кем-то удалена вручную...")
                number+=1
    else:print("в твоей базе данных нет никакой инфы по данному тесту, либо произошёл баг.\nпройди его сам и поделись ответами со всеми, особенно со мной, будешь молодец.")
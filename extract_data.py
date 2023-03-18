from functions import*
directory="input"#папка с сайтами
data=data_preparation();errors=[];raw=[]
for filename in listdir(directory):
    f=directory+"/"+filename
    if isfile(f):
        #try:
        soup=open_code(f);questions_id=[];answers=[];test_id=get_test_name(soup)
        for main_div in get_question_divs(soup):
            save_grade=0#стоит ли записать оценку в бд
            questions_id.append(get_question_id(main_div))#получение id вопроса
            grade=get_grade(main_div)
            main_div=main_div.find("div",class_="formulation clearfix")#углубление в код
            answer=[];wrong=[]
            if grade==None:answers.append([answer,wrong])#на вопрос не удосужились ответить
            else:
                content=main_div.find(class_="answer")
                question_type=get_question_type(main_div)
                if question_type in["combobox group","drag group"]:
                    drag=0 if question_type=="combobox group"else 1#для удобства в будущем
                    questions_essence=sorted(get_subquestions_essence(content))#получение отсортированного списка сути подвопросов
                    subquestions_id=[];subanswers=[]
                    if drag:subanswers_essence=get_answers_essence(content)#получение словаря выбранных подответов, где ключами являются номера выбранных в select option
                    for subcontent in content.findAll("tr"):
                        subquestions_id.append(questions_essence.index(get_essence(subcontent.find("p"))))#получение id подвопроса
                        selected_id=int(subcontent.find("option",{"selected":"selected"})["value"])#номер выбранного option в select
                        if selected_id==0:subanswers.append([[],[]])#на данный подвопрос не удосужились ответить
                        else:
                            if drag:answer=subanswers_essence[selected_id]
                            else:
                                subanswers_essence=sorted(get_answers_essence(subcontent))#получение отсортированного списка содержимого возможных подответов
                                answer=subanswers_essence.index(get_essence(subcontent.find("option",{"selected":"selected"})))#получение id выбранного подответа
                            subanswers.append([[],[answer]]if subcontent.find("i",class_="text-success")is None else[[answer],[]])
                    answers.append(dict(zip(subquestions_id,subanswers)))#добавление словаря подвопросов
                else:
                    if question_type=="combobox":
                        answers_content=sorted(get_answers_essence(main_div))#получение отсортированного списка содержимого возможных ответов
                        selected_id=answers_content.index(get_essence(main_div.find("option",{"selected":"selected"})))#получение id выбранного ответа
                        if grade:answer.append(selected_id)
                        else:wrong.append(selected_id)
                    elif question_type in["radiobutton","checkbox"]:
                        if question_type=="checkbox":save_grade=1
                        answers_content=sorted(get_answers_essence(content))#получение отсортированного списка содержимого возможных ответов
                        having=[1 if content.find("div",class_="correct")is not None else 0,1 if content.find("div",class_="incorrect")is not None else 0]#получение информации о том, есть ли контейнеры, помеченные как правильные/неправильные
                        if 1 in having:#в коде дана информация о правильности/неправильности ответов
                            if having[0]:
                                for correct in content.findAll("div",class_="correct"):answer.append(answers_content.index(get_essence(correct.find(class_="ml-1"))))#получение id правильных ответов
                            if having[1]:
                                for incorrect in content.findAll("div",class_="incorrect"):wrong.append(answers_content.index(get_essence(incorrect.find(class_="ml-1"))))#получение id неправильных ответов
                        else:#разрабы решили ебать мозги
                            if question_type=="radiobutton":#инфу можно выдрать однозначно, так что они идут нахуй
                                for subcontent in content.findAll("div",{'class':['r0','r1']}):#перебор div-ов с классами r0 или r1
                                    if subcontent.find("input",{"checked":"checked"}):#выбран находящийся в данном div-е ответ
                                        selected_id=answers_content.index(get_essence(subcontent.find(class_="ml-1")))
                                        if grade:answer.append(selected_id)
                                        else:wrong.append(selected_id)
                            elif question_type=="checkbox":
                                answers_count=len(content.findAll("input",{"checked":"checked"}))#получение количества нажатых checkbox-ов
                                for subcontent in content.findAll("div",{'class':['r0','r1']}):#перебор div-ов с классами r0 или r1
                                    if subcontent.find("input",{"checked":"checked"}):#выбран находящийся в данном div-е ответ
                                        selected_id=answers_content.index(get_essence(subcontent.find(class_="ml-1")))
                                        if grade:answer.append(selected_id)#ответ полностью правильный
                                        elif grade!=0:#ответ частично правильный
                                            if answers_count==1:answer.append(selected_id);break#выбран всего 1 вариант ответа, инфу можно выдрать однозначно
                                            #в теории сюда можно пихнуть ещё чот для обработки других ебучих случаев
                                        else:wrong.append(selected_id)#ответ полностю неправильный
                    elif question_type=="textbox":
                        value=content.find("input").get("value")
                        if grade:answer.append(value)
                        else:wrong.append(value)
                    else:raw.append(filename)
                    answers.append([answer,wrong,grade]if save_grade and grade!=1 else[answer,wrong])
        merge_test_data(test_id,dict(zip(questions_id,answers)),data)
        #except Exception as err:errors.append(filename);print(err)
if len(errors)!=0:
    print("\nошибки произошли при обработке сделующих файлов:")
    for f in errors:print(f)
if len(raw)!=0:
    print("\nнеподдерживаемые типы вопросов были встречены при обработке сделующих файлов:")
    for f in raw:print(f)
save_data(data)
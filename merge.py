from functions import*
from os import listdir,remove,rename
from os.path import isfile
data=data_preparation()
directory="data"#папка с файлами данных о тестах
files_and_dirs=listdir(directory)#получаем список файлов и каталогов
if"data.py"in files_and_dirs:files_and_dirs.remove("data.py")#если есть файл data.py, то инфа из него уже выдрана и его надо удалить из списка перебираемых файлов
files=[]#получаем список только файлов
for filename in files_and_dirs:
    if isfile(directory+"/"+filename):files.append(filename)
if files==[]:print("в папку data поскидывай файлы алё")#список перебираемых файлов пуст, делать нечего
else:
    for i in range(len(files)):name="data"+str(i)+".py";rename(directory+"/"+files[i],directory+"/"+name);files[i]=name#переименовываем файлы должным образом
    for filename in files:
        exec("from "+directory+"."+filename.split(".")[0]+" import data as new_data")
        for key in new_data.keys():merge_test_data(key,new_data[key],data)
        remove(directory+"/"+filename)
    save_data(data)
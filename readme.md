перед использованием установите python (https://www.python.org/), при установке согласитесь на его добавление в path, после чего установите необходимые библиотеки с помощью команды pip install beautifulsoup4,colorama
поместите скрипты в одну папку, в последствии для их запуска нужно будет предворительно перейти в неё с помощью команды cd путь_до_папки.
создайте в данной папке папки input и data. в папку input следует ложить скаченные сайты с ответами, html кода достаточно.
запуск extract_data.py извлечет данные из этих файлов и положит как файл data.py в папку data.
запустив merge.py и предворительно поместив другие полученные с помощью extract_data.py файлы в папку data можно объединить их в один.
get_answers.py принимает как аргумент командной строки путь до скаченного html кода сайта, если все ответы нужно вводить на одной странице, или до папки с сайтами страниц в противном случае, после чего выводит имеющиеся в файле data.py ответы
все скрипты следует запускать командой python скрипт.py путь_до_файла/папки(в случае get_answers.py)
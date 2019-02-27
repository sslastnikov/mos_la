from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

PRIMARY_SOURCE_PATH = ["firstapp", "la_data", "primary"]
RESULT_SOURCE_PATH = ["firstapp", "la_data", "results"]

def index(request):
    links = []
    links.append('<h2><p><a href="./primary">Стартовые протоколы</a></p></h2>')
    links.append('<h2><p><a href="./results">Результаты</a></p></h2>')
    return HttpResponse("\n".join(links))

def showPrimaryData(request):
    data = {}
    try:
        import os
        resDict = {}
        FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), PRIMARY_SOURCE_PATH[0], PRIMARY_SOURCE_PATH[1], PRIMARY_SOURCE_PATH[2])
        fList = os.listdir(FULL_SOURCE_PATH)
        i = 1
        for fName in fList:
            if not fName.endswith(".evt"):
                continue
            pathName = os.path.join(FULL_SOURCE_PATH, fName)
            with open(pathName, 'r', encoding='utf16') as f:
                for line in f:
                    row = line.split(',')
                    if ((line[0]).isdigit()):
                        #tmp = [row[3], row[1] + ' круг', row[2] + ' забег']
                        link = ('./primary/' + fName[: fName.index(".")] + '/' + str(i), row[1] + ' круг, ' + row[2] + ' забег')
                        resDict.setdefault(row[3], []).append(link)
                        i += 1
        data = {"resultDict": resDict}
    except Exception as e:
        return HttpResponse('<h2>' + str(e) + '</h2>')
    return render(request, "result_list.html", data)

def showResultData(request):
    data = {}
    try:
        import os
        resDict = {}
        FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), RESULT_SOURCE_PATH[0], RESULT_SOURCE_PATH[1], RESULT_SOURCE_PATH[2])
        fList = os.listdir(FULL_SOURCE_PATH)
        for fName in fList:
            if not fName.endswith(".lif"):
                continue
            pathName = os.path.join(FULL_SOURCE_PATH, fName)
            with open(pathName, 'r', encoding='utf16') as f:
                for line in f:
                    if ((line[0]).isdigit() or (line[0]).isalpha()):
                        row = line.split(',')
                        link = ('./results/' + fName[: fName.index(".")], row[1] + ' круг, ' + row[2] + ' забег')
                        resDict.setdefault(row[3], []).append(link)
                    break
        data = {"resultDict": resDict}
    except Exception as e:
        return HttpResponse('<h2>' + str(e) + '</h2>')
    return render(request, "result_list.html", data)

def showResult(request, source):
    data = {}
    try:
        import os
        links = []
        FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), RESULT_SOURCE_PATH[0], RESULT_SOURCE_PATH[1], RESULT_SOURCE_PATH[2])
        pathName = os.path.join(FULL_SOURCE_PATH, source + ".lif")
        with open(pathName, 'r', encoding='utf16') as f:
            i = 0
            for line in f:
                row = line.split(',')
                if i == 0:
                    data['header'] = row[3] + ', ' + row[1] + ' круг, ' + row[2] + ' забег'
                else:
                    links.append([row[0], row[1], row[3] + ' ' + row[4], row[5], row[6]])
                i += 1
            data['rows'] = links
            data['tableHead'] = ['№ п\п', '№ уч.', 'ФИО', 'Организация', 'Результат']

    except Exception as e:
        return HttpResponse('<h2>' + str(e) + '</h2>')
    return render(request, "simple_table.html", data)

def showPrimary(request, source, number):
    data = {}
    try:
        num = int(number)
        import os
        FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), PRIMARY_SOURCE_PATH[0], PRIMARY_SOURCE_PATH[1], PRIMARY_SOURCE_PATH[2])
        pathName = os.path.join(FULL_SOURCE_PATH, source + ".evt")
        rows = []
        with open(pathName, 'r', encoding='utf16') as f:
            lines = f.readlines()
            i = 0
            k = 0
            while (i < num and k < len(lines)):
                if ((lines[k][0]).isdigit()):
                    i += 1
                k += 1
            row = lines[k-1].split(',')
            data['header'] = row[3] + ', ' + row[1] + ' круг, ' + row[2] + ' забег'
            if k < len(lines):
                while (not(lines[k][0].isdigit())):
                    row = lines[k].split(',')
                    rows.append([row[1], row[2], row[3] + ' ' + row[4], row[5], row[6]])
                    k += 1
            data['rows'] = rows
            data['tableHead'] = ['Номер', 'Дорожка', 'ФИО', 'Организация', 'Лицензия']

    except Exception as e:
        return HttpResponse('<h2>' + str(e) + '</h2>')
    return render(request, "simple_table.html", data)
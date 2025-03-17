from bs4 import BeautifulSoup
import json

# HTML 파일 불러오기
html_file_path = "log.html"

with open(html_file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# 'focusable' 클래스를 가진 요소 찾기
focusable_elements = soup.find_all(class_="focusable")

# 'aria-label' 속성 추출
aria_labels = [element.get("aria-label") for element in focusable_elements if element.get("aria-label")]

file.close()

# 아이디 받기
id1 = input("your id: ").strip()
id2 = input("their id: ").strip()
str1 = ", @{} ".format(id1)
str2 = ", @{} ".format(id2)

# 추출한 내용을 파일로 저장
data = []
for label in aria_labels:
    line = label.replace(str1, "$")
    line = line.replace(str2, "$")
    line = line.replace("., ", ".$")
    line = line.replace("?, ", "?$")
    line = line.replace("!, ", "!$")
    line = line.replace("), ", ")$")
    line = line.replace('", ', '"$')
    line = line.replace("', ", "'$")
    line = line.replace("”, ", "”$")
    line = line.replace("’, ", "’$")

    data.append(line)
data[0] = data[0].replace(", ", "$", 1)

# JSONify
thread = []
def formatToot(l):
        toot = l.split('$')
        info = toot[2].split(', ')

        return {
            "name": toot[0],
            "mssg": toot[1],
            "time": info[0],
            "id": info[1].strip()
        }
    
for l in data:
    thread.append(formatToot(l))

try:
    with open('{yourId}/{theirId}.json'.format(yourId=id1, theirId=id2), 'r', encoding='utf-8') as f:
        update = json.load(f)
    f.close()
except FileNotFoundError:
    update = []
finally:
    update.append(thread)
    with open('{yourId}/{theirId}.json'.format(yourId=id1, theirId=id2), 'w', encoding='utf-8') as j:
        json.dump(update, j, indent=2, ensure_ascii=False)
j.close()
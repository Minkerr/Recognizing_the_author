from bs4 import BeautifulSoup
import requests
import sqlite3 as sl
#
#!!!!!
#
# Here I have scrabbed all Lovecraft's stories, separated into chapters, into database
#
#!!!!!
#


# open file with DB. If the file don't exist, he will be created
con = sl.connect('TestDB.db')

url = 'https://www.hplovecraft.com/writings/texts/'
response = requests.get(url)
print(response)
soup = BeautifulSoup(response.text, "html.parser")
links = []
for link in soup.find_all('a'):
    l = link.get('href')
    if l != None and l.startswith('fiction'):
        links.append(l)
# for link in links:
#    print(link)
# print(len(links))

count = 1
for j in range(len(links)):
    url = 'https://www.hplovecraft.com/writings/texts/' + links[j]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.find_all('tr')[4].text
    text = text.replace('\n', '')
    texts = []

    if text.find("I.") != -1:
        texts.append(text[(text.find("I.") + 3): text.find("II.")])
        text = text[text.find("II."):]

    rimNumbers = ["I", "II", "III", "IV", ".V", "VI", "VII", "VIII", "IX", ".X", "XI", "XII"]
    for i in range(2, 12):
        if text.find(rimNumbers[i]+".") != -1:
            texts.append(text[:text.find(rimNumbers[i]+".")])
            text = text[text.find(rimNumbers[i]+"."):]
    texts.append(text)

    for line in texts:
        sql = 'INSERT INTO texts (author, text) values(?, ?)'
        data = [('Lovecraft', line)]
        with con:
            con.executemany(sql, data)
        count += 1
    #
    # with open("parcing.txt", 'w', encoding="utf-8") as reader:
    #    for line in texts:
    #         reader.write("\n_SPLIT_\n")
    #         reader.write(line)
    #         id += 1

#
#!!!!!
#
# But it turned out I didn't need it. So I used this
#
#!!!!!
#

con = sl.connect('TestDB.db')

url = 'https://www.hplovecraft.com/writings/texts/'
response = requests.get(url)
print(response)
soup = BeautifulSoup(response.text, "html.parser")
links = []
for link in soup.find_all('a'):
    l = link.get('href')
    if l != None and l.startswith('fiction'):
        links.append(l)


for j in range(len(links)):
    if j == 2 or j == 9 or j == 24:  # excluded 3 long stories
        continue
    url = 'https://www.hplovecraft.com/writings/texts/' + links[j]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.find_all('tr')[4].text
    sql = 'INSERT INTO texts (author, text) values(?, ?)'
    data = [('Lovecraft', text)]
    with con:
        con.executemany(sql, data)
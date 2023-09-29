from bs4 import BeautifulSoup
import requests
import sqlite3 as sl


con = sl.connect('TestDB.db')

titles = []
with open("titles.txt", 'r', encoding="utf-8") as reader:
    for line in reader:
        titles.append(line)

titleIndex = 0
fullLine = ""
with open("hemingway.txt", 'r', encoding="utf-8") as text:
    for line in text:
        if line.find(titles[titleIndex]) != -1:
            sql = 'INSERT INTO texts (author, text) values(?, ?)'
            data = [('Hemingway', fullLine)]
            with con:
                con.executemany(sql, data)
            titleIndex += 1
            if titleIndex == 26 or titleIndex == 48:
                titleIndex += 1
            fullLine = ""
        else:
            fullLine += line

#
# SECOND PART
#

con = sl.connect('TestDB.db')

with open("parcing.txt", 'w', encoding="utf-8") as reader:
    for i in range(2, 9):
        url = 'https://onlinereadfreenovel.com/ernest-hemingway/p,' + str(i) + ',31949-a_farewell_to_arms_read.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.find('div', class_='text').text
        reader.write(text)

with open("parcing.txt", 'r', encoding="utf-8") as reader:
    for line in reader:
        sql = 'INSERT INTO texts (author, text) values(?, ?)'
        data = [('Hemingway', line)]
        with con:
            con.executemany(sql, data)
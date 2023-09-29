import sqlite3 as sl
import matplotlib.pyplot as plt
from math import *
import math

con = sl.connect('TestDB.db')
#SELECT * FROM texts WHERE id BETWEEN 1 and 50 or id BETWEEN 76 and 100
sentences_love_train = []
words_love_train = []
sentences_hem_train = []
words_hem_train = []
data = con.execute("SELECT * FROM texts WHERE id BETWEEN 26 and 100")
for row in data:
    sentences_love_train.append(row[3])
    words_love_train.append(row[4])
data = con.execute("SELECT * FROM texts WHERE id BETWEEN 126 and 200")
for row in data:
    sentences_hem_train.append(row[3])
    words_hem_train.append(row[4])
    
k = 0
b = 0
mn = 1000
c = 0
alp = pi / 2 + 0.0001
while c < 100:  # searching line equation
    alp = pi / 2 + 0.0001
    while alp <= pi - 0.001:
        count = 0
        for i in range(75):
            if words_love_train[i] < math.tan(alp) * sentences_love_train[i] + c:
                count += 1
            if words_hem_train[i] > math.tan(alp) * sentences_hem_train[i] + c:
                count += 1
        if count < mn:
            mn = count
            k = math.tan(alp)
            b = c
        alp += 0.01
    c += 0.01
print(mn)

plt.axis([5, 35, 2, 6])
plt.title('Lovecraft vs. Hemingway')
plt.ylabel('Average word length')
plt.xlabel('Average sentence length')
plt.plot(sentences_love_train, words_love_train, 'ro')
plt.plot(sentences_hem_train, words_hem_train, 'go')
plt.axline([0, b], [-b / k, 0])
plt.show()

sentences_love_test = []
words_love_test = []
sentences_hem_test = []
words_hem_test = []
data = con.execute("SELECT * FROM texts WHERE id BETWEEN 1 and 25")
for row in data:
    sentences_love_test.append(row[3])
    words_love_test.append(row[4])
data = con.execute("SELECT * FROM texts WHERE id BETWEEN 101 and 125")
for row in data:
    sentences_hem_test.append(row[3])
    words_hem_test.append(row[4])

wrong = 0
for i in range(25):
    if words_love_test[i] < k * sentences_love_test[i] + b:
        wrong += 1
    if words_hem_test[i] > k * sentences_hem_test[i] + b:
        wrong += 1
print(wrong)

plt.axis([5, 35, 2, 6])
plt.title('Lovecraft vs. Hemingway')
plt.ylabel('Average word length')
plt.xlabel('Average sentence length')
plt.plot(sentences_love_test, words_love_test, 'ro')
plt.plot(sentences_hem_test, words_hem_test, 'go')
plt.axline([0, b], [-b / k, 0])
plt.show()

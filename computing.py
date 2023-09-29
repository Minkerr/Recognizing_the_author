import sqlite3 as sl
import re

con = sl.connect('TestDB.db')
with con:
    data = con.execute('SELECT * FROM texts')
    for row in data:
        s = str(row[2])
        s = s.translate({ord(i): None for i in ',;\":-—–[](){}“”'})
        s = s.replace('\n', ' ').replace('\r', ' ').replace(' ', ' ')
        sent_len = 0  # summary len of sentences OR number of words
        word_len = 0
        a = re.split("[.!?]", s)  # a is text divided into sentences
        for i in range(len(a)):
            if len(a[i]) == 0:
                continue
            a[i] = a[i].split()  # divide each sentence into words
            sent_len += len(a[i])
            for word in a[i]:
                word_len += len(word)
        sql = """UPDATE texts SET avg_sent = ?, avg_word = ? WHERE id = ?"""
        val = [(sent_len / len(a), word_len / sent_len, row[0])]
        with con:
            con.executemany(sql, val)

#
# !!!!!!!!!!
#
# Here I hae computed all needed data
#
# !!!!!!!!!!
#

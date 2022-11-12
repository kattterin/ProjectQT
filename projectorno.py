import csv
import sqlite3
import datetime as dt

with open('dollar2.csv', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    con = sqlite3.connect('progectkonv.db')
    cur = con.cursor()
    for i in list(reader)[::-1]:
        d = i[0].split('.')
        # print(i[0])
        # print(float(''.join(('.'.join('1 0324.43'.split(','))).split(' '))))
        mis = [float(''.join(('.'.join(x.split(','))).split(' '))) for x in i[1:]]
        cur.execute(
            f"INSERT INTO currency(DAT, US_dollar, Ukrainian_hryvnia, GBP, Japanese_yen, Kazakh_tenge,\
             Australian_dollar, Danish_krone, Canadian_dollar, Norwegian_krone, Singapore_dollar, Turkish_lira,\
              Swiss_frank) VALUES('{dt.date(int(d[2]), int(d[1]), int(d[0]))}', '{float(mis[0])}', '{float(mis[1])}',\
'{float(mis[2])}', '{float(mis[3])}', '{float(mis[4])}', '{float(mis[5])}', '{float(mis[6])}', '{float(mis[7])}',\
'{float(mis[8])}', '{float(mis[9])}', '{float(mis[10])}', '{float(mis[11])}')")

    con.commit()
    con.close()

import time
import yfinance as yf
import sqlite3 as sql
import threading

conn = sql.connect('rate', check_same_thread=False)
cursor = conn.cursor()


def start():
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS `telegram`  (
                  `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  `kind` varchar(255) NOT NULL,
                  `active` varchar(255) NOT NULL,
                  `datetime` datetime(0) NOT NULL DEFAULT '2020-01-01 00:00:00',
                  `value` double(255, 2) NOT NULL,
                  `currency` varchar(255) NULL DEFAULT 'USD'
                );
                 """)
    cursor.execute("""
                DELETE FROM `telegram`;
                """)
    repeat()


def add_stonck(comp_name, now, value, currency):
    cursor.execute("""INSERT INTO telegram (`kind`, `active`, `datetime`, `value`, `currency`)
                    VALUES ('stocks', ?, ?, ?, ?)
                   """, (comp_name, now, value, currency,))
    conn.text_factory = str

    conn.commit()


def viewhistory(active):
    line = ''
    cursor.execute("SELECT `active`,`datetime`,`value`,`currency` FROM telegram WHERE `active`=?", (str(active),))
    rows = cursor.fetchall()
    count = 0
    for row in str(rows):
        if count == 4:
            count = 0
            line += '\n'
            count = count+1
        line += row
    file_1 = open("history.txt", "w")
    file_1.write(line)
    file_1.close()


def viewnow(active):
    line = ''
    cursor.execute("SELECT `value` FROM telegram WHERE `active`=? ORDER BY `id` DESC LIMIT 1", (str(active),))
    rows = cursor.fetchall()

    for row in str(rows):
        line += row
    return line


def view():
    cursor.execute("SELECT * FROM telegram")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def test():
    stocks_rate('TSLA')
    stocks_rate('AAPL')
    stocks_rate('AMZN')
    stocks_rate('MSFT')


def stocks_rate(comp_name):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    stock_price = yf.Ticker(comp_name)
    ask = stock_price.info['ask']
    currency = 'USD'
    add_stonck(comp_name, now, ask, currency)


def repeat():
    threading.Timer(20.0, repeat).start()  # Перезапуск через 20 секунд
    test()
    view()
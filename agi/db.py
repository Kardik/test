#coding: utf-8
import psycopg2
from config import *

dsn = "dbname='{dbname}' user='{dbuser}' " \
      "password='{dbpass}' host='{dbhost}' " \
      "port='{dbport}'".format(dbname=dbname, \
		    dbuser=dbuser, dbpass=dbpass, \
			dbhost=dbhost, dbport=dbport)

def incertrow(name, secondname, number):
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
	
    cur.execute("INSERT INTO Fio (name, secondname, number) VALUES (%s, %s, %s)", \
	            (name, secondname, number))
    conn.commit()
    cur.close()
    conn.close()

def selectrow():
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
	
    cur.execute("SELECT * FROM Fio;")
	
    rows = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    
    return rows

def createtable():
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
	
    try:
        cur.execute("CREATE TABLE Fio (" \
                    "time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, " \
                    "name VARCHAR NOT NULL, " \
                    "secondname VARCHAR NOT NULL, " \
                    "number VARCHAR NOT NULL);")
    except:
        print('Error')
        
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    createtable()
    incertrow("Иванов", "Иван", "79000000000")
    selectrow()
    
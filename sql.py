import mysql.connector as connection
import pandas as pd
from pandas.io import sql
import pymysql
import sqlalchemy


class connectdb:
    def __init__(self) -> None:
        pass
    
    def createdb(self):
        mydb = connection.connect(
            host= 'localhost',
            user= 'root',
            passwd= '1234',
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE date_firme")
        mydb.close()

    def createtable(self):
        mydb = connectdb().connectmydb()
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE firme (DENUMIRE VARCHAR(255), CUI VARCHAR(255), COD_INMATRICULARE VARCHAR(255), EUID VARCHAR(255), STARE_FIRMA VARCHAR(255), ADRESA_COMPLETA VARCHAR(255) ,ADR_TARA VARCHAR(255), ADR_LOCALITATE VARCHAR(255), ADR_JUDET VARCHAR(255), ADR_DEN_STRADA VARCHAR(255), ADR_DEN_NR_STRADA VARCHAR(255), ADR_BLOC VARCHAR(255), ADR_SCARA VARCHAR(255), ADR_ETAJ VARCHAR(255), ADR_APARTAMENT VARCHAR(255), ADR_COD_POSTAL VARCHAR(255), ADR_SECTOR VARCHAR(255), ADR_COMPLETARE VARCHAR(255),SOMETHING VARCHAR(255))")
        mycursor.execute('SET SQL_SAFE_UPDATES = 0')
        mydb.close()
    
    def add_data(self):
        mydb = connectdb().connectmydb()
        mycursor = mydb.cursor()
        table = pd.read_csv('date_firme.csv', sep = '^', names = ['DENUMIRE', 'CUI', 'COD_INMATRICULARE', 'EUID', 'STARE_FIRMA', 'ADRESA_COMPLETA' ,'ADR_TARA', 'ADR_LOCALITATE', 'ADR_JUDET', 'ADR_DEN_STRADA', 'ADR_DEN_NR_STRADA', 'ADR_BLOC', 'ADR_SCARA', 'ADR_ETAJ', 'ADR_APARTAMENT', 'ADR_COD_POSTAL' ,'ADR_SECTOR', 'ADR_COMPLETARE','null','null2']  ,skiprows = [0],encoding='UTF-8' )
        engine = sqlalchemy.create_engine("mysql+pymysql://" + 'root' + ":" + '1234' + "@" + 'localhost' + "/" + 'date_firme')
        table.to_sql(name ='firme', con = engine, if_exists= 'replace',index = 'False')
        mycursor.execute("ALTER TABLE date_firme.firme DROP COLUMN null2;")
        mydb.close()

    def connectmydb(self):
        mydb = connection.connect(
            host='localhost',
            user='root',
            passwd='1234',
            database='date_firme'
        )
        return mydb

    def ExtractSql(self, command):
        mydb = connectdb().connectmydb()
        mycursor = mydb.cursor()
        mycursor.execute(command)
        result = mycursor.fetchall()
        mydb.close()
        return result

    def AddColumn(self):
        mydb = connectdb().connectmydb()
        mycursor = mydb.cursor()
        try:
            mycursor.execute("ALTER TABLE firme ADD TELEFON VARCHAR(255)")
        except:
            print("Coloana exista")
        try:
            mycursor.execute("ALTER TABLE firme ADD EMAIL VARCHAR(255)")
        except:
            print("Coloana exista")



        mydb.close()

    def Do(self, command):
        mydb = connectdb().connectmydb()
        mycursor = mydb.cursor()
        mycursor.execute(command)
        mydb.commit()
        mydb.close()

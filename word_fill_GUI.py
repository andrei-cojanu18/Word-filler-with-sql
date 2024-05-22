import sys
import os
import sql
import word_fill
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QMessageBox, QDialog
from PyQt5 import uic, QtWidgets


class WordfillGUI(QMainWindow):

    changes_list = []

    def __init__(self):
        super().__init__()
        uic.loadUi("wordfill.ui", self)
        self.show()
        self.cui.returnPressed.connect(self.loadData)
        self.Save.clicked.connect(self.save_sql)
        self.tableWidget.itemClicked.connect(self.takecell)
        self.edit_cell.textChanged.connect(self.tablechange)
        self.generate.clicked.connect(self.generate_word)

    def loadData(self):
        try:
            sql.connectdb().createdb()
            sql.connectdb().createtable()
            sql.connectdb().add_data()
        except Exception as e:
            print(e)
            print("DB is already created")
        try:
            sql.connectdb().AddColumn()
        except Exception as e:
            print(e)
        
        connection = sql.connectdb()
        query = f"SELECT * FROM date_firme.firme WHERE CUI LIKE '%{self.cui.text()}%';"
        result = connection.ExtractSql(query)
        self.tableWidget.setRowCount(len(result))

        row = 0
        for item in result:
            self.tableWidget.setItem(
                row, 0, QtWidgets.QTableWidgetItem(item[1]))
            self.tableWidget.setItem(
                row, 1, QtWidgets.QTableWidgetItem(item[2]))
            self.tableWidget.setItem(
                row, 2, QtWidgets.QTableWidgetItem(item[3]))
            self.tableWidget.setItem(
                row, 3, QtWidgets.QTableWidgetItem(item[6]))
            self.tableWidget.setItem(
                row, 4, QtWidgets.QTableWidgetItem(item[21]))
            self.tableWidget.setItem(
                row, 5, QtWidgets.QTableWidgetItem(item[22]))



            row += 1

    def save_sql(self):
        row = self.tableWidget.currentRow()
        print(row)

        connection = sql.connectdb()
        connection.Do('SET SQL_SAFE_UPDATES = 0')
        command = f"""UPDATE date_firme.firme SET DENUMIRE='{self.tableWidget.item(row,0).text()}', 
        COD_INMATRICULARE='{self.tableWidget.item(row,2).text()}',
        ADRESA_COMPLETA='{self.tableWidget.item(row,3).text()}',
        TELEFON = '{self.tableWidget.item(row,4).text()}',
        EMAIL = '{self.tableWidget.item(row,5).text()}'
        WHERE CUI = '{self.tableWidget.item(row,1).text()}'
        """
        connection.Do(command)
        self.loadData()

    def takecell(self):
        row = self.tableWidget.currentRow()
        column = self.tableWidget.currentColumn()
        try:
            self.edit_cell.setText(self.tableWidget.item(row, column).text())
            print(f'{row} {column}')
        except:
            print('Nu exista text in celula')

    def tablechange(self):
        row = self.tableWidget.currentRow()
        column = self.tableWidget.currentColumn()

        self.tableWidget.setItem(
            row, column, QtWidgets.QTableWidgetItem(self.edit_cell.text()))

    def generate_word(self):
        path = QFileDialog.getSaveFileName(
            self, 'Save File', os.getcwd(), 'Microsoft Word files (*.docx *.doc)')
        print(path)
        fill = word_fill.word()
        cui = self.cui.text()
        fill.Generate(cui, path)
        msg = QMessageBox()
        msg.setWindowTitle('Finalizat!')
        msg.setText('Generare finalizata!')
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordfillGUI()
    sys.exit(app.exec_())

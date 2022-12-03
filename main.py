import sys
import csv

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from products import Ui_MainWindow

STAFF_POSTS = ['Кг', 'Шт', 'Л']


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui = Ui_MainWindow
        self.OpenButton.clicked.connect(self.load_table)  # Кнопка: Открытие файла
        self.AddButton.clicked.connect(self.add)  # Кнопка: Добавление записи
        self.DeleteButton.clicked.connect(self.delete)  # Кнопка: Удаление записи
        self.SaveButton.clicked.connect(self.save_file)  # Кнопка: Сохранение данных
        self.PrintButton.clicked.connect(self.find_for_val)  # Кнопка: Вывод информации
        self.ClearButton.clicked.connect(self.resert_filter)  # Кнопка: Очистить таблицу
        self.CmUnit.addItems(STAFF_POSTS)
        self.CmUnitSelect.addItems(STAFF_POSTS)
        self.modeOpen = False
        self.data = None

    def load_table(self):
        # Загрузка таблицы
        with open("Data.csv", newline='', encoding='UTF8') as file:  # Открытие файла
            data = list(csv.reader(file, delimiter=";"))
            self.data = list(data[1:])
            # self.TableProducts.setRowCount(len(data))  # Кол-во строк в таблице
            self.TableProducts.setColumnCount(4)  # Кол-во столбцов в таблице
            self.TableProducts.setHorizontalHeaderLabels(
                ('Название товара', 'цена', 'Ед. измерения', 'Количество'))  # Добавление названий столбцов в таблице
            # Ширина столбцов в таблице
        for i, row in enumerate(data[1:]):
            self.TableProducts.setRowCount(self.TableProducts.rowCount() + 1)
            for j, elem in enumerate(row):
                self.TableProducts.setItem(i, j, QTableWidgetItem(str(elem)))
        self.TableProducts.resizeColumnsToContents()
        self.modeOpen = True

    def add(self):
        # Кнопка: Добавление записи
        if self.modeOpen:  # Если флаг активен, то добавление возможно
            row = [self.LeNameProduct.text(), self.LePrice.text(),self.CmUnit.currentText(),  self.LeCount.text()]
            # Проверка вводимых полей на пустоту
            if row[0] and row[1] and row[2] and row[3] is not None:
                rowCount = self.TableProducts.rowCount()
                self.TableProducts.insertRow(rowCount)
                for i, el in enumerate(row):
                    self.TableProducts.setItem(rowCount, i, QTableWidgetItem(el))
            self.LeNameProduct.setText('')
            self.LePrice.setText('')
            self.CmUnit.itemText(0)
            self.LeCount.setText('')
            self.data.append(row)

    def delete(self):
        # Кнопка: Удаление записи
        if self.TableProducts.rowCount() > 0:
            currentRow = self.TableProducts.currentRow()
            self.TableProducts.removeRow(currentRow)

    def save_file(self, data):
        with open("Data.csv", mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
            file_writer.writerow(["Название товара", "Цена", "Ед.измерения", "Количество"])
            for row in self.data:
                file_writer.writerow(row)



    def clear(self):
        # Кнопка: Очистить таблицу
        self.TableProducts.clear()  # Очистка таблицы
        self.TableProducts.setHorizontalHeaderLabels(
            ('Название товара', 'Цена', 'Ед.измерения', 'Количество'))  # Добавление названий столбцов в таблице

    def find_for_val(self):
        val = self.CmUnitSelect.itemText(self.CmUnitSelect.currentIndex())
        dt = list(filter(lambda row: row[2] == val, self.data))
        self.update_table(dt)

    def update_table(self, data):
        self.TableProducts.setRowCount(0)
        for i, row in enumerate(data):
            self.TableProducts.setRowCount(self.TableProducts.rowCount() + 1)
            for j, elem in enumerate(row):
                self.TableProducts.setItem(i, j, QTableWidgetItem(str(elem)))
        self.TableProducts.resizeColumnsToContents()

    def resert_filter(self):
        self.update_table(self.data)



def run(self):
    self.teResources.setText("OK")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

import sys
import csv

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from main_form import Ui_MainWindow
import datetime as dt

# станции для отправления
STAFF_POSTS = ['Кг', 'Шт', 'Л']

class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pbOpen.clicked.connect(self.open_file)  # Кнопка: Открытие файла
        self.pbInsert.clicked.connect(self.add)  # Кнопка: Добавление записи
        self.pbDelete.clicked.connect(self.delete)  # Кнопка: Удаление записи
        self.SaveButton.clicked.connect(self.save_file)  # Кнопка: Сохранение данных
        self.ClearButton.clicked.connect(self.resert_filter)  # Кнопка: Очистить таблицу
        self.pbFind.clicked.connect(self.find_for_val) # Кнопка: найти
        self.modeOpen = False
        self.data = None

    def open_file(self):
        # Загрузка таблицы
        with open("data.csv", newline='', encoding='UTF8') as file:  # Открытие файла
            data = list(csv.reader(file, delimiter=";"))
            self.data = list(data[1:])
            # self.TableProducts.setRowCount(len(data))  # Кол-во строк в таблице
            self.twStaffs.setColumnCount(6)  # Кол-во столбцов в таблице
            self.twStaffs.setHorizontalHeaderLabels(
                ('Пункт назнач.', 'Пункт отправ.', 'Номер поезда', 'Вр. Отправления', 'Вр. в пути(мин.)',
                 'Станции'))  # Добавление названий столбцов в таблице
            # Ширина столбцов в таблице
        for i, row in enumerate(data[1:]):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        self.modeOpen = True
        self.avg_time()

    def add(self):
        # Кнопка: Добавление записи
        if self.modeOpen:  # Если флаг активен, то добавление возможно
            row = [self.des.text(), self.dep_point.text(), self.num.text(), self.dep_time.text(), self.trav_time.text(),
                   self.station.text()]
            # Проверка вводимых полей на пустоту
            if row[0] and row[1] and row[2] and row[3] and row[4] and row[5] is not None:
                rowCount = self.twStaffs.rowCount()
                self.twStaffs.insertRow(rowCount)
                for i, el in enumerate(row):
                    self.twStaffs.setItem(rowCount, i, QTableWidgetItem(el))
            try:
                self.des.setText('')
                self.dep_point.setText('')
                self.num.setText('0')
                self.dep_time.setTime(dt.time(hour=00, minute=00))
                self.trav_time.setText('')
                self.station.setText('')
                self.data.append(row)
            except Exception as e:
                print(f"туть: {e}")
                return e

    def delete(self):
        # Кнопка: Удаление записи
        if self.twStaffs.rowCount() > 0:
            currentRow = self.twStaffs.currentRow()
            self.twStaffs.removeRow(currentRow)

    def save_file(self, data):
        with open("data.csv", mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
            file_writer.writerow(['Пункт назнач.', 'Пункт отправ.', 'Номер поезда', 'Вр. Отправления', 'Вр. в пути(мин.)',
                 'Станции'])
            for row in self.data:
                file_writer.writerow(row)


    def update_table(self, data):
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()

    def resert_filter(self):
        self.update_table(self.data)


    def avg_time(self):
        try:
            cur = self.data.cursor()
            avg = cur.execute("select avg(time) as avg from staff").fetchone()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.lblAvgAge.setText(f"Среднее время в пути: {round(avg[0], 4)}")


    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_table(f"select * from staff where {col} like '{val}%'")

def run(self):
    self.teResources.setText("OK")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

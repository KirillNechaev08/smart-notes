
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import json

notes = {
    "Инструкция":{
        "Текст": "Очень важный текст :)",
        "Теги":["Легко", "Важно"]
    },

		"Инструкция2":{
        "Текст": "Очень важный текст2 :)",
        "Теги":["Легко2", "Важно2"]
    },
	
}
with open("notes_data.json", "w", encoding="utf-8") as file:
    json.dump(notes, file, ensure_ascii=False)


app = QApplication([])
'''Интерфейс приложения'''
#параметры окна приложения
notes_win = QWidget()
notes_win.setWindowTitle("Умные заметки")
#виджеты окна приложения
list_notes = QListWidget()
list_notes_label = QLabel("Список заметок")

button_note_create = QPushButton("Создать заметку")
button_note_del = QPushButton("Удалить заметку")
button_note_save = QPushButton("Сохранить заметку")
button_tag_add = QPushButton("Добавить тег")
button_tag_del = QPushButton("Удалить тег")
button_tag_search = QPushButton("Искать по тегу")

field_text = QTextEdit()
field_tag = QLineEdit('')
field_tag.setPlaceholderText("Введите тег...")

list_tags = QListWidget()
list_tags_label = QLabel("Список тегов")

main_layout = QHBoxLayout()
L2 = QHBoxLayout()
L3 = QHBoxLayout()
L1 = QVBoxLayout()
L4 = QVBoxLayout()

L2.addWidget(button_note_create)
L2.addWidget(button_note_del)
L3.addWidget(button_tag_add)
L3.addWidget(button_tag_del)

L1.addWidget(list_notes_label)
L1.addWidget(list_notes)
L1.addLayout(L2)
L1.addWidget(button_note_save)
L1.addWidget(list_tags_label)
L1.addWidget(list_tags)
L1.addWidget(field_tag)
L1.addLayout(L3)
L1.addWidget(button_tag_search)
L4.addWidget(field_text)
main_layout.addLayout(L4)
main_layout.addLayout(L1)
notes_win.setLayout(main_layout)

def search():
    tag = field_tag.text()
    if button_tag_search.text() == "Искать по тегу" and tag != "":
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["Теги"]:
                notes_filtered[note] = notes[note]
            button_tag_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать по тегу")
    else:
        pass

        
def add_note():
    note_name, result = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки:")
    if result == True and note_name != "":
        notes[note_name] = {"Текст": "", "Теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["Теги"])
        print(notes)
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)

def add_tag():
    key = list_notes.selectedItems()[0].text()
    if key != "":
        tag_name, result = QInputDialog.getText(notes_win, "Добавить тег", "Название тега:")
        if result == True and tag_name != "":
            notes[key]["Теги"].append(tag_name)
            list_tags.clear()
            list_tags.addItems(notes[key]["Теги"])
            print(notes)
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=False)

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["Теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["Теги"])
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для удаления не выбрана!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        field_text.clear()
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для удаления не выбрана!")

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        a = field_text.toPlainText()
        notes[key]["Текст"] = a
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для сохранения не выбрана!")

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["Текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["Теги"])

button_note_create.clicked.connect(add_note)#bind создание пустой заметки
button_note_del.clicked.connect(del_note)#bind удаление заметки
button_note_save.clicked.connect(save_note)#bind сохранение заметки
list_notes.itemClicked.connect(show_note)#bind клика по заметки для отображения данных
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search)

with open("notes_data.json", "r", encoding="utf-8") as file:
    notes = json.load(file)

list_notes.addItems(notes)

notes_win.show()
app.exec_()



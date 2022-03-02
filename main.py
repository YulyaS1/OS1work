import sys, os, win32api
import requests
import json, zipfile
import xml.etree.ElementTree as et


def info():
    print("\nЛогические диски:", os.getenv("SystemDrive"))
    s = win32api.GetVolumeInformation(str(os.getenv("SystemDrive")) + "\\")
    print("Имя тома: ", s[0], "\n", "Серийный номер тома: ", s[1], "\n", "Файловая система: ", s[-1], sep='')
    print("Размер: ", os.path.getsize(os.getenv("SystemDrive")), "\n")


class Base:
    def create(self, path):
        if os.path.exists(path) == False:
            f = open(path, 'w')
            f.close()
            print("Файл создан")
        else:
            print("Данный файл уже существует")

    def delete(self, path):
        try:
            os.remove(path)
            print("Файл удален")
        except:
            print("Файл не найден")


class File(Base):
    def add_string(self, path, string):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(string + '\n')

    def read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                print(*[line for line in f], sep='')
            print('\n')
        except:
            print("Файл не найден")


class Json(Base):
    def add_object(self, path):
        print("Создаем рандомный объект, выполняем сериализацию и записываем в файл json\n")
        response = requests.get("https://jsonplaceholder.typicode.com/todos").text
        with open(path, 'w') as f:
            f.write(json.dumps(response))  # сериализация и запись в файл объекта

    def read_json(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = ''
                for line in f:
                    data += line
                print(json.loads(data))  # десериализация и вывод в консоль
        except:
            print("Файл не найден")


class Xml(Base):
    def add_xml(self, path, new_data):
        tree = et.parse(path)
        root = tree.getroot()
        root.append(et.fromstring(new_data))
        tree.write(path)

    def read_xml(self, path):
        try:
            tree = et.parse(path)
            root = tree.getroot()
            print(et.tostring(root))
        except:
            print("Файл не найден")

class Zip(Base):
    def create_zip(self, path):
        zfile = zipfile.ZipFile(path, 'w')
        zfile.close()
        print("Архив создан")

    def add_file(self, path):
        new_file = input("Укажите название файла, который хотите добавить: ")
        zfile = zipfile.ZipFile(path, 'a')
        with open(new_file, 'w', encoding='utf-8'):
            zfile.write(new_file)
        os.remove(new_file)
        zfile.close()
        print("Файл добавлен")

    def read_zip(self, path):
        zfile = zipfile.ZipFile(path, 'r')
        print("Файлы: ", zfile.namelist())
        zfile.close()


def main():
    print("Выберите нужный пункт меню:")
    print("1)Вывести информацию в консоль о логических дисках, именах, номере тома, размере и типе файловой системы.")
    print("2)Работа с файлами")
    print("3)Работа с форматом JSON")
    print("4)Работа с форматом XML")
    print("5)Создание zip архива, добавление туда файла")
    choose = int(input())
    main() if choose not in [1, 2, 3, 4, 5, 6] else 1
    if choose == 1:
        info()
        main()
    path = input('Введите название файла/архива [в формате: name.txt/name.json/name.xml...]: ')
    str1 = "\nВыберите нужный пункт меню:\n1)Создать файл\n2)Прочитать файл в консоль\n3)Записать в файл\n4)Удалить файл\n5)Вернуться в главное меню\n"
    if choose == 2:
        file = File()

        def file_choose():
            print(str1)
            try:
                choose2 = int(input())
                file.create(path) if choose2 == 1 else None
                file.read_file(path) if choose2 == 2 else None
                file.delete(path) if choose2 == 4 else None
                main() if choose2 == 5 else None
                if choose2 == 3:
                    string = input("Введите строку: ")
                    file.add_string(path, string)
                file_choose()
            except:
                print("Ошибка! Введите пункт заново!")
                file_choose()

        file_choose()
    if choose == 3:
        file = Json()

        def json_choose():
            print(str1)
            try:
                choose2 = int(input())
                file.create(path) if choose2 == 1 else None
                file.read_json(path) if choose2 == 2 else None
                file.add_object(path) if choose2 == 3 else None
                file.delete(path) if choose2 == 4 else None
                main() if choose2 == 5 else None
                json_choose()
            except:
                print("Ошибка! Введите пункт заново!")
                json_choose()

        json_choose()
    if choose == 4:
        file = Xml()

        def xml_choose():
            print(str1)
            try:
                choose2 = int(input())
                file.create(path) if choose2 == 1 else None
                file.read_xml(path) if choose2 == 2 else None
                file.delete(path) if choose2 == 4 else None
                main() if choose2 == 5 else None
                if choose2 == 3:
                    new_data = input("Введите строку для XML файла(Например: [<OWNER>Colin Wilcox</OWNER>]): ")
                    file.add_xml(path, new_data)
                xml_choose()
            except:
                print("Ошибка!Введите пункт заново!")
                xml_choose()
        xml_choose()
    if choose == 5:
        file = Zip()

        def zip_choose():
            print(
                "\nВыберите необходимый пункт:\n1)Создать архив в формате zip\n2)Добавить файл в архив\n3)Разархировать файл\n4)Удалить файл и архив\n5)Вернуться в главное меню\n")
            try:
                choose2 = int(input())
                file.create_zip(path) if choose2 == 1 else None
                file.add_file(path) if choose2 == 2 else None
                file.read_zip(path) if choose2 == 3 else None
                file.delete(path) if choose2 == 4 else None
                main() if choose2 == 5 else None
                zip_choose()
            except:
                print("Ошибка! Введите пункт заново!")
                zip_choose()

        zip_choose()


if __name__ == "__main__":
    main()
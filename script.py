import re
import os 
import shutil


# временные папки
SOURCE = "__source__" # копия всей музыки
OTHER = "__other__" # одинокие треки

def main():
    main_folder = input("Введите 'имя папки' с музыкой: ")

    out_folder = f"{main_folder}_out"

    # создание шаблона
    os.makedirs( 
        os.path.join(out_folder, SOURCE), 
        exist_ok=True
    )
    # копирование и фильтрация
    copy_and_filter(main_folder, out_folder)
    # удаление дубликатов
    delete_doubles(out_folder)

    # cd ./<name>_out
    os.chdir(out_folder)

    # основной алгоритм перемещения 
    move_files(SOURCE)
    
    # пытаемся найти место для треков из исходной папки, попутно удаляя найденые
    try_find_tracks_for_folders(SOURCE)

    # папки у которых меньше 2ух треков, будут собраны в кучу (в новую папку)
    collect_single_tracks_in_new_folder()

    # продолжаем искать папку для треков, попутна удаляя их из временной папки
    try_find_tracks_for_folders(OTHER)

    # оставшиеся треки во временной папке сгружаем в корень
    # в конце удаляем временную папку 
    move_tracks(OTHER, ".")

    print(f"Success!\nYour sorted music in '{out_folder}'")


def copy_and_filter(main_folder, out_folder):
    """
    Копирует аудио, отбросив папки и другие файлы
    """

    # получаем список музыки
    files = os.listdir(main_folder)
    
    exts = [".mp3", ".ogg", ".wav", ".flac", ".aac", "m4a", "wma", "aif", "aiff", "ape"]

    filtered_files = list()

    # фильтруем
    for ext in exts:
        n = list(filter(lambda file: ext in file, files))
        filtered_files.extend(n)

    # копируем
    for file in filtered_files:
        try:
            src = os.path.join(main_folder,file) # путь до исходного файла
            dst = os.path.join(out_folder, SOURCE, file) # место, куда будет скопирован файл
            shutil.copy(src, dst)
        except Exception as e:
            print(f"Не удалось скопировать файл {file}: {e}")


def delete_doubles(out_dir):
    """
    track.mp3\n
    trach(1).mp3 <- удаляем дубликат
    """
    files = os.listdir(os.path.join(out_dir, SOURCE))

    files = list(filter(lambda x: "(1)." in x ,files))

    for file in files:
        try:
            os.remove(os.path.join(out_dir,SOURCE,file))
        except Exception as e:
            print(f"Не удалось удалить файл {file}: {e}")


def move_files(src):
    files = os.listdir(src)
    for file in files:
        authors = get_authors(file)

        # создание папок по первому автору
        # если в автор не указан, складываем его в папку с именем "_"
        dst = authors[0] if authors[0] else "_"

        if not os.path.exists(dst):
            os.mkdir(dst)

        try:
            path = os.path.join(src,file)
            shutil.copy(path, dst)
        except Exception as e:
            print(f"Не удалось скопировать файл {file}: {e}")



def try_find_tracks_for_folders(src: str): 
    """
    Пытается найти подходящие папки для каждого трека\n
    Если удаётся, перемещает треки из папки - src в найденную
    """

    # имена треков
    files = os.listdir(src)

    for file in files:
        # путь до исходного файла
        fpath = os.path.join(src,file)
        for folder in os.listdir("."):
            authors = get_authors(file)
            if folder in authors:
                if os.path.exists(fpath):
                    try:
                        if not os.path.exists(os.path.join(folder,src,file)): 
                            shutil.move(fpath, os.path.join(folder))
                    except Exception:
                        # если файл уже существует, удаляем его из временного хранения
                        os.remove(fpath)


def collect_single_tracks_in_new_folder():
    """
    Перебирает все папки в корне\n
    Перемещает трек в новую папку, если он единственный в папке\n
    Удаляет папку
    """

    # создание временной папки, куда будут попадать одиночные треки
    if not os.path.exists(OTHER):
        os.mkdir(OTHER)

    # получаем список всех файлов в корне
    any_files = os.listdir(".")
    # нам нужны только папки
    folders = list(filter(lambda file: os.path.isdir(file) ,any_files))

    for folder in folders:
        if len(os.listdir(folder)) < 2:
            files = os.listdir(folder)
            for file in files:
                try:
                    src = os.path.join(folder, file) # ./folder/file
                    shutil.move(src, OTHER)                
                except:
                    # print(f"Не удалось переместить файл во временный каталог __other__")
                    pass

            if len(os.listdir(folder)) == 0:
                os.rmdir(folder)


def move_tracks(src,dst):
    """
    Переместить файлы из одной папки в другую
    """
    files = os.listdir(src)
    for file in files:
        path = os.path.join(src,file)
        if os.path.exists(path):
            try:
                shutil.move(path, dst)
            except:
                # print("Не удалось переместить файл в корень")
                pass

    # удаление папки  
    try:
        shutil.rmtree(src)
    except Exception as e:
        print(f"Ошибка удаления {e}")


# возвращаем список авторов
def get_authors(file: str):
    """
    Предпологается, что трек имеет шаблонный вид:\n
    'Author & Author2 - track name.mp3'\n
    После роаботы этой функции получает: ["Author","Author2"]\n
    разделитель всегда ' - ' (пробел минус пробел)
    """

    authors = re.split(r',\s|\sft\.\s|\sft\s|\sfeat\.\s|\sfeat\s|\s-\s|\s&\s|\sx\s', file)
    authors = [author.strip().lower() for author in authors]

    return authors


if __name__ == "__main__":
    main()
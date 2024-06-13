#!/bin/bash

# Имя проекта и исходный файл
PROJECT_NAME="tmusic"
SCRIPT_NAME="script"
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"

if [[ "$OSTYPE" == "linux-gnu" ]]; then

    # Создание виртуального окружения
    echo "Создание виртуального окружения..."
    python -m venv $VENV_DIR

    # Активация виртуального окружения
    source $VENV_DIR/bin/activate

    # Установка зависимостей
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Установка зависимостей..."
        pip install -r $REQUIREMENTS_FILE
    else
        echo "Файл $REQUIREMENTS_FILE не найден. Пропуск установки зависимостей."
    fi

    # Установка PyInstaller, если он не установлен
    if ! pip show pyinstaller &> /dev/null; then
        echo "Установка PyInstaller..."
        pip install pyinstaller
    fi

    # Создание исполняемого файла
    echo "Создание исполняемого файла..."
    pyinstaller --onefile --name $PROJECT_NAME "$SCRIPT_NAME.py" 

    # Проверка, был ли исполняемый файл создан
    if [ -f "./dist/$PROJECT_NAME" ]; then
        mv "./dist/$PROJECT_NAME" "."
        chmod +x ./$PROJECT_NAME
        echo "Исполняемый файл создан и перемещен в корневую директорию проекта."
    else
        echo "Не удалось создать исполняемый файл. Проверьте журнал ошибок."
        exit 1
    fi

    # Удаление временных файлов
    echo "Очистка временных файлов..."
    rm -rf build
    rm -rf dist
    rm -rf __pycache__
    rm -rf $PROJECT_NAME.spec
    rm -rf venv

    # Деактивация виртуального окружения
    deactivate


    mv "$PROJECT_NAME" "/usr/local/bin"
    cat ./docs/man.txt | gzip > tmusic.1.gz

    mv tmusic.1.gz /usr/share/man/man1
    mandb

    echo "Программа tmusic успешно установлена!"
    echo "Наберите 'man tmusic', чтобы посмотреть, как пользоваться программой"     

else
    echo "Ваша ОС не поддерживается, попробуйте выбрать другой способ установки"
fi
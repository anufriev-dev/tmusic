#!/bin/bash

# Имя проекта и исходный файл
PROJECT_NAME="tmusic"
SCRIPT_NAME="script"
VENV_DIR="venv"
PYTHON=python


# Выбор между python и python3
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Python не найден. Установите Python и попробуйте снова."
    exit 1
fi

# Выбор между pip и pip3
if command -v pip3 &> /dev/null; then
    PIP=pip3
elif command -v pip &> /dev/null; then
    PIP=pip
else
    echo "Pip не найден. Установите pip и попробуйте снова."
    exit 1
fi


# Создание виртуального окружения
echo "Создание виртуального окружения..."
$PYTHON -m venv $VENV_DIR

# Активация виртуального окружения
source $VENV_DIR/bin/activate

# Установка PyInstaller, если он не установлен
if ! $PIP show pyinstaller &> /dev/null; then
    echo "Установка PyInstaller..."
    $PIP install pyinstaller
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

if [ ! -d "/usr/local/bin" ]; then
    mkdir "/usr/local/bin"
fi

mv "$PROJECT_NAME" "/usr/local/bin/"

#!/bin/bash

TPATH="/usr/local/bin/tmusic"

if [ -f "$TPATH" ]; then
    rm "$TPATH"
fi


echo "Программа tmusic успешно удалена!"

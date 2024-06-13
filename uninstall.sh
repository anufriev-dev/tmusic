#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    
    TPATH="/usr/local/bin/tmusic"

    if [ -f "$TPATH" ]; then
        rm "$TPATH"
    fi
    
    MPATH="/usr/share/man/man1/tmusic.1.gz"

    if [ -f "$MPATH"  ]; then
        rm "$MPATH"
        mandb
    fi

    echo "Программа tmusic успешно удалена!"
fi

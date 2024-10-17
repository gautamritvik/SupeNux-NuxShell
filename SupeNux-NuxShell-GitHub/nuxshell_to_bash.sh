#!/bin/bash
while true; do
    echo "Bash Shell (type in 'exit' to return to NuxShell)"
    read -p "$ >>> " cmd
    if [ "$cmd" == "exit" ]; then
        echo "Returning to NuxShell..."
        exit 0
    else
        $cmd 2>&1 | sed 's/^.*: //'
    fi
done

#!/bin/bash
while true; do
    echo "Bash Shell (type in 'exit' to return to NuxShell)"
    read -p "$ >>> " cmd
    if [ "$cmd" == "exit" ]; then
        echo "Returning to NuxShell..."
        exit 0
    else
        bash -c "$cmd" 2>/dev/null || echo "bash: $cmd: command not found"
    fi
done

#/usr/bin/env bash

_comp_fpaste()
{
    local cur prev options
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    options="--debug --title --author --private --clipin --wayland-clipin --clipout --input-selection --fullpath --pasteself --sysinfo --btrfsinfo --printonly --confirm --raw-url"

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${options}" -- ${cur}) )
    else
        _filedir
    fi
    return 0
}


complete -F _comp_fpaste fpaste

# Bash completion for fpaste

_fpaste()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--help --version --fullpath --sysinfo --pasteself --printonly --confirm --private --URL --password -n -l -x -P -U -d -i -o"


    case "${prev}" in
        -x)
            local running=$(for x in "1800" "21600" "86400" "604800" "2592000"; do echo ${x}; done )
            COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
            return 0
            ;;
        -P)
            local running=$(for x in "yes" "no"; do echo ${x}; done )
            COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
            return 0
            ;;
        -l)
            local running=$(for lang in `fpaste -l list`; do echo ${lang}; done)
            COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
            return 0
            ;;
        *)
            ;;
    esac

    COMPREPLY=( $(compgen -W "${opts} $( find . -maxdepth 1 -type f)" -- ${cur}) )
    return 0

}

complete -F _fpaste fpaste


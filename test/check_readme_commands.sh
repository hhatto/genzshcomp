#/bin/bash
GENZSH_BIN="./genzshcomp.py"
COMMANDS=( `echo "gunicorn markdown2 paver pep8 pylint"` )

for command in ${COMMANDS[@]}
do
    ${command} -h | $GENZSH_BIN > /dev/null
    if [ "$?" -eq 0 ]
    then
        echo "OK:" ${command}
    else
        echo "NG:" ${command}
    fi
done

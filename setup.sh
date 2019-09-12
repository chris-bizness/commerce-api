#!/bin/bash

if [[ "$VIRTUAL_ENV" == "" ]]
then
    printf "You are not in a virtual environment. Would you like to continue anyway? [y/N]  "
    read should_continue
    if [[ ${should_continue[1]} != "y" && ${should_continue[1]} != "Y" ]]
    then
        return 1 2>/dev/null || exit 1
    fi
fi

printf "\n\n  ~~  Running the pip install  ~~\n\n"
pip install -U -r requirements/build.txt

printf "\n\n  ~~  Migration time  ~~\n\n"
python manage.py migrate


printf "\n\n        * * *\nGee willy that was easy\n        * * *\n\n"

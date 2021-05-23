#!/usr/bin/env bash
echo "mypy"
mypy --config-file=mypy.ini SMSActivateRU

echo -e "\nflake8"
flake8 --config=.flake8 SMSActivateRU

echo -e "\npylint"
pylint --rcfile=.pylintrc SMSActivateRU
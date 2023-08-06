#!/usr/bin/env bash

#isort -rc -c -df **/*.py && \
check-manifest --ignore ".travis-*" && \
python ./oarepo_heartbeat/libraries.py
#python setup.py test

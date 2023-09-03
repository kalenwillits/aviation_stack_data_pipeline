#!/bin/bash

cp -r ../../include/ .
cp ../../pytest.ini .
docker build -t aviation_stack_load --build-arg AVIATION_STACK_API_KEY .

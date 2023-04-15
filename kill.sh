#!/bin/bash
 #to kill the flask process running at port 5000
 kill -9 `ss -tunlp | grep 5000 |awk '{print $7}'|awk -F "," '{print $2}'| awk -F "=" '{print $2}' `

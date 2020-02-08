#!/bin/bash 

#Original concept https://tinyurl.com/qu4mot7
#$1 should be a path

cat "$1" | gzip | base64

#!/bin/bash

#принимает на вход директорию
#находит все файлы окан. на txt
#заменяет подстроки september на october
#сохраняет бекапы в тех же директориях с именем <старое имя>.bk


echo "Please enter a path to the directory"
read dir
find $dir -name *.txt | while read fname
do
  sed 's/september/october/g' $fname > $(echo "$fname" | sed 's/.txt/.bk/')
done

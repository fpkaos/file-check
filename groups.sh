#!/bin/bash

#создание группы developers с gid 2000
#создание пользователей ivanov, petrov, sidorov (uid 2001, 2002, 2003 соотв.)
#входящих в данную группу

if [ -z $(cat /etc/group | grep developers) ];
then
  groupadd -g 2000 developers
  uids=( [2001]=ivanov [2002]=petrov [2003]=sidorov )
  for i in ${!uids[@]}; do
  useradd -g 2000 -u $i ${uids[$i]}
  done
else
  echo "Group already exists!"
fi

#userdel -r ivanov
#delgroup developers

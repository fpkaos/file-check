#1. Напишите задачу для cron, которая запускает команду 
#/usr/local/bin/do-stuff каждое воскресенье в 11:00 от 
#имени пользователя nobody.

00 11 * * 7 nobody /usr/local/bin/do-stuff 

#2. Напишите задачу для cron, которая запускает команду 
#/usr/local/bin/do-stuff два раза в час 
#от имени пользователя nobody.

30 * * * * nobody /usr/local/bin/do-stuff 

#3.Напишите задачу для cron, которая запускает команду 
#/local/bin/do-stuff каждый час от имени пользователя nobody.

00 * * * * nobody /usr/local/bin/do-stuff 

#4. Напишите задачу для cron, которая запускает команду 
#/usr/local/bin/do-stuff дважды в сутки от имени пользователя nobody.

00 12,00 * * * nobody /usr/local/bin/do-stuff 

#5. Напишите задачу для cron, которая запускает команду 
#/usr/local/bin/do-stuff на 15-й, 28-й, 36- й и 45-й минутах каждого 
#часа от имени пользователя nobody.

15,28,36,45 * * * * nobody /usr/local/bin/do-stuff 

#6. Напишите задачу для cron, которая запускает команду 
#/usr/local/bin/do-stuff каждый день в 02:20 от имени пользователя nobody.

20 2 * * * nobody /usr/local/bin/do-stuff 

#7. Напишите задачу для cron, которая запускает команду 
#/usr/local/bin/do-stuff первого числа каждого месяца от 
#имени пользователя nobody.

00 12 1 * * nobody /usr/local/bin/do-stuff 

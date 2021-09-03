Приложение для нахождения минимальной подсети для заданного набора IP-адресов на Python.
Приложение работает с адресами формата IPv4.

Используемая версия: Python 3.6

Время работы программы: менее 0,0015 секунд.

Способ запуска программы:

1)Перейдите в репозиторий с программой\добавьте программу в рабочий репозиторий. Избегайте кириллических символов в пути к файлам.

2)Добавьте в репозиторий файл с расширением ".txt" и  Запишите в него адреса подсети.
Условия записи для корректной работы:
	1)Записывайте адреса с 1 строки;
	2)На 1 строку записывайте только 1 адрес;
	3)Адреса записывайте в точечно-десятичной нотации.

Пример:

Правильно:
add_list.txt
----------------------------------------------------
192.168.1.2
192.168.1.3
192.168.1.5
----------------------------------------------------

Неправильно:

Список.docx
----------------------------------------------------
192.168.1.2 192.168.1.3 
	11000000,10101000,1,101

----------------------------------------------------

3)Программа запускается через консоль. Для запуска наберите комманду:

Ваш_путь>python main.py *имя_списка_адресов*.txt IPv4
Регистр учитывается.

Результат работы программы выводится в консоль с новой строки в виде:

Result net: *сеть*/*префикс маски*




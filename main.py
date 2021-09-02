#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import os

def check_mistake_argv(argv):
    if argv[1][-4:] == ".txt":
        pass
    else:
        print('Проверьте, в каком формате хранятся адреса. Используйте только ".txt".')
        exit()

    if argv[2] == "IPv4":
        pass
    elif argv[2] == "IPv6":
        print("IPv6 пока не поддерживается. Только IPv4.")
        exit()
    else:
        print("Проверьте правильность ввода типа адресов. IPv4 или IPv6. Регистр учитывется.")
        exit()

    ip_filename = argv[1] #Запись параметра, с именем файла, который хранит список аддресов
    ip_type = argv[2]     #Запсиь параметра, с типом адрессов
    return ip_filename,ip_type

def make_address_list_ipv4(filename):
    try:
        file = open(os.path.abspath(filename))
    except IOError:
        print("Файл не найден. Проверьте правильность ввода.")
        exit()

    pre_address_list = file.read().splitlines() # построковый список адрессов
    file.close()

    address_list = list()
    pre_one_address = list()
    for i in pre_address_list:
        step_list = i.split(".")# разбиваем строки на отдельые значения
        pre_one_address.clear()
        for j in step_list:
            try:
                pre_one_address.append(int(j))# преобразовываем строковые значения в int
            except ValueError:
                print("Проверьте правильность введёных адресов. Ошибка произошла из-за ",j ," значения.")
                exit()
        address_list.append(pre_one_address)# добавляем преобразованный адресс в общий список
    #тут ошибка, в больщой список адресов сохранятеся только последний адрес.
    address_list.sort()
    return address_list
    #теперь мы имееем отсортированный список вида [[192,168,1,3],[192,168,1,4]] и т.д

def roundup(subnetmaskx):# функция округления XOR значений
    if subnetmaskx == 0:
        return 255
    elif subnetmaskx < 2:
        return 254
    elif subnetmaskx < 4:
        return 252
    elif subnetmaskx < 8:
        return 248
    elif subnetmaskx < 16:
        return 240
    elif subnetmaskx < 32:
        return 224
    elif subnetmaskx < 64:
        return 192
    elif subnetmaskx < 128:
        return 128
    elif subnetmaskx < 256:
        return 0
    else:
        return 0

def search_base_address_ipv4(address_list):
    low_address = address_list[0]
    top_address = address_list[-1]

    xor_list = list()
    mask_list = list()
    for i in range(0,3):
        xor_list.append(low_address[i] ^ top_address[i])
    for i in xor_list:
        mask_list.append(roundup(i))

    if mask_list[0] < 255:
        mask_list[1] = 0
        mask_list[2] = 0
        mask_list[3] = 0
    if mask_list[1] < 255:
        mask_list[2] = 0
        mask_list[3] = 0
    if mask_list[2] < 255:
        mask_list[3] = 0

    base_address = list()
    if mask_list[0]<255:
        base_address.append(low_address[0])
        base_address.append(0)
        base_address.append(0)
        base_address.append(0)
    else:
        base_address.append(low_address[0])

    if mask_list[1]< 255:
        base_address.append(low_address[1])
        base_address.append(0)
        base_address.append(0)
    else:
        base_address.append(low_address[1])

    if mask_list[2]< 255:
        base_address.append(low_address[2])
        base_address.append(0)
    else:
        base_address.append(low_address[2])

    if mask_list[3]< 255:
        if mask_list[3] < 2 : base_address.append(1)
        if mask_list[3] < 4 : base_address.append(2)
        if mask_list[3] < 8: base_address.append(4)
        if mask_list[3] < 16: base_address.append(8)
        if mask_list[3] < 32: base_address.append(16)
        if mask_list[3] < 64: base_address.append(32)
        if mask_list[3] < 128: base_address.append(64)
        if mask_list[3] < 256: base_address.append(128)

    dict_mask = {32: [255, 255, 255, 255]
        , 31: [255, 255, 255, 254]
        , 30: [255, 255, 255, 252]
        , 29: [255, 255, 255, 248]
        , 28: [255, 255, 255, 240]
        , 27: [255, 255, 255, 224]
        , 26: [255, 255, 255, 192]
        , 25: [255, 255, 255, 128]
        , 24: [255, 255, 255, 0]
        , 23: [255, 255, 254, 0]
        , 22: [255, 255, 252, 0]
        , 21: [255, 255, 248, 0]
        , 20: [255, 255, 240, 0]
        , 19: [255, 255, 224, 0]
        , 18: [255, 255, 192, 0]
        , 17: [255, 255, 128, 0]
        , 16: [255, 255, 0, 0]
        , 15: [255, 254, 0, 0]
        , 14: [255, 252, 0, 0]
        , 13: [255, 248, 0, 0]
        , 12: [255, 240, 0, 0]
        , 11: [255, 224, 0, 0]
        , 10: [255, 192, 0, 0]
        , 9: [255, 128, 0, 0]
        , 8: [255, 0, 0, 0]
        , 7: [254, 0, 0, 0]
        , 6: [252, 0, 0, 0]
        , 5: [248, 0, 0, 0]
        , 4: [240, 0, 0, 0]
        , 3: [224, 0, 0, 0]
        , 2: [192, 0, 0, 0]
        , 1: [128, 0, 0, 0]
        , 0: [0, 0, 0, 0]}

    for key, value in dict_mask.items():
        if value == mask_list:
            short_mask = key

    return base_address,short_mask




ip_filename,ip_type_v4 = check_mistake_argv(sys.argv)

if ip_type_v4 == "IPv4":
    address_list_ipv4 = make_address_list_ipv4(ip_filename)
    base_address,short_mask = search_base_address_ipv4(address_list_ipv4)
    print("Result net: {}.{}.{}.{}/{}".format(base_address[0],base_address[1],base_address[2],base_address[3],short_mask))







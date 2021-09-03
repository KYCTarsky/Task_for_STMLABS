#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Python ver 3.6.0

import sys
import os
#import time
#start_time = time.time()

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


    address_list = list()
    pre_address_list = list()
    out_address_list=list()
    for line in file:
        address_list.append(line[:-1].split("."))# разбиваем строки на отдельые значения и добавляем в общий список

    for i in address_list:
        for j in i:
                try:
                    pre_address_list.append(int(j))# преобразовываем строковые значения в int
                except ValueError:
                    print("Проверьте правильность введёных адресов. Ошибка произошла из-за ", j," значения в ", i," строке.")
                    exit()
        out_address_list.append(pre_address_list)# добавляем сформированный адрес в общий список
        pre_address_list = list()
    out_address_list.sort()
    file.close()

    return out_address_list
    # теперь мы имееем отсортированный список вида [[192,168,1,3],[192,168,1,4]] и т.д


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

def binary_convert(num):
    if num <= 255:
        pass
    else:
        print(num," не является допустимым значением для преобразования.")
        exit()

    num_bin = format(num,'b')# в двоичное значнение
    if len(num_bin) == 8:
        return num_bin
    else:# len(num_bin) < 10
        return "0"*(8-len(num_bin))+num_bin

def search_mask(address_list):
    low_address = address_list[0]
    top_address = address_list[-1]
    # определяем минимальный и максимальный адрес подсети из списка
    # и на основании этого определяем маску подсети
    xor_list = list()
    mask_list = list()
    for i in range(0, 4):
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
    return mask_list


def base_address(mask,address_list):
    binary_mask = str()
    for i in mask:
        binary_mask += binary_convert(i)

    binary_address = str()
    for i in address_list[0]:
        binary_address += binary_convert(i)

    binary_base_address = str()
    base_address = list()
    for i in range(1,33):
        binary_base_address += str(int(binary_address[i-1]) and int(binary_mask[i-1]))# проводим операцию побитового И и определяем подсеть
        if i % 8 == 0:
            base_address.append(int(binary_base_address, base = 2))# переводим двоичные значения в 10 систему
            binary_base_address = str()
    return base_address

def main():
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
            , 0: [0, 0, 0, 0]}# список масок

    ip_filename,ip_type_v4 = check_mistake_argv(sys.argv)
    if ip_type_v4 == "IPv4":
        address_list_ipv4 = make_address_list_ipv4(ip_filename)
        mask = search_mask(address_list_ipv4)
        address = base_address(mask, address_list_ipv4)
        for key, value in dict_mask.items():
            if value == mask:
                short_mask = key
        print("Result net: {}.{}.{}.{}/{}".format(address[0],address[1],address[2],address[3],short_mask))

if __name__ == "__main__":
    main()
    #print("--- %s seconds ---" % (time.time() - start_time))





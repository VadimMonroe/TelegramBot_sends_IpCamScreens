import os
import sys
import socket
import threading

"""
system arguments variables:
python LAN_check.py level_1 level_2

examples:
python LAN_check.py (empty levels)
python LAN_check.py port 34567
"""
command = None if len(sys.argv) == 1 else sys.argv[1]

socket.setdefaulttimeout(0.9)
print_lock = threading.Lock()

list_of_working_base_ip = []
list_of_working_ip = []
threads = []
ports = []


def port_searching(ip: str, search_port_inner: list) -> None:
    """Проверяем порты конкретного ip (range(0, 65535))"""
    if command == 'port':
        search_port = int(sys.argv[2])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn = s.connect_ex((ip, search_port))
            with print_lock:
                if conn == 0:
                    print(f'{ip} Port {search_port}: OPEN')
                    ports.append(f'{ip}:{search_port}')

            s.close()
        except Exception as E3port:
            print('E3port:', E3port)
    else:
        for i in search_port_inner:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                conn = s.connect_ex((ip, i))
                with print_lock:
                    if conn == 0:
                        print(f'{ip} Port {i}: OPEN')
                        ports.append(f'{ip}:{i}')
                s.close()
            except Exception as E3port:
                print('E3port:', E3port)


def threading_port(ip_list: list, what_port: list):
    """Запускаем параллельный поиск портов в нескольких IP"""
    for _ in ip_list:
        check_ip_port = threading.Thread(target=port_searching, args=[_, what_port])
        check_ip_port.start()
        threads.append(check_ip_port)


def threading_ping(ip: str, ip_list: list) -> None:
    """Параллельная проверка работающих айпишников"""
    a = os.popen(f'ping -c 1 -t 1 {ip}').readlines()
    for _ in a:
        if 'ttl' in _:
            ip_list.append(ip)


def check_base_list(ip_list: list) -> None:
    """Generate all IPs from 192.168.0.1 - 192.168.255.1"""
    for i in range(256):
        base_ip = f'192.168.{i}.1'
        check_ip_thread = threading.Thread(target=threading_ping, args=[base_ip, ip_list])
        check_ip_thread.start()
        threads.append(check_ip_thread)


def check_ip_list(ip_list: list) -> None:
    """Generate all IPs from 192.168....0 - 192.168....255"""
    for _ in list_of_working_base_ip:
        for j in range(256):
            temp = _.split('.')
            temp[3] = str(j)
            check_ip_thread = threading.Thread(target=threading_ping, args=['.'.join(temp), ip_list])
            check_ip_thread.start()


def main(port_search_for: list = range(0, 65535)) -> None:
    print('\033[034mCheck base ip:\033[0m')
    check_base_list(list_of_working_base_ip)
    print(list_of_working_base_ip)
    print('\033[034mCheck next level ip:\033[0m')
    check_ip_list(list_of_working_ip)
    for thread in threads:
        thread.join()
    print(list_of_working_ip)
    print(f'\033[034mCheck ports:\033[0m{port_search_for}')
    threading_port(list_of_working_ip, port_search_for)
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main([34567])
    print(ports)

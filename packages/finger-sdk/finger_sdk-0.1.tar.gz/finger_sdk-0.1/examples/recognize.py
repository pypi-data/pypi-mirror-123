# coding: utf-8
import idc
import idaapi
import idautils
from finger_sdk import client, ida_func
import platform


def recognize_functions(client):
    for func_ea in idautils.Functions():
        pfn = idaapi.get_func(func_ea)
        func_name = idaapi.get_func_name(func_ea)
        func_feat = ida_func.get_func_feature(pfn.start_ea)
        if func_feat:
            func_id, res = client.recognize_function(func_feat)
            if res and res[func_id]:
                func_symbol = res[func_id]
                print("[+]Recognize %s: %s" %(func_name, func_symbol))
            else:
                print("[-]%s recognize failed" %(func_name))
        else:

            print("[-]%s extract feature failed" %(func_name))


def main():
    url = "https://sec-lab.aliyun.com/finger/recognize/"
    headers = {'content-type': 'application/json'}
    timeout = 5
    version = platform.python_version()
    if version.startswith('3'):
        ida_auto.auto_wait()
        my_client = client.Client(url, headers, timeout)
        recognize_functions(my_client)
        ida_pro.qexit(0)
    else:
        Wait()
        my_client = client.Client(url, headers, timeout)
        recognize_functions(my_client)
        Exit(0)


if __name__ == "__main__":
    main()

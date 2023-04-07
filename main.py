import subprocess
import sys
import encryptANDdecrypt
import pathlib
import os
import win32print
import platform

def get_printer():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)

    # 显示为一个菜单
    for i, printer in enumerate(printers):
        print(f"{i+1}. {printer[2]}")

    select = input('请输入要使用的打印机序号：')
    select = int(select)

    return printers[select - 1][2]

def start_printer(cprinter,pdf):
    if sys.platform == 'win32':
        args = [f".\\bin\\PDFtoPrinter.exe",
                f"{pdf}",
                f"{cprinter}",
                ]
        subprocess.run(args, encoding="utf-8", shell=True)
    print(f"\t|已发送至打印机：{cprinter}")

if '__main__' == __name__:
    ead = encryptANDdecrypt.EAD()

    # if 'win' in platform.platform():
    priv = pathlib.Path('X:\\privkey.pem')
    # else:
        # priv = pathlib.Path('')

    while True:
        # print(priv.exists())

        if priv.exists():
            ead.load_keys(priv)
            print('loaded keys')
            break

    # ead.encrypt(pathlib.Path('./target.pdf'), pathlib.Path('./target.encrypt.pdf'))
    ead.decrypt(pathlib.Path('./target.encrypt.pdf'), pathlib.Path('./target.pdf'))
    printer = get_printer()

    start_printer(printer, './target.pdf')

    pathlib.Path('./target.pdf').unlink()

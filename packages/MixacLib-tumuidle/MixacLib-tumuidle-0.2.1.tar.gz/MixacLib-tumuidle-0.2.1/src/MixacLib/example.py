import console.utils
from colorama import Fore
from console import utils
import os

class mcolor():
    def inf(information):
        green = Fore.GREEN
        reset = Fore.RESET
        print('[' + green + '信息' +reset + ']' + information)
        pass

    def debug(debuginf):
        cyan = Fore.CYAN
        reset = Fore.RESET
        print('[' + cyan + '调试' + reset + ']' + debuginf)
        pass

    def warn(warning):
        yellow = Fore.YELLOW
        reset = Fore.RESET
        print('[' + yellow + '警告' + reset + ']' + warning)
        pass

    def error(errorinf):
        red = Fore.RED
        reset = Fore.RESET
        print('[' + red + '错误' + reset + ']' + errorinf)
        pass

    def title(titlestr):
        magenta = Fore.MAGENTA
        reset = Fore.RESET
        print(magenta + titlestr)

    pass

class cons():
    def title(name):
        console.utils.set_title(name)
        color.inf('已设置标题为 {}'.format(name))
        pass
    pass

if __name__ == '__main__':
    pass

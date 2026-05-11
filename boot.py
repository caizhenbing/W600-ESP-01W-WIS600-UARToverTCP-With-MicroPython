# boot.py - PA1 恢复按钮：上电时检测 PA1 是否拉低超过 1 秒
import uos
from machine import Pin
import time

RECOVERY_CODE = '''# main.py - AP + FTP basic
import easyw600, w600, time
easyw600.createap()
time.sleep(2)
w600.run_ftpserver(port=21, username="admin", password="12345")
'''

# ---------- PA1 检测 ----------
def is_recovery_triggered():
    # 尝试两种命名，优先 'PA1'
    for name in ('PA1', 'PA_01'):
        try:
            pin = Pin(name, Pin.IN, Pin.PULL_UP)    # 启用内部上拉
            time.sleep(0.1)                         # 等电平稳定
            if pin.value() == 0:                    # 拉低
                time.sleep(1)                       # 持续 1 秒
                if pin.value() == 0:                # 仍为低
                    return True
            return False
        except:
            continue
    return False

# ---------- 语法/内容检查 ----------
def syntax_ok(filename):
    try:
        f = open(filename, 'r')
        code = f.read()
        f.close()
        compile(code, filename, 'exec')
        return True
    except:
        return False

def has_ap_ftp(filename):
    try:
        f = open(filename, 'r')
        code = f.read()
        f.close()
        return 'easyw600.createap' in code and 'w600.run_ftpserver' in code
    except:
        return False

# ---------- 执行判断 ----------
need_recovery = False

if is_recovery_triggered():
    print("PA1 held low -> recovery")
    need_recovery = True
elif 'main.py' not in uos.listdir():
    print("main.py missing")
    need_recovery = True
else:
    if not syntax_ok('main.py'):
        print("main.py syntax error")
        need_recovery = True
    elif not has_ap_ftp('main.py'):
        print("main.py lacks AP/FTP")
        need_recovery = True
    else:
        print("main.py OK")

if need_recovery:
    with open('main.py', 'w') as f:
        f.write(RECOVERY_CODE)
    print("Recovery main.py written.")

# boot.py - auto-recovery on syntax error OR missing essential commands
import uos
import machine
RECOVERY_CODE = '''# main.py - AP + FTP basic
import easyw600, w600, time
easyw600.createap()
time.sleep(2)
w600.run_ftpserver(port=21, username="admin", password="12345")
'''
def check_syntax(filename):
    try:
        f = open(filename, 'r')
        code = f.read()
        f.close()
        compile(code, filename, 'exec')
        return True
    except SyntaxError:
        return False
    except:
        return False
def has_essentials(filename):
    try:
        f = open(filename, 'r')
        code = f.read()
        f.close()
        return 'easyw600.createap' in code and 'w600.run_ftpserver' in code
    except:
        return False
need_recovery = False
if 'main.py' not in uos.listdir():
    print("main.py missing, creating recovery...")
    need_recovery = True
else:
    if not check_syntax('main.py'):
        print("main.py has syntax error, recovering...")
        need_recovery = True
    elif not has_essentials('main.py'):
        print("main.py lacks AP/FTP commands, recovering...")
        need_recovery = True
    else:
        print("main.py OK, running normally.")
if need_recovery:
    with open('main.py', 'w') as f:
        f.write(RECOVERY_CODE)
    print("Recovery main.py written. Restarting...")
    machine.reset()

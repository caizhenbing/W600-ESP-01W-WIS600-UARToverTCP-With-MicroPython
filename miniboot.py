import uos
uos.remove('main.py')
f = open('main.py', 'w')
f.write('''# main.py - AP hotspot + FTP server
import easyw600
import w600
import time
print("Starting AP mode...")
easyw600.createap()
time.sleep(2)
print("AP ready: W600-AP")
print("Connect to the AP, then use FTP")
print("Starting FTP server on port 21...")
w600.run_ftpserver(port=21, username="admin", password="12345")
''')
f.close()
import machine
machine.reset()

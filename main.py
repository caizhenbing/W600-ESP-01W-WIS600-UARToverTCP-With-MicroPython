# main.py - AP + FTP + UART Bridge (original stable loop)
import w600, network, time, socket, easyw600, gc
from machine import UART, Pin

# ========== AP + FTP ==========
print("AP...")
easyw600.createap()
time.sleep(2)
print("AP: W600-AP")
try:
    w600.run_ftpserver(port=21, username='admin', password='12345')
except:
    pass

# ========== UART 检测（与原代码完全相同） ==========
uart = None
print("Init UART...")

for uart_id in [0, 1]:
    try:
        u = UART(uart_id, 115200)
        u.write(b'U')
        time.sleep(0.1)
        u.read()            # 清空回显
        uart = u
        print("UART%d 可用 (115200)" % uart_id)
        break
    except Exception as e:
        print("UART%d 不可用: %s" % (uart_id, e))

if uart is None:
    print("无可用 UART，桥接将进入 echo 模式")

# ========== TCP 桥接 (5001) ==========
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5001))
s.listen(1)
print("Bridge on port 5001")

while True:
    conn, addr = s.accept()
    conn.setblocking(False)
    print("Client:", addr)
    last = time.time()

    while True:
        # UART → TCP
        if uart:
            try:
                data = uart.read()
                if data and len(data) > 0:
                    conn.send(data)
                    last = time.time()
            except Exception as e:
                print("UART read error:", e)

        # TCP → UART
        try:
            tcp_data = conn.recv(1024)
            if tcp_data:
                # 调试：在串口 REPL 中显示收到的 TCP 数据
                print("TCP -> UART:", tcp_data[:50])
                if uart:
                    try:
                        uart.write(tcp_data)
                        print("Sent to UART OK")
                    except Exception as e:
                        print("UART write error:", e)
                else:
                    conn.send(b"Echo: " + tcp_data + b"\r\n")
                last = time.time()
            else:
                print("Client closed")
                break
        except OSError:
            pass
        except Exception as e:
            print("TCP recv error:", e)
            break

        if time.time() - last > 60:
            print("Idle timeout")
            break
        time.sleep(0.01)

    conn.close()
    gc.collect()
    print("Disconnected")

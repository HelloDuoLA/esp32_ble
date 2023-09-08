import PikaStdLib
import machine 
import bluetooth
import _bluetooth
import const
# import mytest
mem = PikaStdLib.MemChecker()
print('mem used max:')
mem.max()
print('mem used now:')
mem.now()

print('hello PikaPython')


a = bluetooth.BLE()
# b = a.active(1)
# c = a.advertise(0,1,1)

def ble_irq(event,data):
    # event = const._IRQ_CENTRAL_CONNECT
    if event == const._IRQ_CENTRAL_CONNECT:
        # A central has connected to this peripheral.
        print("_IRQ_CENTRAL_CONNECT")
        print(data)
    elif event == const._IRQ_GATTC_SERVICE_DONE:
        print("_IRQ_GATTC_SERVICE_DONE")
        print(data)

    
# a.irq(ble_irq)

# service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
# reader_uuid  = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
# sender_uuid  = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

# services = (
#     (
#         bluetooth.UUID(service_uuid), 
#         (
#             (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY), 
#             (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),
#         )
#     )
#     ,
# )

# a.gatts_register_services(services)

for i in range(65000,70000):
    # b = a.test2(str(i) + "t" * (i % 10))
    # b = a.test2(str(i) + str(70000 - i))
    b = a.test2("ABCDEF")

# a.test(1)
# a.test2()
# a.pyi_active(1)
# b = a.active(1)
# a.advertise(0,1,1)
# a.gap_advertise(20,"adv_data_test")
# c = a.run()
# print(a.gap_name)
# a.pyi_active(1)
# a.config("mac")
# a.active(0)
# a.__test2()
# a.pyi_active()

# girl_tuple = ("a",("b",("c"),"d"),"e")
 
# for everyOne in girl_tuple:
#     print(everyOne)

"""
问题汇总
1. super().func 报错
2. py文件调用.pyi文件会打印返回值 ok
3. pyi文件需要返回字符串、二进制码流如何处理
4. config函数有些参数无法读取
5. 进行BLE失能时,该如何处理


问题汇总
1. nvs_flash_init()这种调用一次的函数应该在哪里调用
2. 启动蓝牙线程任务在哪里调用(已解决)
3. print_addr函数的实现在哪里, 需要怎么样引用
4. 引用头文件失败
5. py文件 elif没通过
6. ESP 的日志没打印出来？
"""


# HR_UUID = bluetooth.UUID("0x180D")
# HR_CHAR = (bluetooth.UUID("0x2A37"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,(("DSCSUUID1",bluetooth.FLAG_READ),("DSCSUUID2",bluetooth.FLAG_READ)))
# HR_SERVICE = (HR_UUID, (HR_CHAR,),)
# UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
# UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,(("DSCSUUID1",bluetooth.FLAG_NOTIFY),("DSCSUUID2",bluetooth.FLAG_READ),("DSCSUUID3",bluetooth.FLAG_INDICATE)))
# UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE,(("DSCSUUID2",bluetooth.FLAG_WRITE),))
# UART_SERVICE = (UART_UUID, (UART_TX, UART_RX))
# SERVICES = (HR_SERVICE, UART_SERVICE,)

# a.gatts_register_services(SERVICES)


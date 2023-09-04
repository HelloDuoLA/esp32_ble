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
b = a.active(1)
a.advertise(0,1,1)

def ble_irq(event,data):
    # event = const._IRQ_CENTRAL_CONNECT
    if event == const._IRQ_CENTRAL_CONNECT:
        # A central has connected to this peripheral.
        print("_IRQ_CENTRAL_CONNECT")
        print(data)
    elif event == const._IRQ_GATTC_SERVICE_DONE:
        print("_IRQ_GATTC_SERVICE_DONE")
        print(data)

    
a.irq(ble_irq)


# a.test(1)
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

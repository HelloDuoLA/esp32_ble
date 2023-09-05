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


service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
reader_uuid  = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
sender_uuid  = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

# services = ((bluetooth.UUID(service_uuid), ((bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY), (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),)), )

# services = (
#     # (
#     #     bluetooth.UUID(service_uuid), 
#     #     # (
#     #     #     (sender_uuid, bluetooth.FLAG_NOTIFY), 
#     #     #     (reader_uuid, bluetooth.FLAG_WRITE),
#     #     # )
#     # )
#     # (12,((13,869),(45,999999),("110")))
#     (12,((bluetooth.UUID(13),869),(45,999999),("110")))
#     ,
# )

print("")
print("")
print("")
# for everyOne in services:
#     if isinstance(everyOne, tuple):
#         for everyTwo in everyOne:
#             print(everyTwo)
#     print(everyOne)

# def print_tuple(tuple1):
#     new_tuple = []
#     for index in tuple1:
#         if isinstance(index, tuple):
#             # 如果元素是元组，则递归处理
#             new_tuple.append(print_tuple(index))
#             # print(index)
#             # print(type(index))
#             # pass
#         elif isinstance(index, bluetooth.UUID) :
#             # 如果元素是整数且大于100，则将其替换为10
#             # new_tuple.append(10)
#             print(index.value)
#             # new_tuple.append(index.value)
#         else:
#             # 其他情况保持不变
#             new_tuple.append(index)
#             print(index)
    
    
#     return tuple(new_tuple)

# print_tuple(services)
# a.gatts_register_services(services)


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

services = (
    (
        bluetooth.UUID(service_uuid), 
        (
            (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY), 
            (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),
        )
    ), 
)
# ab = (bluetooth.UUID("123"),(bluetooth.UUID("3"),8),bluetooth.UUID("1"),2,)

# def fff(d):
#     a = []
#     for i in d :
#         if isinstance(i, bluetooth.UUID) :
#             a.append(i.value)
#             print(i.value)
#         elif isinstance(i, tuple):
#             a.append(fff(i))
#         else:
#             a.append(i)
#             print(i)
#     return tuple(a)

# fff(services)

# services = ((12,((bluetooth.UUID(13),869),(45,999999),("110"))),)

a.gatts_register_services(services)
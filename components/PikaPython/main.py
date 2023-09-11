import PikaStdLib
import machine 
import bluetooth
import _bluetooth
import const
mem = PikaStdLib.MemChecker()

def ble_irq(event,data):
    if event == const._IRQ_CENTRAL_CONNECT:
        print("_IRQ_CENTRAL_CONNECT")
        print(data)
    elif event == const._IRQ_CENTRAL_DISCONNECT:
        print("_IRQ_CENTRAL_DISCONNECT")
        print(data)
    elif event == const._IRQ_GATTS_WRITE :
        print("IRQ_GATTS_WRITE")
        print(data)
    elif event == const._IRQ_GATTS_READ_REQUEST  :
        print("_IRQ_GATTS_READ_REQUEST")
        print(data)
    elif event == const._IRQ_SCAN_RESULT:
        print("_IRQ_SCAN_RESULT data : ")
        print(data)
    elif event == const._IRQ_SCAN_DONE:
        print("_IRQ_SCAN_DONE: ")
        print("data: ",data)
    elif event == const._IRQ_PERIPHERAL_CONNECT:
        print("_IRQ_PERIPHERAL_CONNECT")
        print("data: ",data)
    elif event == const._IRQ_PERIPHERAL_DISCONNECT:
        print("_IRQ_PERIPHERAL_DISCONNECT: ")
        print("data: ",data)
    elif event == const._IRQ_GATTC_SERVICE_RESULT :
        print("_IRQ_GATTC_SERVICE_RESULT")
        print(data)
    elif event == const._IRQ_GATTC_SERVICE_DONE:
        print("_IRQ_GATTC_SERVICE_DONE")
        print(data)
    elif event == const._IRQ_GATTC_CHARACTERISTIC_RESULT:   
        print("_IRQ_GATTC_CHARACTERISTIC_RESULT")
        print(data)
    elif event == const._IRQ_GATTC_CHARACTERISTIC_DONE:    
        print("_IRQ_GATTC_CHARACTERISTIC_DONE")
        print(data)
    elif event == const._IRQ_GATTC_DESCRIPTOR_RESULT:           
        print("_IRQ_GATTC_DESCRIPTOR_RESULT")
        print(data)
    elif event == const._IRQ_GATTC_DESCRIPTOR_DONE  :          
        print("_IRQ_GATTC_DESCRIPTOR_DONE")
        print(data)
    elif event == const._IRQ_GATTC_READ_RESULT      :        
        print("_IRQ_GATTC_READ_RESULT")
        print(data)
    elif event == const._IRQ_GATTC_READ_DONE        :        
        print("_IRQ_GATTC_READ_DONE")
        print(data)
    elif event == const._IRQ_GATTC_WRITE_DONE       :       
        print("_IRQ_GATTC_WRITE_DONE ")
        print(data)
    elif event == const._IRQ_GATTC_NOTIFY           :      
        print("_IRQ_GATTC_NOTIFY ")
        print(data)
    elif event == const._IRQ_GATTC_INDICATE         :          
        print("_IRQ_GATTC_INDICATE ")
        print(data)
    elif event == const._IRQ_GATTS_INDICATE_DONE    :          
        print("_IRQ_GATTS_INDICATE_DONE")
        print(data) 
    elif event == const._IRQ_MTU_EXCHANGED          :           
        print("_IRQ_MTU_EXCHANGED ")
        print(data)
    elif event == const._IRQ_L2CAP_ACCEPT           :           
        print("_IRQ_L2CAP_ACCEPT")
        print(data) 
    elif event == const._IRQ_L2CAP_CONNECT          :           
        print("_IRQ_L2CAP_CONNECT ")
        print(data)
    elif event == const._IRQ_L2CAP_DISCONNECT       :           
        print("_IRQ_L2CAP_DISCONNECT ")
        print(data)
    elif event == const._IRQ_L2CAP_RECV             :           
        print("_IRQ_L2CAP_RECV   ")
        print(data)
    elif event == const._IRQ_L2CAP_SEND_READY       :           
        print("_IRQ_L2CAP_SEND_READY ")
        print(data)
    elif event == const._IRQ_CONNECTION_UPDATE      :          
        print("_IRQ_CONNECTION_UPDATE")
        print(data)
    elif event == const._IRQ_ENCRYPTION_UPDATE      :           
        print("_IRQ_ENCRYPTION_UPDATE")
        print(data)
    elif event == const._IRQ_GET_SECRET             :           
        print("_IRQ_GET_SECRET")
        print(data)
    elif event == const._IRQ_SET_SECRET             :           
        print("_IRQ_SET_SECRET")
        print(data)

print('mem used max:')
mem.max()
print('mem used now:')
mem.now()

print('hello PikaPython')


a = bluetooth.BLE()
b = a.active(1)
b = a.irq(ble_irq)

# 注册服务，服务端
# HR_UUID = bluetooth.UUID("0x180D")
# HR_CHAR = (bluetooth.UUID("0x2A37"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,(("DSCSUUID1",bluetooth.FLAG_READ),("DSCSUUID2",bluetooth.FLAG_READ)))
# HR_SERVICE = (HR_UUID, (HR_CHAR,),)
# UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
# UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,(("DSCSUUID1",bluetooth.FLAG_NOTIFY),("DSCSUUID2",bluetooth.FLAG_READ),("DSCSUUID3",bluetooth.FLAG_INDICATE)))
# UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE,(("DSCSUUID2",bluetooth.FLAG_WRITE),))
# UART_SERVICE = (UART_UUID, (UART_TX, UART_RX))
# SERVICES = (HR_SERVICE, UART_SERVICE,)
# c = a.gatts_register_services(SERVICES)
# print("chrs handle is",c)
# # c = a.gap_advertise(6250)
# a.last_adv_data = "adv_test"
# a.last_resp_data = bluetooth._to_string(bytearray('0x20'))
# c = a.gap_advertise(6250,"adv_test","rsp_test")

# 扫描服务，客户端
# d = a.gap_scan(0, 1280000, 11250, True)
d = a.gap_scan(1000,320000,active=True)
# d = a.gap_scan(1000,320000)
# d = a.gap_scan(1000,320000,active=False)
# addr = bytes([0x0c,0xae,0xb0,0xb6,0xaf,0xa5])
# addr = bytes([0x6c,0xf9,0x87,0xd5,0x49,0x24])
# addr = bytes([0x34,0x85,0x18,0x92,0x0d,0xb6]) # old esp32
addr = bytes([0xec,0xda,0x3b,0x67,0x7a,0x82])  # new eps32 s3
# a.gap_connect(addr,0)

# a.test3(1,0)
# a.gattc_discover_services(1)
# a.gattc_discover_characteristics(1, 6, 9)
# a.gattc_discover_characteristics(1, 10, 23)
a.gattc_discover_characteristics(1, 12, 0xff)
# a.gap_disconnect(1)

# print(a.config("mac"))
# print(a.config("addr_mode"))


# c = a.gap_advertise(6250)
# c = a.gap_advertise(6250)
# a.set_rsp_data(bytes([0x3,0x33,0x11,0x22]) ,4)
# print(bytes([3,33,11,22]))
# a.set_rsp_data("03331122" ,4)
# c = a.gap_advertise(6250,"","")
# a.gap_advertise(None)
# print(c)
# a.test2("data test")




# for i in range(65000,70000):
    # b = a.test2(str(i) + "t" * (i % 10))
    # b = a.test2(str(i) + str(70000 - i))
    # c = 0xABCD
    # b = a.test2(str('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'))
# b = a.test2(0x11111111)
# b = a.test2(0xFFFFFFFF)
# b = a.test2(0xeeeeeeee)
# b = a.test2("ABCDEFAB")

# a = 0xABCDEFEF
# b = hex(a).upper()
# print(b)

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

# 待测试函数
# a.test_call_some_name()

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





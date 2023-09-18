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
        a.gap_advertise(6250)
        print(data)
    elif event == const._IRQ_GATTS_WRITE :
        print("IRQ_GATTS_WRITE")
        print(data)
    elif event == const._IRQ_GATTS_READ_REQUEST  :
        print("_IRQ_GATTS_READ_REQUEST")
        print(data)
        return const._GATTS_NO_ERROR
        # return const._GATTS_ERROR_READ_NOT_PERMITTED
    elif event == const._IRQ_SCAN_RESULT:
        print("_IRQ_SCAN_RESULT")
        if data[2] == 4 :
            print("rsq data : ")
            print(data)
        else:
            print(data)

    elif event == const._IRQ_SCAN_DONE:
        print("_IRQ_SCAN_DONE: ")
        print("data: ",data)
    elif event == const._IRQ_PERIPHERAL_CONNECT:
        print("_IRQ_PERIPHERAL_CONNECT")
        print("data: ",data)
    elif event == const._IRQ_PERIPHERAL_DISCONNECT:
        # a.gap_advertise(6250)
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
    elif event == const._IRQ_GATTC_SUBSCRIBE        :
        print("_IRQ_GATTC_SUBSCRIBE  ")
        print(data)
    elif event == const._IRQ_GATTS_SUBSCRIBE        :
        print("_IRQ_GATTS_SUBSCRIBE  ")
        print(data)

print('mem used max:')
mem.max()
print('mem used now:')
mem.now()

print('hello PikaPython')

a = bluetooth.BLE()
# b = a.active(1)
# b = a.irq(ble_irq)

# 注册服务，服务端
# HR_UUID = bluetooth.UUID(0x180D)
# HR_CHAR = (bluetooth.UUID(0x2A37), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,((bluetooth.UUID(0x3001),bluetooth.FLAG_READ),(bluetooth.UUID(0x3002),bluetooth.FLAG_READ)))
# HR_SERVICE = (HR_UUID, (HR_CHAR,),)
# UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
# UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,((bluetooth.UUID(0x30000001),bluetooth.FLAG_NOTIFY),(bluetooth.UUID(0x30000001),bluetooth.FLAG_READ),(bluetooth.UUID(0x30000002),bluetooth.FLAG_INDICATE)))
# UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE | bluetooth.FLAG_INDICATE,((bluetooth.UUID('6E400006-B5A3-F393-E0A9-E50E24DCCA9E'),bluetooth.FLAG_WRITE),))
# UART_SERVICE = (UART_UUID, (UART_TX, UART_RX))
# SERVICES = (HR_SERVICE, UART_SERVICE,)
# c = a.gatts_register_services(SERVICES)

# 注册服务，服务端
# HR_UUID = bluetooth.UUID(0x180D)
# HR_CHAR = (bluetooth.UUID(0x2A37), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY)
# HR_SERVICE = (HR_UUID,)
# UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
# UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ  | bluetooth.FLAG_NOTIFY | bluetooth.FLAG_INDICATE)
# UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE | bluetooth.FLAG_INDICATE,((bluetooth.UUID('6E400006-B5A3-F393-E0A9-E50E24DCCA9E'),bluetooth.FLAG_WRITE),))
# UART_SERVICE = (UART_UUID, (UART_TX, UART_RX))
# SERVICES = (HR_SERVICE, UART_SERVICE,)
# c = a.gatts_register_services(SERVICES)

# test_char1_UUID =  bluetooth.UUID('33333333-2222-2222-1111-111100000001')
# test_flag1      =  bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
# test_dsc1       = (bluetooth.UUID('34343434-2323-2323-1212-121201010101'),bluetooth.FLAG_DSC_READ )
# test_dsc2       = (bluetooth.UUID('34343434-2323-2323-1212-121201010102'),bluetooth.FLAG_DSC_WRITE)
# test_dscs1      = (test_dsc1,test_dsc2)
# test_char1      = (test_char1_UUID,test_flag1,test_dscs1)

# test_char2_UUID =  bluetooth.UUID('33333333-2222-2222-1111-111100000002')
# test_flag2      =  bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
# test_dsc3       = (bluetooth.UUID('34343434-2323-2323-1212-121201010103'),bluetooth.FLAG_DSC_READ | bluetooth.FLAG_DSC_WRITE)
# test_dscs2      = (test_dsc3,) # 单个的时候,是必须的
# test_char2      = (test_char2_UUID,test_flag2,test_dscs2)

# test_UUID      =  bluetooth.UUID('59462f12-9543-9999-12C8-58B459A2712D')
# test_chars      = (test_char1,test_char2)
# test_service    = (test_UUID, test_chars)
# test_services   = (test_service,)

# c = a.gatts_register_services(test_services)

# len(test_service[1])
# test_char1_UUID =  bluetooth.UUID('33333333-2222-2222-1111-111100000001')
# test_flag1      =  bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
# test_dsc1       = (bluetooth.UUID('34343434-2323-2323-1212-121201010101'),bluetooth.FLAG_READ)
# test_dscs1      = (test_dsc1,)
# test_char1      = (test_char1_UUID,test_flag1,test_dscs1)

# test_UUID      =  bluetooth.UUID('59462f12-9543-9999-12C8-58B459A2712D')
# test_chars      = (test_char1,)
# test_service    = (test_UUID, test_chars)
# test_services   = (test_service,)

# print(a.gatts_register_services(test_services))

# print("chrs handle is",c)
# c = a.gap_advertise(6250)
# print(a.gap_advertise(6250))
# a._last_adv_data = "adv_test"
# a._last_resp_data = bluetooth._to_string(bytearray('0x20'))
# a._last_resp_data = "resp_test"
# e = a.gap_advertise(6250,"adv_test","rsp_test")
# c = a.gap_advertise(6250,"adv","rsp")
# c = a.gap_advertise(6250,"adv","rsp")
# c = a.gap_advertise(6250,bytes("adv"),bytes("rsp"))
# c = a.gap_advertise(6250,bytearray("adv"),bytearray("rsp"))
# c = a.gap_advertise(6250,bytearray("adv"),bytes([0x12,0x34,0x56]))

# 扫描服务，客户端
# d = a.gap_scan(0, 1280000, 11250, True)
# d = a.gap_scan(1000,320000,active=True)
# d = a.gap_scan(1000,320000)
# d = a.gap_scan(1000,320000,active=False)
# addr = bytes([0x0c,0xae,0xb0,0xb6,0xaf,0xa5])
# addr = bytes([0x6c,0xf9,0x87,0xd5,0x49,0x24])
# addr = bytes([0x34,0x85,0x18,0x92,0x0d,0xb6]) # old esp32
addr = bytes([0xec,0xda,0x3b,0x67,0x7a,0x82])  # new eps32 s3
addr = bytes([0xec,0xda,0x3b,0x67,0x7a,0x82])  # new eps32 s3
# a.gap_connect(addr,0)


# a._c2py_dict
# a._py2c_dict
# a._c2value_dict

# a.gatts_read(21)
# a.gatts_write(21,bytes([0x43]))
# a.gatts_write(22,bytes([0x43,0x43]))
# a.gatts_write(20,bytes([0x20,0x20,0x20]))
# a.gatts_write(20,0x12345678)
# a.gatts_write(20,"test")


# a.gatts_notify(1,21,bytes([0x43]))
# a.gatts_notify(1,21,bytes("test"))
# a.gatts_notify(1,21,"test")
# a.gatts_indicate(1,22)

# a.test3(1,0)
# a.gattc_discover_services(1)
# a.gattc_discover_services(1,bluetooth.UUID(bytes([0x18,0x00])))
# a.gattc_discover_services(1,bluetooth.UUID(bytes([0x18,0x01])))

# a.gattc_discover_characteristics(1, 6, 9)
# a.gattc_discover_characteristics(1, 10, 23)
# a.gattc_discover_characteristics(1, 12, 0xff)
# a.gattc_discover_characteristics(1, 1, 0xff)
# a.gattc_discover_characteristics(1, 1, 0xff,bluetooth.UUID(bytes([0x2A,0x00])))

# chr_UUID = bytes([0x33,0x33,0x33,0x33,0x22,0x22,0x22,0x22,0x11,0x11,0x11,0x11,0x00,0x00,0x00,0x00])  # new eps32 s3
# a.gattc_discover_characteristics(1, 1, 0xff,bluetooth.UUID(bytes(chr_UUID)))

# ble_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
# ble_UUID.replace("-","")
# result = [int(ble_UUID[i:i+2],16) for i in range(0, len(ble_UUID), 2)]

# p = b"\x33\x33\x33\x33\x22\x22\x22\x22\x11\x11\x11\x11\x00\x00\x00\x00"
# a.gattc_discover_descriptors(1, 1, 0xff)
# a.gattc_discover_descriptors(1, 23,24)
# a.gap_disconnect(1)

# a.gattc_read(1,8)
# a.gattc_read(1,25)
# a.gattc_write(1,25,"test")
# a.gattc_write(1,8,"test")

# a.gatts_notify(1,25)
# a.gatts_notify(1,25,"indicate_test")

# a.gatts_indicate(1,25)



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



## test
# c = bluetooth.UUID('6E400001-B5A3-F393-E0A9--E50E24DCCA9')


'''
1. 部分函数无法实现

2. 部分函数用不太上

3. 完成对应的profile, micropython中的API不太够用。(时间安排)

4. 句柄与对应值的存储方式

    - 客户端与服务端的句柄不一致

5. 新增描述符支持
'''
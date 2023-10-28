# 不可用
import HeartRate
import bluetooth
import const

a = None
def run():
    HR_sender = HeartRate.Sender()

    UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
    UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ  | bluetooth.FLAG_NOTIFY | bluetooth.FLAG_INDICATE)
    UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE | bluetooth.FLAG_INDICATE,((bluetooth.UUID('6E400006-B5A3-F393-E0A9-E50E24DCCA9E'),bluetooth.FLAG_WRITE),))
    UART_SERVICE = (UART_UUID, (UART_TX, UART_RX))
    # SERVICES = (UART_SERVICE,)

    test_char1_UUID =  bluetooth.UUID('33333333-2222-2222-1111-111100000001')
    test_flag1      =  bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
    test_dsc1       = (bluetooth.UUID('34343434-2323-2323-1212-121201010101'),bluetooth.FLAG_DSC_READ )
    test_dsc2       = (bluetooth.UUID('34343434-2323-2323-1212-121201010102'),bluetooth.FLAG_DSC_WRITE)
    test_dscs1      = (test_dsc1,test_dsc2)
    test_char1      = (test_char1_UUID,test_flag1,test_dscs1)

    test_char2_UUID =  bluetooth.UUID('33333333-2222-2222-1111-111100000002')
    test_flag2      =  bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
    test_dsc3       = (bluetooth.UUID('34343434-2323-2323-1212-121201010103'),bluetooth.FLAG_DSC_READ | bluetooth.FLAG_DSC_WRITE)
    test_dscs2      = (test_dsc3,) # 单个的时候,是必须的
    test_char2      = (test_char2_UUID,test_flag2,test_dscs2)

    test_UUID      =  bluetooth.UUID('59462f12-9543-9999-12C8-58B459A2712D')
    test_chars      = (test_char1,test_char2)
    test_service    = (test_UUID, test_chars)

    UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9F')
    UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9F'), bluetooth.FLAG_READ  | bluetooth.FLAG_NOTIFY | bluetooth.FLAG_INDICATE)
    UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9F'), bluetooth.FLAG_WRITE | bluetooth.FLAG_INDICATE,((bluetooth.UUID('6E400006-B5A3-F393-E0A9-E50E24DCCA9E'),bluetooth.FLAG_WRITE),))
    UART_SERVICE2 = (UART_UUID, (UART_TX, UART_RX))

    SERVICES = (UART_SERVICE,test_service,)
    B = HR_sender.register_services(HeartRate.FLAG_SRV_BSL|HeartRate.FLAG_SRV_APPEND,SERVICES)
    print("handles = ",B)
    HR_sender.adv(62500)

    HR_sender.update_hr(97)
    # HR_sender.update_hr(98)
    # HR_sender._ble.gatts_notify(1,20,23)
    # HR_sender._ble.gatts_notify(1,21)
    # HR_sender._ble.gatts_write(21,HeartRate.SENSOR_LOC_FINGER)
    # HR_sender._ble.gatts_write(20,0x0648)
    # HR_sender._ble.gatts_notify(1,20,[0x06,0x48])
    # HR_sender._ble.gatts_notify(1,20,[0x22,0x48])
    # HR_sender._ble.gatts_write(20,[0x06,0x48],True)
    # HR_sender._ble.gatts_write(21,0)


    # HR_sender._ble._py2c_dict
    # HR_sender._ble._c2py_dict    
    # HR_sender._ble._c2value_dict 

    # TODO:断开蓝牙连接会报错
    # TODO:修改广播名
    # TODO:DEBUG    

    for i in range(256):
        HR_sender._ble.gatts_write(20,[i,99],True)
        # HR_sender._ble.gatts_write(20,[0x06,99],True) # invalid
        # HR_sender._ble.gatts_write(20,[0x08,99],True) # invalid
        # HR_sender._ble.gatts_write(20,[0x09,99],True) # invalid
        # HR_sender._ble.gatts_write(20,[0x0A,99],True) # invalid
        # HR_sender._ble.gatts_write(20,[0x0B,99],True) # invalid
    # F6 F4 F2 F0   
    # import test_HeartRate
    # e = test_HeartRate.run()

# def ble_irq(event,data):
#     if event == const._IRQ_CENTRAL_CONNECT:
#         print("_IRQ_CENTRAL_CONNECT")
#         print(data)
#     elif event == const._IRQ_CENTRAL_DISCONNECT:
#         print("_IRQ_CENTRAL_DISCONNECT")
#         a.gap_advertise(6250)
#         print(data)
#     elif event == const._IRQ_GATTS_WRITE :
#         print("IRQ_GATTS_WRITE")
#         print(data)
#     elif event == const._IRQ_GATTS_READ_REQUEST  :
#         print("_IRQ_GATTS_READ_REQUEST")
#         print(data)
#         return const._GATTS_NO_ERROR
#         # return const._GATTS_ERROR_READ_NOT_PERMITTED
#     elif event == const._IRQ_SCAN_RESULT:
#         print("_IRQ_SCAN_RESULT")
#         if data[2] == 4 :
#             print("rsq data : ")
#             print(data)
#         else:
#             if data[1][0] == 0xec :
#                 print("UUID",bytes(data[1]))
#                 print(bytes(data[4]))   
#     elif event == const._IRQ_SCAN_DONE:
#         print("_IRQ_SCAN_DONE: ")
#         print("data: ",data)
#     elif event == const._IRQ_PERIPHERAL_CONNECT:
#         print("_IRQ_PERIPHERAL_CONNECT")
#         print("data: ",data)
#     elif event == const._IRQ_PERIPHERAL_DISCONNECT:
#         # a.gap_advertise(6250)
#         print("_IRQ_PERIPHERAL_DISCONNECT: ")
#         print("data: ",data)
#     elif event == const._IRQ_GATTC_SERVICE_RESULT :
#         print("_IRQ_GATTC_SERVICE_RESULT")
#         print(data)
#     elif event == const._IRQ_GATTC_SERVICE_DONE:
#         print("_IRQ_GATTC_SERVICE_DONE")
#         print(data)
#     elif event == const._IRQ_GATTC_CHARACTERISTIC_RESULT:   
#         print("_IRQ_GATTC_CHARACTERISTIC_RESULT")
#         print(data)
#     elif event == const._IRQ_GATTC_CHARACTERISTIC_DONE:    
#         print("_IRQ_GATTC_CHARACTERISTIC_DONE")
#         print(data)
#     elif event == const._IRQ_GATTC_DESCRIPTOR_RESULT:           
#         print("_IRQ_GATTC_DESCRIPTOR_RESULT")
#         print(data)
#     elif event == const._IRQ_GATTC_DESCRIPTOR_DONE  :          
#         print("_IRQ_GATTC_DESCRIPTOR_DONE")
#         print(data)
#     elif event == const._IRQ_GATTC_READ_RESULT      :        
#         print("_IRQ_GATTC_READ_RESULT")
#         print(data)
#     elif event == const._IRQ_GATTC_READ_DONE        :        
#         print("_IRQ_GATTC_READ_DONE")
#         print(data)
#     elif event == const._IRQ_GATTC_WRITE_DONE       :       
#         print("_IRQ_GATTC_WRITE_DONE ")
#         print(data)
#     elif event == const._IRQ_GATTC_NOTIFY           :      
#         print("_IRQ_GATTC_NOTIFY ")
#         print(data)
#     elif event == const._IRQ_GATTC_INDICATE         :          
#         print("_IRQ_GATTC_INDICATE ")
#         print(data)
#     elif event == const._IRQ_GATTS_INDICATE_DONE    :          
#         print("_IRQ_GATTS_INDICATE_DONE")
#         print(data) 
#     elif event == const._IRQ_MTU_EXCHANGED          :           
#         print("_IRQ_MTU_EXCHANGED ")
#         print(data)
#     elif event == const._IRQ_L2CAP_ACCEPT           :           
#         print("_IRQ_L2CAP_ACCEPT")
#         print(data) 
#     elif event == const._IRQ_L2CAP_CONNECT          :           
#         print("_IRQ_L2CAP_CONNECT ")
#         print(data)
#     elif event == const._IRQ_L2CAP_DISCONNECT       :           
#         print("_IRQ_L2CAP_DISCONNECT ")
#         print(data)
#     elif event == const._IRQ_L2CAP_RECV             :           
#         print("_IRQ_L2CAP_RECV   ")
#         print(data)
#     elif event == const._IRQ_L2CAP_SEND_READY       :           
#         print("_IRQ_L2CAP_SEND_READY ")
#         print(data)
#     elif event == const._IRQ_CONNECTION_UPDATE      :          
#         print("_IRQ_CONNECTION_UPDATE")
#         print(data)
#     elif event == const._IRQ_ENCRYPTION_UPDATE      :           
#         print("_IRQ_ENCRYPTION_UPDATE")
#         print(data)
#     elif event == const._IRQ_GET_SECRET             :           
#         print("_IRQ_GET_SECRET")
#         print(data)
#     elif event == const._IRQ_SET_SECRET             :           
#         print("_IRQ_SET_SECRET")
#         print(data)
#     elif event == const._IRQ_GATTC_SUBSCRIBE        :
#         print("_IRQ_GATTC_SUBSCRIBE  ")
#         print(data)
#     elif event == const._IRQ_GATTS_SUBSCRIBE        :
#         print("_IRQ_GATTS_SUBSCRIBE  ")
#         print(data)
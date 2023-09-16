import bluetooth

a = bluetooth.BLE()

c = bluetooth.UUID(0x291a)
c = bluetooth.UUID(0x291a123)
c = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
c = bluetooth.UUID(bytearray('6E400001B5A3F393E0A9E50E24DCCA9E'))

c = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9')
c = bluetooth.UUID('6E400001-B5A3-F393-E0A9--E50E24DCCA9')
c = bluetooth.UUID(0x29199999)
value = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
value = '6E400001-B5A3-F393-E0A9-E50E24DCCA9'
value = '6E400001-B5A3-F393-E0A9--50E24DCCA9'
len(value) == 36 and (value[8] == '-') and (value[13] == '-') and (value[18] == '-') and  (value[23] == '-')
c.value


# 广播
# 输入格式判断
c = a.gap_advertise(6250,"adv_test","rsp_test")
c = a.gap_advertise(6250,"adv","rsp")
c = a.gap_advertise(6250,"adv","rsp")
c = a.gap_advertise(6250,bytes("adv"),bytes("rsp"))
c = a.gap_advertise(6250,bytearray("adv"),bytearray("rsp"))
c = a.gap_advertise(6250,bytearray("adv"),bytes([0x12,0x34,0x56]))

# 暂停广播
a.gap_advertise(None)

# 测间隔
a.gap_advertise(625 * 400 ,"adv_test","rsp_test")
a.gap_advertise(625 * 10 ,"adv_test","rsp_test")
a.gap_advertise(625 * 32,"adv_test","rsp_test")
a.gap_advertise(625 * 40 ,"adv_test","rsp_test")
a.gap_advertise(0 ,"adv_test","rsp_test",False)
a.gap_advertise(0)

# 测连接
a.gap_advertise(0 ,"adv_test","rsp_test",False)

# 多次连接广播
a.gap_advertise(0)
a.gap_advertise(625 * 400 ,"adv_test","rsp_test")


#测扫描
a.gap_scan(10000,320000,active=True)
a.gap_scan(10000,320000,active=False)

# 无限扫描
a.gap_scan(0,320000,active=True)
a.gap_scan(0,320000,active=False)

# 停止扫描
a.gap_scan(None)

# 多次扫描
a.gap_scan(10000,320000,active=True)
a.gap_scan(10000,320000,active=False)

# 测connect
a.gap_scan(1000,320000,active=False)
addr = bytes([0xec,0xda,0x3b,0x67,0x7a,0x82])  # new eps32 s3
a.gap_connect(addr,0)


addr = bytes([0xec,0xda,0x3b,0x67,0x7a,0x82])  # new eps32 s3
addr = [0xec,0xda,0x3b,0x67,0x7a]  # new eps32 s3


a.gap_disconnect(1)
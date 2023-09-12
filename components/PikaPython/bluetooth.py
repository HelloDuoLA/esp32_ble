import _bluetooth
# 标志位
FLAG_BROADCAST = 0x0001
FLAG_READ      = 0x0002
FLAG_WRITE_NO_RESPONSE = 0x0004
FLAG_WRITE     = 0x0008
FLAG_NOTIFY    = 0x0010
FLAG_INDICATE  = 0x0020
FLAG_AUTHENTICATED_SIGNED_WRITE = 0x0040

FLAG_AUX_WRITE           = 0x0100
FLAG_READ_ENCRYPTED      = 0x0200
FLAG_READ_AUTHENTICATED  = 0x0400
FLAG_READ_AUTHORIZED     = 0x0800
FLAG_WRITE_ENCRYPTED     = 0x1000
FLAG_WRITE_AUTHENTICATED = 0x2000
FLAG_WRITE_AUTHORIZED    = 0x4000

class UUID():
    value  = ""
    def __init__(self,value):
        self.value =  UUID_to_bytes(value)

class BLE(_bluetooth.BLE):

    last_adv_data  = ""  #广播内容
    last_resp_data = ""  #回应扫描内容
    addr_mode      =  0  #地址类型 BLE_OWN_ADDR_PUBLIC,BLE_OWN_ADDR_RANDOM,BLE_OWN_ADDR_RPA_PUBLIC_DEFAULT,BLE_OWN_ADDR_RPA_RANDOM_DEFAULT
    callback_func  = None  #回调函数

    def __init__(self):
        print("BLE init")
        # a = super().__init__()
        a = self.init()
        self.setCallback(self.ble_callback)
    
    def test(self, interval_us, adv_data=None, resp_data=None, connectable=True):
        if isinstance(adv_data,bytes) :
            print( "neirong " ,_to_string(adv_data), "size" ,len(_to_string(adv_data)))
        print(type(adv_data))
    
    def test2(self, data):
        # print("num  " ,num)
        # print("len num ", len(num))
        # num_str = _to_string(num)
        # print("num_str : ", num_str)
        # return self.pyi_test2(num_str,len(num_str))
        # if interval_us == None :
        # print(interval_us)
        # print(adv_data)
        # print(resp_data)
        # print(connectable)
        # a.test2(2, resp_data = "resp_data")
        self.pyi_test2(data,len(data))


    def test3(self,connhandle,valuehandle):
        return self.pyi_test3(connhandle,valuehandle)
    
    def test_call_some_name(self):
        super().test_call_some_name()  
    
    def active(self):
        self.pyi_active()

    def active(self,active_flag):
        if (active_flag > 0 or active_flag == True):
            return self.pyi_active(True)
        elif (active_flag == 0 or active_flag == False):
            return self.pyi_active(False)

    def config(self, *param_name, **kv): # a.config(mac="1123",gap_name="test")
    # 获取参数属性   a.config("mac")
        first_param = param_name[0]
        if first_param == "mac":
            return (self.config_addr_mode_get(),self.config_mac_get())
        elif first_param == "addr_mode":
            return self.config_addr_mode_get()
        elif first_param == "gap_name":
            return self.config_gap_name_get()
        elif first_param == "rxbuf" :
            self.config_addr_rxbuf_get()
        elif first_param == "mtu" :
            self.config_mtu_get()
        elif first_param == "bond" :
            self.config_bond_get()
        elif first_param == "mitm" :
            self.config_mitm_get()
        elif first_param == "io":
            self.config_io_get()
        elif first_param == "le_secure":
            self.config_le_secure_get()
        else:
            print("ValueError: unknown config param")   

    # 设置参数
        if "mac" in kv:
            return self.config_mac_update(kv["mac"])

        if ("addr_mode" in kv):
            return self.config_addr_mode_update(kv["addr_mode"])

        if ("gap_name" in kv):
            return self.config_gap_name_update(kv["gap_name"])

        if ("rxbuf" in kv):
            return self.config_rxbuf_update(kv["rxbuf"])

        if ("mtu" in kv):
            return self.config_mtu_update(kv["mtu"])

        if ("bond" in kv):
            return self.config_bond_update(kv["bond"])

        if ("mitm" in kv):
            return self.config_mitm_update(kv["mitm"])

        if ("bond" in kv):
            return self.config_mac_update(kv["bond"])

        if ("io" in kv):
            return self.config_io_update(kv["io"])

        if ("le_secire" in kv):
            return self.config_le_secire_update(kv["le_secire"])
    # a.config("mac"="test","gap_name"="test2")

    # 回调事件处理函数
    def irq(self,func):
        # self.setCallback(func)
        self.callback_func = func

    def ble_callback(self,data):
        # TODO:memoryview没有实现
        self.callback_func(data[0],data[1:])

    # 完成
    def gap_advertise(self, interval_us, adv_data=None, resp_data=None, connectable=True):
        if interval_us is None: 
            print("interval_us is None\r\n")
            return self.stop_advertise()
        else :
            # 设置广播载荷
            if adv_data is None: #参数为空，则使用上次数据
                adv_data = self.last_adv_data
            else :
                self.last_adv_data = _to_string(adv_data)

            # 设置响应载荷
            if resp_data is None:
                resp_data = self.last_resp_data
            else :
                self.last_resp_data = _to_string(resp_data)
                # print(self.last_resp_data)
                print(resp_data)

            return self.advertise(self.addr_mode,int(interval_us/625),connectable,self.last_adv_data,len(self.last_adv_data),self.last_resp_data,len(self.last_resp_data))

    # active的作用是接受扫描响应数据
    # """
    # 使用interval_us和window_us可选择配置占空比。扫描器将每interval_us微秒运行window_us 微秒，
    # 总共持续duration_ms毫秒。默认间隔和窗口分别为 1.28 秒和 11.25 毫秒（后台扫描）。
    # """
    def gap_scan(self, duration_ms, interval_us=1280000, window_us=11250, active=False):
        if duration_ms is None :
            return self.gap_stop_disc()
        else:
            # print("duration=%d,interval_us=%d, window_us=%d, active=" %( duration_ms,interval_us,window_us),active)
            print("active=",active)
            return self.gap_disc(self.addr_mode, duration_ms,int(interval_us/625),int(window_us/625),active)

    def gap_connect(self,peer_addr,peer_addr_type, scan_duration_ms=2000):
        return self.pyi_gap_connect(peer_addr,peer_addr_type ,scan_duration_ms)

    def gap_disconnect(self, conn_handle):
        return self.pyi_gap_disconnect(conn_handle)

    def gatts_register_services(self, services):
        convert_services = _convert_ble_service_info(services)
        print("convert_services  : ",convert_services)
        return self.gatts_register_svcs(convert_services)
        # return convert_services

    def gatts_read(self,value_handle):
        # 暂不清楚对照哪个函数,或者直接调用gattc试一试
        pass

    def gatts_write(self,value_handle, data, send_update=False):
        # 暂不清楚对照哪个函数
        pass

    def gatts_notify(self,conn_handle, value_handle, data=None):
        if data is None:
            self.gatts_notify_no_data(conn_handle, value_handle)
        else :
            self.gatts_notify_custom(conn_handle, value_handle,data)


    def gatts_indicate(self,conn_handle, value_handle,data=None):
        if data is None:
            self.gatts_indicate_no_data(conn_handle, value_handle)
        else :
            self.gatts_indicate_custom(conn_handle, value_handle,data)

    def gatts_set_buffer(self,value_handle, len, append=False):
        # 暂不清楚对照哪个函数
        pass

    def gattc_discover_services(self,conn_handle, uuid:UUID=None):
        if uuid == None:
            return self.gattc_dis_svcs(conn_handle)
        else :
            return self.gattc_dis_svcs_by_uuid(conn_handle,uuid.value,len(uuid.value))

    def gattc_discover_characteristics(self,conn_handle, start_handle, end_handle, uuid:UUID=None):
        if uuid == None:
            return self.gattc_dis_chrs(conn_handle,start_handle,end_handle)
        else :
            return self.gattc_dis_chrs_by_uuid(conn_handle, start_handle, end_handle,uuid.value,len(uuid.value))

    def gattc_discover_descriptors(self,conn_handle, start_handle, end_handle):
        return self.gattc_dis_dscs(conn_handle,start_handle, end_handle)

    def gattc_read(self,conn_handle, value_handle):
        return self.pyi_gattc_read(conn_handle, value_handle)

    def gattc_write(self,conn_handle, value_handle, data, mode = 0):
        if mode == 0:
            return self.gattc_write_with_no_rsp(conn_handle, value_handle, data, len(data))
        elif mode == 1:
            return self.gattc_write_with_rsp(conn_handle, value_handle, data,len(data))

    def gattc_exchange_mtu(self,conn_handle):
        self.pyi_gattc_exchange_mtu(conn_handle)
        pass

# 将UUID类型转换为字符串
def _convert_ble_service_info(data):
    new_tuple = []
    for i in data :
        if isinstance(i,UUID) :
            new_tuple.append(i.value)
            # print(i.value)
        elif isinstance(i, tuple):
            new_tuple.append(_convert_ble_service_info(i))
        else:
            new_tuple.append(i)
            # print(i)
    return tuple(new_tuple)

# 将数据转为字符串格式
def _to_string(data):
    data_str = ""
    if isinstance(data,bytes):
        data_str = data.decode()
    elif isinstance(data,bytearray):
        data_str = data.decode()
    elif isinstance(data,str):
        data_str = data
    elif isinstance(data,int):
        data_str = hex(data)[2:]

def UUID_to_bytes(value:UUID):
    value_bytes = ""
    if isinstance(value,bytes):
        value_bytes = value
    elif isinstance(value,bytearray): #貌似没有太好的方式转到bytes上
        value_bytes = value.decode()
    elif isinstance(value,str):
        value_str = value.replace("-","")
        value_bytes = bytes([int(value_str[i:i+2],16) for i in range(0, len(value_str), 2)])
    elif isinstance(value,int): # 65535 
        value_bytes = bytes([value])

    return value_bytes
    
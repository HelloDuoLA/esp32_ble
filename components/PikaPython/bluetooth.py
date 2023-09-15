import _bluetooth
# 特性标志位
FLAG_BROADCAST = 0x0001
FLAG_READ      = 0x0002
FLAG_WRITE_NO_RESPONSE = 0x0004
FLAG_WRITE     = 0x0008
FLAG_NOTIFY    = 0x0010
FLAG_INDICATE  = 0x0020
FLAG_AUTHENTICATED_SIGNED_WRITE = 0x0040

# 描述符标志位
FLAG_DSC_READ           = 0x01
FLAG_DSC_WRITE          = 0x02
FLAG_DSC_READ_ENC       = 0x04
FLAG_DSC_READ_AUTHEN    = 0x08
FLAG_DSC_READ_AUTHOR    = 0x10
FLAG_DSC_WRITE_ENC      = 0x20
FLAG_DSC_WRITE_AUTHEN   = 0x40
FLAG_DSC_WRITE_AUTHOR   = 0x80

FLAG_AUX_WRITE           = 0x0100
FLAG_READ_ENCRYPTED      = 0x0200
FLAG_READ_AUTHENTICATED  = 0x0400
FLAG_READ_AUTHORIZED     = 0x0800
FLAG_WRITE_ENCRYPTED     = 0x1000
FLAG_WRITE_AUTHENTICATED = 0x2000
FLAG_WRITE_AUTHORIZED    = 0x4000

class UUID():
    value  = ""
    _UUID_bits = ""
    def __init__(self,value):
        self.value,self._UUID_bits = UUID_to_bytes(value)
    


class BLE(_bluetooth.BLE):
    # 所有实例共享
    def __init__(self):
        print("BLE init")
        # a = super().__init__()
        self.last_adv_data  = ""  #广播内容
        self.last_resp_data = ""  #回应扫描内容
        self.addr_mode      =  0  #地址类型 BLE_OWN_ADDR_PUBLIC,BLE_OWN_ADDR_RANDOM,BLE_OWN_ADDR_RPA_PUBLIC_DEFAULT,BLE_OWN_ADDR_RPA_RANDOM_DEFAULT
        self.callback_func  = None  #回调函数

        self._basic_value_handle = 20
        self._py2c_dict = {}
        self._c2py_dict = {}
        self._c2value_dict = {}
        self.conn_handles = [] 
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
    
    def test4(self,data):
        # print(data[0],data[1],data[2])
        print(data[0],data[1])
        return 0
    
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
        event_id = data[0]
        # print("event_id",event_id)
        # print("data  ",data[1])
        if event_id > 100 :      #自定义回调事件
            if event_id == 101 : # 建立句柄映射 
                ble_value_handles = data[1]
                length = len(ble_value_handles)
                for i in range(length):
                    # py 映射 c handle
                    key =  self._basic_value_handle + i
                    value = ble_value_handles[i] 
                    self._py2c_dict[str(key)] = value 

                    # c 映射 py handle
                    self._c2py_dict[str(value)] = key

                    # c handle 映射 value, 默认值为空
                    self._c2value_dict[str(value)] = ""
            elif event_id == 102: #nimble蓝牙协议栈读属性 TODO:回调函数没反应
                print("data1",data[1])
                buf = self._c2value_dict[str(data[1])]
                print("buf " ,buf)
                return len(buf),buf
                # return bytes([99])
        else: 
            if event_id == 3: # write
                self._c2_change_value(data[2], data[3])
                data = data[:3]
            if event_id == 4: #read 请求
                rc = self.callback_func(event_id,data[1:])
                value = -99
                length   = -99
                if rc == 0:   #允许读
                    value = self._c2value(data[2]) 
                    length = len(value)
                return rc,length,value
            return self.callback_func(event_id,data[1:])

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
            
            # if resp_data is None and adv_data is None and interval_us is not None:
            #     self.advertise_continue()

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
        # print("convert_services  : ",convert_services)

        offset = 0
        chr_list = _count_chrs(services)
        all_chr_count = 0
        new_list1 = []

        # 计算pyhandle返回值
        # 计算chr总数量
        for i in range(len(chr_list)):
            new_list2 = []
            all_chr_count += chr_list[i]
            for j in range(chr_list[i]):
                value_handle = self._basic_value_handle + offset
                new_list2.append(value_handle)
                # self._py2c_dict[str(value_handle)] = -99
                offset += 1
            new_list1.append(new_list2)

        rc = self.gatts_register_svcs(convert_services,all_chr_count)
        
        if rc < 0 :
            return rc
        
        return tuple(new_list1) 

    # TODO:待验证
    def gatts_read(self,value_handle):
        return self._py2value(value_handle)

    # TODO:待验证
    def gatts_write(self,value_handle, data, send_update=False):
        if send_update == False:
            return self._py2_change_value(value_handle,data)
        else : 
            self._py2_change_value(value_handle,data)
            self.gatts_chr_updated(value_handle)
        

    def gatts_notify(self,conn_handle, value_handle, data=None):
        value = ""
        if data is None:
            value = self._py2value(value_handle)
            c_value_handle = self._py2c_dict[str(value_handle)]
        else :
            if isinstance(data,bytes): #TODO:关注一下数据类型
                value = data
            elif isinstance(data,int):
                value = bytes([data])
            else:
                value = bytes(data)
        c_value_handle = self._py2c_dict[str(value_handle)]
        self.pyi_gatts_notify(conn_handle, c_value_handle,value,len(value))


    def gatts_indicate(self,conn_handle, value_handle,data=None):
        value = ""
        if data is None:
            value = self._py2value(value_handle)
            c_value_handle = self._py2c_dict[str(value_handle)]
        else :
            if isinstance(data,bytes): 
                value = data
            elif isinstance(data,int):
                value = bytes([data])
            else:
                value = bytes(data)
        c_value_handle = self._py2c_dict[str(value_handle)]
        self.pyi_gatts_indicate(conn_handle, c_value_handle,value,len(value))

    def gatts_set_buffer(self,value_handle, len, append=False):
        # TODO:暂不清楚对照哪个函数
        pass

    def gattc_discover_services(self,conn_handle, uuid:UUID=None):
        if uuid == None:
            return self.gattc_dis_svcs(conn_handle)
        else :
            return self.gattc_dis_svcs_by_uuid(conn_handle,uuid.value,len(uuid.value))

    def gattc_discover_characteristics(self,conn_handle, start_handle, end_handle, uuid:UUID=None):
        if uuid == None:
            return self.gattc_diss(conn_handle,start_handle,end_handle)
        else :
            return self.gattc_diss_by_uuid(conn_handle, start_handle, end_handle,uuid.value,len(uuid.value))

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

    # 通过C handle找值 
    def _c2value(self, handle):
        return self._c2value_dict[str(handle)]
        # return self._c2value_dict["25"]
    
    # 通过PY handle找值
    def _py2value(self,handle):
        c_handlue = self._py2c_dict[str(handle)]
        return self._c2value(c_handlue)
        # return self._c2value(25)
    
    # 通过C handle 改值
    def _c2_change_value(self,handle,value):
        self._c2value_dict[str(handle)] = value
        return 0

    # 通过py handle 改值    
    def _py2_change_value(self,handle,value):
        c_handlue = self._py2c_dict[str(handle)]
        return self._c2_change_value(c_handlue,value)
        
# 将UUID类型转换为字符串
def _convert_ble_service_info(data):
    new_list = []
    for i in data :
        if isinstance(i,UUID) :
            new_list.append(i.value)
            new_list.append(i._UUID_bits)
            # print(i.value)
        elif isinstance(i, tuple):
            new_list.append(_convert_ble_service_info(i))
        else:
            new_list.append(i)
            # print(i)
    return tuple(new_list)

def _count_chrs(srvs_tuple):
    srv_count = len(srvs_tuple)
    # print("srv_count",srv_count)
    # print("srvs_tuple", srvs_tuple)
    chr_count = [] # 每个服务的特性数量
    for i in range(srv_count):
        # srv_tuple = srvs_tuple[i]
        # print("srv_tuple ", srv_tuple )
        # chrs_tuple = srv_tuple[]
        chr_count.append(len(srvs_tuple[i][1]))
        # print("chrs_tuple",chrs_tuple)
    return chr_count

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
    value_bytes = []
    if isinstance(value,bytearray): #貌似没有太好的方式转到bytes上
        value_bytes = value.decode()
    elif isinstance(value, bytes):
        value_bytes = value
    elif isinstance(value,str):
        value_str = value.replace("-","")
        # print(value_str)
        # value_bytes = bytes([int(value_str[i:i+2],16) for i in range(0, len(value_str), 2)])
        value_list = []
        for i in range(0, len(value_str), 2):
            value_list.append(int(value_str[i:i+2],16))
        value_bytes = bytes(value_list)

    elif isinstance(value,int): # 65535 
        value_list = []
        if value >= 0 and value < 65536 : #8 bit uuid
            value_list.append(int(value/256))
            value_list.append(value%256)
        elif value >= 0 and value < 65536 * 65536:
            value_list.append(int(value/(65536 * 256)))
            value_list.append(int((value%(65536 * 256))/65536))
            value_list.append(int((value%(65536))/256))
            value_list.append((value%(256)))

        value_bytes = bytes(value_list)
    
    UUID_bits = len(value_bytes)
    # print(value_bytes)
    return value_bytes,UUID_bits



    
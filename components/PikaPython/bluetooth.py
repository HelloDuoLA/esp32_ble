import _bluetooth
# 需要额外注意类型转换

class BLE(_bluetooth.BLE):
    last_adv_data  = ""  #广播内容
    last_resp_data = ""  #回应扫描内容
    addr_mode      =  0  #地址类型 BLE_OWN_ADDR_PUBLIC,BLE_OWN_ADDR_RANDOM,BLE_OWN_ADDR_RPA_PUBLIC_DEFAULT,BLE_OWN_ADDR_RPA_RANDOM_DEFAULT
    conn_handle    = ""  #连接句柄
    gap_name     = "nimble"  #蓝牙名称
    # def __init__(self):
        # super().__init__()
        # pass
    
    def test(self):
        super().pyi_test()
    
    def __test2(self):
        print("test2")

    def active(self):
        self.pyi_active()

    def active(self,active_flag):
        if (active_flag > 0 or active_flag == True):
            return self.pyi_active(True)
        elif (active_flag == 0 or active_flag == False):
            return self.pyi_active(False)

    # 获取参数属性, 暂时先不用管    
    def config(self,param_name, /):
        if(param_name=="mac"):
            return(super().config_addr_mode_get(),super().config_mac_get())
        elif(param_name=="addr_mode"):
            super().config_addr_mode_get()
        elif(param_name=="gap_name"):
            super().config_addr_gap_name_get()
        elif(param_name=="rxbuf"):
            super().config_addr_rxbuf_get()
        elif(param_name=="mtu"):
            super().config_mtu_get()
        elif(param_name=="bond"):
            super().config_bond_get()
        elif(param_name=="mitm"):
            super().config_mitm_get()
        elif(param_name=="io"):
            super().config_io_get()
        elif(param_name=="le_secure"):
            super().config_le_secure_get()
        else:
            print("ValueError: unknown config param")

    # 设定属性
    def config(self,*, mac,addr_mode,gap_name,rxbuf,mtu,bond,mitm,io,le_secire=False):
        if mac != None:
            super().config_mac_update(mac)
        
        if addr_mode != None:
            if (addr_mode >= 0 and addr_mode < 5):
                # super().config_addr_mode_update(addr_mode)
                self.addr_mode = addr_mode
                return True
            else :
                return False

        if gap_name != None:
            self.gap_name = gap_name
            return super().config_gap_name_update(self.gap_name)

        if rxbuf != None:
            super().config_rxbuf_update(rxbuf)

        if mtu != None:
            super().config_mtu_update(mtu)
        
        if bond != None:
            super().config_bond_update(bond)

        if mitm != None:
            super().config_mitm_update(mitm)

        if io != None:
            if(io >= 0 and io < 5 ):
                super().config_io_update(io)

        if le_secire != None:
            super().config_le_secire_update(le_secire)

    
    # 回调事件处理函数
    def irq(func):
        super().setCallback(func)

    # """
    # interval_us:广告间隔时间, 为none则停止广播
    # adv_data: 包含在所有广播中, 是任何实现缓冲协议的类型(例如bytes, bytearray, str)
    # resp_data: 被发送以响应主动扫描, 是任何实现缓冲协议的类型(例如bytes, bytearray, str)

    # """
    def gap_advertise(self, interval_us, adv_data=None, *, resp_data=None, connectable=True):
        # 设置广播载荷
        if adv_data is None:
            adv_data = self.last_adv_data
        else :
            self.last_adv_data = adv_data
            super().set_adv_data(adv_data,len(adv_data))

        # 设置响应载荷
        if resp_data is None:
            resp_data = self.last_resp_data
        else :
            self.last_resp_data = resp_data
            super().set_rsp_data(resp_data,len(resp_data))

        # 停止广播
        if interval_us is None: 
            return super().stop_advertise()
        else :
            return super().gap_advertise(self.addr_mode,interval_us,connectable)

    # #TODO:active的作用是什么意思
    # """
    # 使用interval_us和window_us可选择配置占空比。扫描器将每interval_us微秒运行window_us 微秒，
    # 总共持续duration_ms毫秒。默认间隔和窗口分别为 1.28 秒和 11.25 毫秒（后台扫描）。
    # """
    def gap_scan(self, duration_ms, interval_us=1280000, window_us=11250, active=False, /):
        if duration_ms is None :
            super().gap_stop_scan()
        elif (duration_ms == 0):
            super().gap_scan()
        else:
            super().gap_scan_forever()

    # """
    # micropython:直接输入时间

    # nimble: 按照单位算时间
    # duration:  

    # """
    # def gap_scan(self, duration_ms, interval_us=1280000, window_us=11250, active=False, /):
    #     if duration_ms is None :
    #         super.gap_stop_scan()
    #     else:
    #         duration = duration_ms / 10
    #         super.gap_scan(duration_ms, interval_us, window_us, active)

    def gap_connect(self, addr_type, addr, scan_duration_ms=2000, /):
        super().gap_connect(addr_type, addr,scan_duration_ms)
        pass

    def gap_disconnect(self, conn_handle, /):
        super().gap_disconnect()
        pass

    def gatts_register_services(self, services_definition, /):
        for service in services_definition:
            service_uuid, characteristics = service
    
    
    # # 遍历特征
    # for characteristic in characteristics:
    #     char_uuid, flags = characteristic
    #     print(f"Characteristic UUID: {char_uuid}")
    #     print(f"Flags: {flags}")
    #     super.register_a_service()


    def gatts_read(value_handle, /):
        pass

    def gatts_write(value_handle, data, send_update=False, /):
        pass

    def gatts_notify(conn_handle, value_handle, data=None, /):
        pass

    def gatts_indicate(conn_handle, value_handle, /):
        pass

    def gatts_set_buffer(value_handle, len, append=False, /):
        pass

    def gattc_discover_services(conn_handle, uuid=None, /):
        pass

    def gattc_discover_characteristics(conn_handle, start_handle, end_handle, uuid=None, /):
        pass

    def gattc_discover_descriptors(conn_handle, start_handle, end_handle, /):
        pass

    def gattc_read(conn_handle, value_handle, /):
        pass

    def gattc_write(conn_handle, value_handle, data, mode=0, /):
        pass

    def gattc_exchange_mtu(conn_handle, /):
        pass


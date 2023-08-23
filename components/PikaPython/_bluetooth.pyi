from PikaObj import *

class BLE:
    def __init__(self) -> None: ...

    def test(self):
        pass
    
    def active(self):
        pass
    
    def stop_advertise(self) -> int:
        pass
    
    def set_adv_data(self, data:str, data_len: int ) -> int :
        pass 

    def set_rsp_data(self, data:str, data_len: int ) -> int :
        pass

    def gap_connect(self, addr_type : int, addr : str ,scan_duration_ms : int64) -> int :
        pass

    def gap_disconnect(self) -> int :
        pass

    # def config():
    #     pass

    # def irq():
        # pass

    def gap_advertise(interval_us, adv_data=None,resp_data=None, connectable=True):
        pass

    def gap_stop_scan() -> int:
        pass
    
    def register_a_service(service_info : tuple) -> int:
        pass

    def gap_scan(self, duration_ms:int, interval_us:int, window_us:int, active:bool) -> int:
        pass

    def config_name_update(gap_name:str) -> int:
        pass





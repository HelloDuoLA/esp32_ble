import bluetooth
IBEACON_SENDER   =    0
IBEACON_RECEIVER =    1

# class iBeacon():
#     def __init__(self,):

class Sender():
    def __init__(self) -> None:
        self.UUID  = bytes([0xFD, 0xA5, 0x06, 0x93, 0xA4, 0xE2, 0x4F, 0xB1, 0xAF, 0xCF, 0xC6, 0xEB, 0x07, 0x64, 0x78, 0x25])
        self.Major = 0
        self.Minor = 0
        self.ble = bluetooth.BLE()

    def active(self,active_flag = None):
        if active_flag == None:
            return self.ble.pyi_check_active()
        else:
            if (active_flag > 0 or active_flag == True):
                return self.ble.pyi_active(True)
            elif (active_flag == 0 or active_flag == False):
                return self.ble.pyi_active(False)
    
    def config(self,*param_name, **kv):
        try:
            self.ble._check_active()
        except:
            raise OSError
        
        first_param = param_name[0]
        if first_param == "UUID":
            pass
        elif first_param == "Major":
            return self.Major
        elif first_param == "Minor":
            return
        else:
            raise KeyError
        
        if "UUID" in kv:
            value  = kv["UUID"]
            self.UUID = kv["UUID"]
        
        if "Major" in kv:
            self.Major = kv["Major"]

        if "Minor" in kv:
            self.Minor = kv["Minor"]

        return 0
    
    def adv(self):
        try:
            self.ble._check_active()
        except:
            raise OSError


    def _input2UUID(self,value):
        UUID = bluetooth.UUID(value)
        return UUID
    
    def _input2UINT16(self,value):
        if isinstance(value,int):
            if value > 0 and value < 65535:
                return value
            else :
                raise ValueError
        else:
            raise ValueError
    


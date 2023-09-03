import PikaStdLib
import machine 
import bluetooth
import _bluetooth
# import mytest
mem = PikaStdLib.MemChecker()
print('mem used max:')
mem.max()
print('mem used now:')
mem.now()

print('hello PikaPython')
a = bluetooth.BLE()
# a.pyi_active(1)
b = a.active(1)
# a.advertise(1,1,1)
# c = a.run()
# print(a.gap_name)
# a.pyi_active(1)
# a.config("mac")
# a.active(0)
# a.__test2()
# a.pyi_active()

"""
问题汇总
1. super().func 报错
2. py文件调用.pyi文件会打印返回值 ok
3. pyi文件需要返回字符串、二进制码流如何处理
4. config函数有些参数无法读取
5. 进行BLE失能时,该如何处理


问题汇总
1. 在哪里进行初始化比较好
2. 启动蓝牙线程任务在哪里调用
3. print_addr函数的实现实在哪里, 需要怎么样引用
4. 引用头文件失败
"""

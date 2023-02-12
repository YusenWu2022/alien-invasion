import time
class Clock():  #结构体是可变参数，但是纯粹的数字是不可变参数，所以传要改变的参数必须打包进结构体
    def __init__(self):
        self.time=time.perf_counter()
        
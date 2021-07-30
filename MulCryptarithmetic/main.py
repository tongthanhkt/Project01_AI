import function
import threading
import time
import os


def calculator():
    start_time = time.time()
    set_variable, X, C = function.initCSP()
    print(X)
    print(C)
    assignment = {}
    if set_variable == "NO SOLUTION":
        function.writeOutput(assignment, False)
    else:
        flag = function.backtrackingSearch(assignment, X, C)
        print(assignment)
        function.writeOutput(assignment, flag)
    print("--- %s seconds ---" % (time.time() - start_time))
    os._exit(0)


def delayM():
    time.sleep(600)                     # Setting thoi gian (tham so-> thoi gian)
    print("Chay qua thoi gian")
    os._exit(0)


class ThreadBeforeTime (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      calculator()                      # Thuc thi luong truoc thoi gian setting


class ThreadAfterTime (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      delayM()                          # Thuc thi luong sau thoi gian setting


# Create new threads
threadBeforeTime = ThreadBeforeTime()   # Khoi tao luong thuc thi truoc thoi gian setting
threadAfterTime = ThreadAfterTime()     # Khoi tao luong thuc thi sau thoi gian setting
# Start Threads
threadBeforeTime.start()
threadAfterTime.start()
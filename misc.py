from threading import Thread
# import threading

myVar = 0
myVarOld = 0

def fun(num):
    global myVar
    for i in range(10):
        print(f"{' '*num}{num+i}")
        myVar = num+i

ts = [Thread(target=fun, args=(i,)) for i in range(100)]
for t in ts: t.start()
for t in ts: t.join()


myDict = {1:1, 2:1, 3:2}

def fib(num):
    global myDict
    if num not in myDict.keys():
        myDict[num] = fib(num-1) + fib(num-2)
        def myFun(num):
            pass
    return myDict[num]

print(fib(100))




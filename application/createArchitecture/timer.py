from threading import Timer

def hello():
    print("hello, world")

x = input()
t = Timer(int(x), hello)
t.start() # after 30 seconds, "hello, world" will be printed

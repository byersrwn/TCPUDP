import threading
import client
import importlib.util
def main():
    arg1 = 'localhost'
    arg2 = '8080'
    arg3 = 'TCP'
    arg4 = 'send'
    spec = importlib.util.spec_from_file_location("client", "client.py")
    clientScript = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(clientScript)
    list = []
    list2 = []
    # for i in range (1, 1000): #send 100 messages
    #     list.append(threading.Thread(target=client.main, args=(arg1, arg2, arg3, arg4, "msgFolder/msg" + str(i) + ".txt")))
    #     # threading.Thread(target=client.main, args=(arg1, arg2, arg3, arg4, "msgFolder/msg" + str(i) + ".txt")).start()
    # for i in range (1, 1000):
    #     list[i].start()
    # for i in range (1, 1000):
    #     list2.append(threading.Thread(target=client.main, args=(arg1, arg2, arg3, "receive", i)))
    # for i in range (1, 1000):
    #     list2[i].start()
        

def createMsgs():
    for i in range (100,1000):
        name = "msg" + str(i) + ".txt"
        f = open(name, "w")
        f.write("This is message number " + str(i))
        f.close()


if __name__ == "__main__":
    main()


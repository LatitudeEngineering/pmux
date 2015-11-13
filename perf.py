import zmq
import time
from multiprocessing import Process, Pipe

def test_str(n):
    _str = ""
    for i in range(n):
        _str += "a"
    return _str


SIZE = 2 ** 26



#################################
##  multiprocessing
#################################
def mp_test():

    def client(conn):
        payload = test_str(SIZE)
        count = 0
        start = time.time()
        try:
            while True:
                conn.send(payload)
                conn.recv()
                count +=1
        except:
            pass
        finally:
            end = time.time()
            total = end - start
            print 'total: ', count
            print 'took: ', total
            print 'req / sec:', count / total
            print 'bandwidth: %f MBps' % (((count / total) * SIZE) / 2 ** 20)
            conn.close()

    def server(conn):
        try:
            while True:
                conn.recv()
                conn.send('ok')
        except:
            pass
        finally:
            conn.close()

    ps,pc = Pipe()
    proc_serv = Process(target=server, args=(ps,))
    proc_serv.start()
    proc_client = Process(target=client, args=(pc,))
    proc_client.start()

    while True:
        time.sleep(1)

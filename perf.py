import zmq
import time
from multiprocessing import Process, Pipe

def test_str(n):
    _str = ""
    for i in range(n):
        _str += "a"
    return _str

#################################
##  ZeroMQ
#################################
def zmq_server(endpoint):
    ctx = zmq.Context(io_threads=2)
    s = ctx.socket(zmq.REP)
    s.bind('ipc://' + endpoint)
    #s.bind('tcp://127.0.0.1:9001')
    try:
        while True:
            s.recv_string()
            s.send_string('ok')
    finally:
        s.close()
        ctx.destroy()


def zmq_client(endpoint):
    ctx = zmq.Context(io_threads=2)
    s = ctx.socket(zmq.REQ)
    s.connect('ipc://' + endpoint)
    #s.connect('tcp://127.0.0.1:9001')
    count = 0

    payload = test_str(2 ** 1)

    start = time.time()
    try:
        while True:
            s.send_string(payload)
            s.recv_string()
            count += 1
    finally:
        end = time.time()
        total = end - start
        print 'total: ', count
        print 'took: ', total
        print 'req / sec:', count / total
        s.close()
        ctx.destroy()


def mp_test():

    def client(conn):
        payload = test_str(2 ** 1)
        count = 0
        start = time.time()
        try:
            while True:
                conn.send(payload)
                conn.recv()
                count +=1
        finally:
            end = time.time()
            total = end - start
            print 'total: ', count
            print 'took: ', total
            print 'req / sec:', count / total
            conn.close()

    def server(conn):
        try:
            while True:
                conn.recv()
                conn.send('ok')
        finally:
            conn.close()

    ps,pc = Pipe()
    proc_serv = Process(target=server, args=(ps,))
    proc_serv.start()
    proc_client = Process(target=client, args=(pc,))
    proc_client.start()

    while True:
        time.sleep(1)

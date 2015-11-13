import zmq
import time
from multiprocessing import Process, Pipe
from nanomsg import Socket, PAIR
import nnpy

def test_str(n):
    _str = ""
    for i in range(n):
        _str += "a"
    return _str


SIZE = 2 ** 26


#################################
##  ZeroMQ
##  1.7GBps, IvyBridge laptop, 1MB messages
##  3.75GBps, IvyBridge laptop, 64MB messages
#################################
def zmq_server(endpoint):
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.REP)
    s.bind('ipc://' + endpoint)
    #s.bind('ipc://127.0.0.1:9001')
    try:
        while True:
            s.recv(copy=False)
            s.send('ok', copy=False)
    except:
        pass
    finally:
        s.close()
        ctx.destroy()


def zmq_client(endpoint):
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.REQ)
    s.connect('ipc://' + endpoint)
    #s.connect('ipc://127.0.0.1:9001')
    count = 0

    payload = test_str(SIZE)

    start = time.time()
    try:
        while True:
            s.send(payload, copy=False)
            s.recv(copy=False)
            count += 1
    except:
        pass
    finally:
        end = time.time()
        total = end - start
        print 'total: ', count
        print 'took: ', total
        print 'req / sec:', count / total
        print 'bandwidth: %f MBps' % (((count / total) * SIZE) / 2 ** 20)
        s.close()
        ctx.destroy()


#################################
##  Nanomsg
#################################
def nano_server(endpoint):
    s = Socket(PAIR)
    s.bind('ipc://' + endpoint)
    #s.bind('tcp://127.0.0.1:9001')
    try:
        while True:
            s.recv()
            s.send('ok')
    finally:
        s.close()


def nano_client(endpoint):
    s = Socket(PAIR)
    s.connect('ipc://' + endpoint)
    #s.connect('tcp://127.0.0.1:9001')
    count = 0

    payload = test_str(SIZE)

    start = time.time()
    try:
        while True:
            s.send(payload)
            s.recv()
            count += 1
    except:
        pass
    finally:
        end = time.time()
        total = end - start
        print 'total: ', count
        print 'took: ', total
        print 'req / sec:', count / total
        print 'bandwidth: %f MBps' % (((count / total) * SIZE) / 2 ** 20)
        s.close()


#################################
##  nnpy
#################################
def nn_server(endpoint):
    s = nnpy.Socket(nnpy.AF_SP, nnpy.PAIR)
    #s.bind('ipc://' + endpoint)
    s.bind('tcp://127.0.0.1:9001')
    try:
        while True:
            s.recv()
            s.send('ok')
    finally:
        s.close()


def nn_client(endpoint):
    s = nnpy.Socket(nnpy.AF_SP, nnpy.PAIR)
    #s.connect('ipc://' + endpoint)
    s.connect('tcp://127.0.0.1:9001')
    count = 0

    payload = test_str(SIZE)

    start = time.time()
    try:
        while True:
            s.send(payload)
            s.recv()
            count += 1
    except:
        pass
    finally:
        end = time.time()
        total = end - start
        print 'total: ', count
        print 'took: ', total
        print 'req / sec:', count / total
        print 'bandwidth: %f MBps' % (((count / total) * SIZE) / 2 ** 20)
        s.close()


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

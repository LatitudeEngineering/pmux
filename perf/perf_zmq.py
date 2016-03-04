import perf
import time
import zmq


SIZE = perf.SIZE
test_str = perf.test_str

#################################
##  ZeroMQ
##  1.7GBps, IvyBridge laptop, 1MB messages
##  3.75GBps, IvyBridge laptop, 64MB messages
#################################
def zmq_server(endpoint):
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.REP)
    #s.bind('ipc://' + endpoint)
    s.bind(endpoint)
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
    #s.connect('ipc://' + endpoint)
    s.connect(str(endpoint))
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

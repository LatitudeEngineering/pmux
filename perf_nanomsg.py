from nanomsg import Socket, PAIR
import time
import perf


SIZE = perf.SIZE
test_str = perf.test_str


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

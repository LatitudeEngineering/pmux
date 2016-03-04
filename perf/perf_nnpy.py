import perf
import time
import nnpy

SIZE = perf.SIZE
test_str = perf.test_str

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

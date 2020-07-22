from multiprocessing import Pool
import multiprocessing
import time


def f(x, y):
    print('calc')
    test = 3**3000000
    print('donecalc')

if __name__ == '__main__':
    cores = multiprocessing.cpu_count()
    elements = 12

    print('parallel...')
    start = time.time()
    with Pool(processes=cores) as pool:
        pool.starmap(f, [(i, i) for i in range(elements)])
    parallel_time = time.time() - start

    print('\n' + 'serial...')
    start = time.time()
    for i in range(elements):
        f(i, i)
    serial_time = time.time() - start

    print('\nresults...')
    overhead = parallel_time - serial_time/6
    print('parallel: ' + str(parallel_time))
    print('serial: ' + str(serial_time))
    print('estimated overhead: ' + str(overhead))
    if serial_time < parallel_time:
        print('no advantage')
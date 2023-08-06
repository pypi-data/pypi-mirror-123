import multiprocessing as mp
from typing import List, Callable, Iterable


class Task:
    """
    task helper.
    constructor:
        task (Callable): Callable object.
    usage:
    """
    def __init__(self, task: Callable):
        self._task = task

    def run(self, argument: Iterable):
        try:
            return self._task(*argument)
        except Exception as e:
            return e


class Pool:
    """
    multiprocessing.Pool helper
    constructor:
        task (Task): Task object.
        arguments (Iterable[Iterable]):arguments list.
        parallel (int): parallel
    usage:
        from slimhelper.parallel_helper import Pool, Task
        def test(a: int, b: str):
            print(a, b)
            return str(a)+b
        p1 = (1, 'a')
        p2 = (2, 'b')
        p3 = (3, 'c')
        task = Task(test)
        params = (p1, p2, p3, p1, p2, p3)
        pool = Pool(task, params, 2)
        r = pool.start()
        print(r)
    """
    def __init__(self, task: Task, arguments: Iterable[Iterable], parallel: int):
        self._task = task
        self._arguments = arguments
        self._parallel = parallel


    def start(self) -> Iterable:
        with mp.Pool(self._parallel) as pool:
            return pool.map(self._task.run, self._arguments)

def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

# Инициализация переменной вызова глобальной функции
funcRuns = 0

# Упаковка функции во враппере мемоизации
@memoize
def f(x):
  global funcRuns

  # Увеличение funcRuns при каждом запуске функции
  funcRuns += 1
  return True

# Инициализация списка чисел
nums = [0,1,2,3,4,4]

# Запуск спискового включения с двумя вызовами f(x) на каждую итерацию
#   с 6 элементами в списке и 2 вызовами за итерацию, что
#   приведет к 12 выполнениям функций.
[f(x) for x in nums if f(x)]

# Запуск номера журнала f(x)
print(funcRuns)
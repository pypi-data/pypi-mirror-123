import matplotlib.pyplot as plt
import matplotlib_iterm2
import time
import random

def hist(a, number_of_columns):
    min_val, max_val = min(a), max(a)
    step = (max_val - min_val) / number_of_columns
    value_counts = [0] * number_of_columns
    
    for el in a:
        column = int((el - min_val) // step)
        if column == number_of_columns:
            column -= 1
        value_counts[column] += 1 
    
    bins_names = [min_val + i * step for i in range(number_of_columns + 1)]
    return value_counts, bins_names

def draw_hist(a):
    number_of_columns = len(set(a))
    value_counts, bins_names = hist(a, number_of_columns)
    plt.bar(bins_names[:-1], value_counts, width = 0.7, bottom = 0, align = 'edge')


def test():
    n = 1000000
    a = [random.randint(1, 1000) for i in range(n)]
    start_time = time.time()
    draw_hist(a)
    plt.show()
    my_time = time.time() - start_time
    print("___Custom fast draw_hist takes %s seconds___" % my_time)
    start_time = time.time()
    plt.hist(a, bins = len(set(a)), width = 0.7)
    plt.show()
    plt_time = time.time() - start_time
    print("___Standart plt.hist takes %s seconds___" % plt_time)


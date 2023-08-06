import seaborn as sns
import numpy as np


def plot(left, right, step_num, f):
    diff = right - left
    if step_num < diff:
        argv = np.arange(left, right, step_num)
    else:
        argv = np.linspace(left, right, step_num)
    sns.lineplot(x=argv, y=[f(i) for i in argv])

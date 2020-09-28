import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
#creating a subplot 
ax1 = fig.add_subplot(1,1,1)

def animate(_):
    data = open('stock.txt','r').read()
    lines = data.split('\n')
    lines.pop(-1)
    xs = []
    ys = []

    for line in lines:
        x, y = line.split(',') # Delimiter is comma
        xs.append(float(x))
        ys.append(float(y))

    ax1.clear()

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Live graph with matplotlib')
    plt.scatter(xs, ys)

if __name__ == "__main__":
    inp = read_and_strip(file_name="small_input.txt")

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
    print(inp)

import matplotlib.pyplot as plt

def line_plot(title, data, x, xlabel, y, ylabel):
    x_values = [item[x] for item in data]
    y_values = [item[y] for item in data]
    _, ax = plt.subplots()
    ax.plot(x_values, y_values)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    # ax.grid()
    plt.show()

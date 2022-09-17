import matplotlib.pyplot as plt

def line_plot(title, data, x, xlabel, y, ylabel):
    """
    Realiza un gráfico de línea para los datos especificados.
    """
    x_values = [item[x] for item in data]
    y_values = [item[y] for item in data]
    fig, ax = plt.subplots()
    fig.figure.set_size_inches(10, 5)

    ax.plot(x_values, y_values, linewidth=2)
    ax.yaxis.set_major_formatter("${x:1.2f}")
    ax.set_facecolor("#f5f0ed")
    ax.grid(color="#ffffff")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#c2ae97")
    ax.spines["bottom"].set_color("#c2ae97")

    plt.xticks(rotation=45)
    fig.subplots_adjust(bottom=0.2)
    plt.show()

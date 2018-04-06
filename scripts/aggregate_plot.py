import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from matplotlib.ticker import FuncFormatter, MaxNLocator
from math import *


class AntennaePlot:
    def __init__(self, ax, start, color, means, stds, time=False):
        self.data = list(zip(means, stds))
        self.d = 0.2
        self.ax = ax
        self.start = start
        self.color = color
        self.time = time

    def plot(self):
        x = self.start - 1
        dx=4
        for mean, std in self.data:
            x += dx
            self._antennae(x, mean, std)
        m = max(self.data, key=lambda x: x[0] + x[1])
        x_major_ticks = np.arange(-0.5, x + 1.5*dx, dx)
        y_high_lim = 1.2*round((m[0] + m[1]))
        y_major_ticks = np.linspace(0, y_high_lim, 7)
        y_minor_ticks = np.linspace(0, y_high_lim, 13)
        if self.time:
            y_high_lim = 15000
            y_major_ticks = np.linspace(0, y_high_lim, 7)
            y_minor_ticks = np.linspace(0, y_high_lim, 13)

        self.ax.set_ylim(bottom=0, top=y_high_lim)
        self.ax.set_xlim([1, 6])
        self.ax.set_xticks(x_major_ticks)
        # plt.minorticks_on()
        # ax.tick_params(axis='y', which='minor', bottom='off')
        self.ax.set_yticks(y_major_ticks)
        self.ax.set_yticks(y_minor_ticks, minor=True)
        self.ax.grid(alpha=0.25)

        def format_fn(tick_val, tick_pos):
            if tick_pos == 1:
                return "1-1000"
            if tick_pos == 2:
                return "1-100"
            if tick_pos == 3:
                return "1-200"
            if tick_pos == 4:
                return "5-100"
            if tick_pos == 5:
                return "5-200"
            return ""

        self.ax.xaxis.set_major_formatter(FuncFormatter(format_fn))

    def _antennae(self, x, mean, std):
        self.ax.bar(x, mean, alpha=0.5, color=self.color)
        self.ax.errorbar(x, mean, std, lw=2, capsize=5, capthick=2, color=self.color)
        return
        std = 0
        steam = mlines.Line2D([x, x], [0, mean], color=self.color, aa=True)
        left_antennae_x = [x, x - 0.5 * self.d]
        right_antennae_x = [x, x + 0.5 * self.d]
        antennae_y = [mean, mean + std]
        left_antennae = mlines.Line2D(left_antennae_x, antennae_y, color=self.color, aa=True)
        right_antennae = mlines.Line2D(right_antennae_x, antennae_y, color=self.color, aa=True)
        self.ax.add_line(steam)
        self.ax.add_line(left_antennae)
        self.ax.add_line(right_antennae)


if __name__ == "__main__":
    # table 3
    sw_based_strategy1_c7_means = (1.000, 0.894, 0.897, 0.920, 0.903)
    sw_based_strategy1_c12_means = (0.977, 0.749, 0.781, 0.755, 0.838)
    sw_based_strategy1_c19_means = (0.821, 0.605, 0.602, 0.608, 0.626)

    sw_based_strategy1_c7_stds = (0.000, 0.079, 0.075, 0.074, 0.092)
    sw_based_strategy1_c12_stds = (0.044, 0.165, 0.151, 0.133, 0.134)
    sw_based_strategy1_c19_stds = (0.050, 0.113, 0.141, 0.112, 0.128)

    # table 4
    sw_based_strategy2_c7_means = (1.000, 0.986, 0.974, 0.949, 0.949)
    sw_based_strategy2_c12_means = (0.977, 0.774, 0.820, 0.803, 0.803)
    sw_based_strategy2_c19_means = (0.821, 0.622, 0.587, 0.600, 0.596)

    sw_based_strategy2_c7_stds = (0.000, 0.042, 0.052, 0.062, 0.062)
    sw_based_strategy2_c12_stds = (0.044, 0.218, 0.183, 0.173, 0.186)
    sw_based_strategy2_c19_stds = (0.050, 0.079, 0.115, 0.088, 0.127)

    # table 5
    ari_based_strategy1_c7_means = (1.000, 0.894, 0.897, 0.920, 0.903)
    ari_based_strategy1_c12_means = (0.978, 0.749, 0.781, 0.790, 0.850)
    ari_based_strategy1_c19_means = (0.829, 0.625, 0.609, 0.580, 0.611)

    ari_based_strategy1_c7_stds = (0.000, 0.079, 0.075, 0.074, 0.092)
    ari_based_strategy1_c12_stds = (0.039, 0.165, 0.151, 0.152, 0.120)
    ari_based_strategy1_c19_stds = (0.046, 0.124, 0.128, 0.087, 0.117)

    # table 6
    ari_based_strategy2_c7_means = (1.000, 0.986, 0.974, 0.949, 0.949)
    ari_based_strategy2_c12_means = (0.978, 0.792, 0.820, 0.807, 0.788)
    ari_based_strategy2_c19_means = (0.829, 0.636, 0.631, 0.591, 0.612)

    ari_based_strategy2_c7_stds = (0.000, 0.042, 0.052, 0.062, 0.062)
    ari_based_strategy2_c12_stds = (0.039, 0.221, 0.183, 0.192, 0.188)
    ari_based_strategy2_c19_stds = (0.046, 0.088, 0.108, 0.090, 0.100)

    time_c7_means = (5651, 805, 1270, 4093, 6256)
    time_c12_means = (9021, 1215, 1855, 6104, 9328)
    time_c19_means = (11413, 1702, 2686, 8200, 13376)

    time_c7_stds = (1158, 109, 186, 371, 799)
    time_c12_stds = (692, 53, 147, 504, 581)
    time_c19_stds = (1261, 173, 231, 399, 806)

    dct = {"sw_based": {
        "c7": {"strategy1": {"means": sw_based_strategy1_c7_means, "stds": sw_based_strategy1_c7_stds},
               "strategy2": {"means": sw_based_strategy2_c7_means, "stds": sw_based_strategy2_c7_stds}},
        "c12": {"strategy1": {"means": sw_based_strategy1_c12_means, "stds": sw_based_strategy1_c12_stds},
                "strategy2": {"means": sw_based_strategy2_c12_means, "stds": sw_based_strategy2_c12_stds}},
        "c19": {"strategy1": {"means": sw_based_strategy1_c19_means, "stds": sw_based_strategy1_c19_stds},
                "strategy2": {"means": sw_based_strategy2_c19_means, "stds": sw_based_strategy2_c19_stds}}
    },
        "ari_based": {
            "c7": {"strategy1": {"means": ari_based_strategy1_c7_means, "stds": ari_based_strategy1_c7_stds},
                   "strategy2": {"means": ari_based_strategy2_c7_means, "stds": ari_based_strategy2_c7_stds}},
            "c12": {"strategy1": {"means": ari_based_strategy1_c12_means, "stds": ari_based_strategy1_c12_stds},
                    "strategy2": {"means": ari_based_strategy2_c12_means, "stds": ari_based_strategy2_c12_stds}},
            "c19": {"strategy1": {"means": ari_based_strategy1_c19_means, "stds": ari_based_strategy1_c19_stds},
                    "strategy2": {"means": ari_based_strategy2_c19_means, "stds": ari_based_strategy2_c19_stds}}

        },
        "time": {
            "c7": {"means": time_c7_means, "stds": time_c7_stds},
            "c12": {"means": time_c12_means, "stds": time_c12_stds},
            "c19": {"means": time_c19_means, "stds": time_c19_stds}
        }
    }

    fig, big_axes = plt.subplots(figsize=(15.0, 15.0), nrows=3, ncols=1, sharey=True)

    names = iter(["SW", "ARI", "TIME"])
    for row, big_ax in enumerate(big_axes, start=1):
        big_ax.set_title("%s \n" % next(names), fontsize=16)
        big_ax.tick_params(labelcolor=(1., 1., 1., 0.0), top='off', bottom='off', left='off', right='off')
        big_ax._frameon = False

    # SW plot
    sw_based = dct["sw_based"]
    i = 1
    for clusters in ["c7", "c12", "c19"]:
        ax = fig.add_subplot(3, 3, i)
        ax.set_title(clusters)
        print(i)
        AntennaePlot(ax, 0.05, "r", sw_based[clusters]["strategy1"]["means"],
                     sw_based[clusters]["strategy1"]["stds"]).plot()
        AntennaePlot(ax, 0.95, "b", sw_based[clusters]["strategy2"]["means"],
                     sw_based[clusters]["strategy2"]["stds"]).plot()
        i += 1
    # ARI plot
    ari_based = dct["ari_based"]
    for clusters in ["c7", "c12", "c19"]:
        ax = fig.add_subplot(3, 3, i)
        ax.set_title(clusters)
        print(i)
        AntennaePlot(ax, 0.05, "r", ari_based[clusters]["strategy1"]["means"],
                     ari_based[clusters]["strategy1"]["stds"]).plot()
        AntennaePlot(ax, 0.95, "b", ari_based[clusters]["strategy2"]["means"],
                     ari_based[clusters]["strategy2"]["stds"]).plot()
        i += 1

    time = dct["time"]
    for clusters in ["c7", "c12", "c19"]:
        ax = fig.add_subplot(3, 3, i)
        ax.set_title(clusters)
        print(i)
        AntennaePlot(ax, 0.5, "r", time[clusters]["means"],
                     time[clusters]["stds"], True).plot()
        i += 1

    plt.tight_layout()
    plt.savefig("bars.png", dpi=300)
    # plt.show()

    # exit(1)
    # plt.subplots_adjust(left=0.03, right=0.99, top=0.88, bottom=0.1, wspace=0.07)
    # plt.show()

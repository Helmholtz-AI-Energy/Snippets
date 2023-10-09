from matplotlib import pyplot as plt
import torch

from torch import Tensor
from typing import Optional

try:
    from HAIcolours import gray, blue
except ModuleNotFoundError:
    blue = 'tab:blue'
    gray = 'tab:gray'

plt.rcParams['figure.dpi'] = 600


def plot_calibration(predicted: Tensor, target: Tensor, dpi: Optional[int] = 600) -> (plt.Figure, plt.Axes):
    """
    Makes a calibration plot (also Q-Q plot)

    :param Tensor predicted: Tensor containing empirical percentages of predicted quantiles
    :param Tensor target: Tensor containing theoretical target percentages of predicted quantiles
    :param Optional[int] dpi: Resolution of plot in dpi

    :return plt.Figure, plt.Axes:
    """
    plt.rc('font', size=4)
    fig, ax = plt.subplots(dpi=dpi)
    ax.plot([0, 1], [0, 1], 'k', linewidth=1, transform=ax.transAxes)

    ax.plot(target, predicted, blue)

    ticks = torch.arange(0, 1.1, 0.2)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    ax.set_aspect('equal')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.grid(True)
    ax.set_ylabel('Theoretical quantiles')
    ax.set_xlabel('Predicted quantiles')

    plt.show()
    return fig, ax

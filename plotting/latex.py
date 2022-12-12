# To make matplotlib use latex formatting add this to the rc
from matplotlib import rc
new_rc = {
    "figure.figsize": figSize,
    "figure.autolayout": True,
    "text.usetex": True,
    "axes.labelsize": 10,
    "font.size": 8,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8 
}
rc(**new_rc)



from math import floor, log10, inf

def round_to_significant(x: float, significant_figures: int = 3) -> float:
    """
    Round floats to a given number of non-zero digits

    :param float x: number to be rounded
    :param int significant_figures: number of non-zero digits

    :returns float:
    """
    try:
        digits = significant_figures - int(floor(log10(abs(x)))) - 1
        return round(x, digits)
    except OverflowError:
        return inf
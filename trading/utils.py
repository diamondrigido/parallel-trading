import math


def get_quantity(balance, start_price, symbol_info):
    qnt = (float(balance) - 0.1) / float(start_price)
    step_size = 0.0
    for f in symbol_info["filters"]:
        if f["filterType"] == "LOT_SIZE":
            step_size = float("stepSize")

    precision = int(round(-math.log(step_size, 10), 0))
    qnt = float(round(qnt, precision))

    return qnt

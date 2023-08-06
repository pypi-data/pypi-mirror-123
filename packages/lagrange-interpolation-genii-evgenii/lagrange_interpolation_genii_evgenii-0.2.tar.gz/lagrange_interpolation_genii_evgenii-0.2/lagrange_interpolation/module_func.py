def fun(x_values, y_values):
    def func(value):
        res = 0
        for ind in range(0, len(y_values)):
            cur = 1
            for index in range(0, len(x_values)):
                if index != ind:
                    cur *= (value - x_values[index]) / (x_values[ind] - x_values[index])
            cur *= y_values[ind]
            res += cur
        return res

    return func

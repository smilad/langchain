def neuron(x, w, b):
    miani =  w * x + b
    final = max(miani, 0)
    return final, miani
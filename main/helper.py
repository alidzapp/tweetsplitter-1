def slice(string, slice):
    return [(string[i:i+slice].strip()) for i in range(0, len(string), slice)]
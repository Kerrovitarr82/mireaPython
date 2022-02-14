def script(check, x, y):
    if check("level") == 1:
        if check("gold", x, y):
            return "take"
        if check("gold", x, y + 1):
            return "down"
        return "right"

    if check("level") == 2:
        if check("gold", x, y):
            return "take"
        if check("gold", x + 1, y) or check("gold", x + 2, y):
            return "right"
        if check("gold", x - 1, y):
            return "left"
        if check("gold", x, y + 1):
            return "down"
        if check("gold", x, y - 1):
            return "up"
        if not check("wall", x, y - 1):
            return "up"
        return "right"

    if check("level") == 3:
        if check("gold", x, y):
            return "take"
        if check("wall", x - 1, y):
            if check("wall", x, y - 1) and check("wall", x - 1, y):
                return "right"
            return "up"
        if check("wall", x + 1, y):
            if check("wall", x + 1, y) and check("wall", x, y + 1):
                return "left"
            return "down"
        if check("wall", x, y - 1):
            return "right"
        if check("wall", x, y + 1):
            return "left"
        if check("wall", x + 1, y - 1):
            return "right"
        if check("wall", x - 1, y + 1):
            return "left"
        if check("wall", x + 1, y + 1):
            return "down"
        return "up"

    if check("level") == 4:
        if check("gold", x, y):
            return "take"
        if check("gold", x + 4, y):
            if check("wall", x + 1, y):
                return "down"
            return "right"
        if check("wall", x - 1, y):
            if check("wall", x, y - 1) and check("wall", x - 1, y):
                return "right"
            return "up"
        if check("wall", x + 1, y):
            if check("wall", x + 1, y) and check("wall", x, y + 1):
                return "left"
            return "down"
        if check("wall", x, y - 1):
            return "right"
        if check("gold", x, y - 5):
            return "up"
        if check("wall", x, y + 1):
            return "left"
        if check("gold", x - 1, y + 6):
            return "down"
        if check("gold", x - 1, y + 5):
            return "down"
        if check("wall", x + 1, y - 1):
            return "right"
        if check("wall", x - 1, y + 1):
            return "left"
        if check("wall", x + 1, y + 1):
            return "down"
        return "up"
    return "pass"

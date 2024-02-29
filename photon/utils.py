def centerY(app, size: int=1):
    return int((app.screenY - size) / 2)

def centerX(app, size: int=1):
    return int((app.screenX - size) / 2)

def centerTextX(app, text: str):
    return int((app.screenX - len(text)) / 2)
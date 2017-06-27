class Entity():
    def __init__(self):
        pass

def get_object(row):
    info = Entity()
    for key, value in row.items():
        setattr(info, key, value)
    return info


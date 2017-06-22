import entity

def get_object(row):
    info = entity.Entity()
    for key, value in row.items():
        setattr(info, key, value)
    return info


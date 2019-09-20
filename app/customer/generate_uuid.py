import uuid

def generate_uuid():
    number=uuid.uuid1()
    string=str(number)
    return string

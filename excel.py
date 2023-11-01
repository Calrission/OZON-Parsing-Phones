import pandas as pd

from models import Device


def write(devices: list[Device], excel_file="devices.xlsx"):
    columns = list(map(lambda x: x, Device.__annotations__))
    data = {column: [device.__getattribute__(column) for device in devices] for column in columns}
    df = pd.DataFrame(data)
    df.to_excel(excel_file)

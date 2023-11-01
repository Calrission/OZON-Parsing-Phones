from excel import write
from parser import *

devices = []
refresh_page()
while check_correct_now_page():
    from parser import page
    print(f"На {page} странице")
    new_devices = get_devices_from_page()
    print(f"+ {len(new_devices)} новых телефонов")
    devices.extend(new_devices)
    write(devices)
    cloudframe_bypass()
    next_page()
print("Достигнута конечная страница")

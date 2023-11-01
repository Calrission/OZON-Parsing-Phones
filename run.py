from output import to_excel, to_db, clear_table
from parser import *

devices = []
refresh_page()
if config["clear_table"] and config["output_type"] == "db":
    clear_table()
while check_correct_now_page():
    from parser import page
    print(f"На {page} странице")
    new_devices = get_devices_from_page()
    print(f"+ {len(new_devices)} новых телефонов")
    devices.extend(new_devices)
    if config["output_type"] == "excel":
        to_excel(devices)
    else:
        to_db(devices)
    cloudframe_bypass()
    next_page()
print("Достигнута конечная страница")

import csv
import os
import shutil
import time
from datetime import datetime
from netmiko import ConnectHandler
from routers import ROUTERS

with open('routers.csv') as f:
    reader = csv.reader(f)
    next(reader)
    routers = list(reader)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_base = '../../output'

if os.path.exists(output_base):
    shutil.rmtree(output_base)

def connect(router):
    device = {
        'device_type': router[5],
        'host': router[0],
        'port': int(router[1]),
        'username': router[2],
        'password': router[3],
        'timeout': 60,
        'global_delay_factor': 2,
    }
    
    if router[4]:
        device['secret'] = router[4]
    
    conn = ConnectHandler(**device)
    
    if router[5] == 'arista_eos':
        conn.enable()
    
    return conn

versions_dir = os.path.join(output_base, 'versions')
os.makedirs(versions_dir, exist_ok=True)

with open(os.path.join(versions_dir, f"versions_{timestamp}.txt"), 'w') as f:
    f.write("host,sw_version\n")
    for r in routers:
        try:
            vendor = ROUTERS[r[5]]
            conn = connect(r)
            output = conn.send_command(vendor.get_version_command())
            version = vendor.parse_version(output)
            f.write(f"{r[0]},{version}\n")
            conn.disconnect()
        except Exception as e:
            print(f"Erro em {r[0]}: {e}")
            f.write(f"{r[0]},error\n")

for r in routers:
    hostname = r[0].split('.')[0].split('-')[-1]
    router_dir = os.path.join(output_base, hostname)
    os.makedirs(router_dir, exist_ok=True)

    try:
        vendor = ROUTERS[r[5]]
        conn = connect(r)
        
        with open(os.path.join(router_dir, f"neighbours_{hostname}_{timestamp}.txt"), 'w') as f:
            f.write("interface,neighbour_hostname,neighbour_interface\n")
            output = conn.send_command(vendor.get_lldp_command())
            f.writelines(vendor.parse_lldp(output, own_hostname=hostname))
        
        with open(os.path.join(router_dir, f"interfaces_{hostname}_{timestamp}.txt"), 'w') as f:
            f.write("interface,status,ip,mask\n")
            output = conn.send_command(vendor.get_interface_command())
            f.writelines(vendor.parse_interfaces(output))

        with open(os.path.join(router_dir, f"conf_{hostname}_{timestamp}.txt"), 'w') as f:
            f.write(conn.send_command(vendor.get_config_command()))
        
        conn.disconnect()
    except Exception as e:
        print(f"Erro em {hostname}: {e}")
#!/usr/bin/env python3
import yaml, json, socket, requests
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print("=== VALIDACION RESTCONF ===")
print(f"Script : validacion_restconf.py")
print(f"Fecha  : {datetime.now()}")
print(f"Host   : {socket.gethostname()}")
print("===========================")

with open("../vars/vars_005D-12.yaml") as f:
    v = yaml.safe_load(f)
r = v["router"]
c = v["cliente"]

BASE = f"https://{r['ip']}/restconf/data"
HEADERS = {"Accept": "application/yang-data+json"}
AUTH = (r["usuario"], r["password"])

def get_endpoint(url, filename):
    resp = requests.get(url, headers=HEADERS, auth=AUTH, verify=False)
    data = resp.json()
    with open(f"evidencias/responses/{filename}", "w") as f:
        json.dump(data, f, indent=2)
    return data

# Consultas
h   = get_endpoint(f"{BASE}/Cisco-IOS-XE-native:native/hostname", "get_hostname.json")
lo  = get_endpoint(f"{BASE}/ietf-interfaces:interfaces/interface=Loopback{r['loopback_id']}", "get_loopback.json")
gi  = get_endpoint(f"{BASE}/ietf-interfaces:interfaces/interface=GigabitEthernet1", "get_interfaces.json")
ntp = get_endpoint(f"{BASE}/Cisco-IOS-XE-native:native/ntp", "get_ntp.json")

# Extraer valores
hostname_obtenido = h.get("Cisco-IOS-XE-native:hostname", "")

# Loopback IP
try:
    lo_iface = lo.get("ietf-interfaces:interface", {})
    if isinstance(lo_iface, list):
        lo_iface = lo_iface[0]
    loopback_ip_obtenido = lo_iface.get("ietf-ip:ipv4", {}).get("address", [{}])[0].get("ip", "")
except:
    loopback_ip_obtenido = ""

# Descripcion WAN
try:
    gi_iface = gi.get("ietf-interfaces:interface", {})
    if isinstance(gi_iface, list):
        gi_iface = gi_iface[0]
    desc_wan_obtenido = gi_iface.get("description", "")
except:
    desc_wan_obtenido = ""

# NTP
try:
    ntp_data = ntp.get("Cisco-IOS-XE-native:ntp", {})
    ntp_obtenido = ntp_data.get("Cisco-IOS-XE-ntp:server", {}).get("server-list", [{}])[0].get("ip-address", "")
except:
    ntp_obtenido = ""

criterios = [
    ("Hostname",    hostname_obtenido,    c["hostname"]),
    ("Loopback IP", loopback_ip_obtenido, r["loopback_ip"]),
    ("Desc WAN",    desc_wan_obtenido,    r["descripcion_wan"]),
    ("NTP Server",  ntp_obtenido,         r["ntp_server"]),
]

ok_count = 0
for nombre, obtenido, esperado in criterios:
    status = "[OK]" if obtenido == esperado else "[FAIL]"
    if status == "[OK]": ok_count += 1
    print(f"{status} {nombre}: obtenido='{obtenido}' esperado='{esperado}'")

print(f"\nResultado: {'CONFORME' if ok_count == 4 else 'NO CONFORME'} ({ok_count}/4)")

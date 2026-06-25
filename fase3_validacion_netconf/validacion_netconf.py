#!/usr/bin/env python3
import yaml, socket
from datetime import datetime
from ncclient import manager
from lxml import etree

# Metadatos
print("=== VALIDACION NETCONF ===")
print(f"Script : validacion_netconf.py")
print(f"Fecha  : {datetime.now()}")
print(f"Host   : {socket.gethostname()}")
print("==========================")

# Cargar variables
with open("../vars/vars_005D-12.yaml") as f:
    v = yaml.safe_load(f)
r = v["router"]
c = v["cliente"]

# Filtro XML
filtro = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
    <interface>
      <Loopback/>
      <GigabitEthernet/>
    </interface>
    <ntp/>
  </native>
</filter>
"""

# Conectar y obtener config
with manager.connect(
    host=r["ip"], port=830,
    username=r["usuario"], password=r["password"],
    hostkey_verify=False, allow_agent=False, look_for_keys=False
) as m:
    reply = m.get_config(source="running", filter=filtro)
    xml_str = reply.xml

# Guardar XML crudo
with open("evidencias/rpc_reply_raw.xml", "w") as f:
    f.write(xml_str)

# Parsear XML
root = etree.fromstring(xml_str.encode())
ns = {"x": "http://cisco.com/ns/yang/Cisco-IOS-XE-native"}

# Extraer valores
hostname = root.findtext(".//x:hostname", namespaces=ns) or ""
loopback_ip = root.findtext(f".//x:Loopback[x:name='{r['loopback_id']}']/x:ip/x:address/x:primary/x:address", namespaces=ns) or ""
loopback_mask = root.findtext(f".//x:Loopback[x:name='{r['loopback_id']}']/x:ip/x:address/x:primary/x:mask", namespaces=ns) or ""
desc_wan = root.findtext(".//x:GigabitEthernet[x:name='1']/x:description", namespaces=ns) or ""

# Buscar NTP con múltiples paths posibles
ntp = ""
ntp_paths = [
    ".//x:ntp/x:server/x:server-list/x:ip-address",
    ".//x:ntp/x:server/x:vrf/x:server-list/x:ip-address",
    ".//x:ntp/x:peer/x:server-list/x:ip-address",
]
for path in ntp_paths:
    resultado = root.findtext(path, namespaces=ns)
    if resultado:
        ntp = resultado
        break

# Si aún no lo encontró, buscar en todo el XML
if not ntp:
    for elem in root.iter():
        if elem.tag and "ip-address" in elem.tag and elem.text == r["ntp_server"]:
            ntp = elem.text
            break

# Comparar
criterios = [
    ("Hostname",      hostname,     c["hostname"]),
    ("Loopback IP",   loopback_ip,  r["loopback_ip"]),
    ("Loopback Mask", loopback_mask, r["loopback_mask"]),
    ("Desc WAN",      desc_wan,     r["descripcion_wan"]),
    ("NTP Server",    ntp,          r["ntp_server"]),
]

ok_count = 0
for nombre, obtenido, esperado in criterios:
    status = "[OK]" if obtenido == esperado else "[FAIL]"
    if status == "[OK]": ok_count += 1
    print(f"{status} {nombre}: obtenido='{obtenido}' esperado='{esperado}'")

print(f"\nResultado: {'CONFORME' if ok_count == 5 else 'NO CONFORME'} ({ok_count}/5)")

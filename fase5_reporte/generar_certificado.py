#!/usr/bin/env python3
import yaml, os
from datetime import datetime

with open("../vars/vars_005D-12.yaml") as f:
    v = yaml.safe_load(f)

def check_conforme(filepath):
    try:
        with open(filepath) as f:
            contenido = f.read()
            return "CONFORME" in contenido and contenido.count("NO CONFORME") == 0
    except:
        return False

netconf_ok  = check_conforme("../fase3_validacion_netconf/evidencias/output_validacion_netconf.txt")
restconf_ok = check_conforme("../fase4_validacion_restconf/evidencias/output_validacion_restconf.txt")
diff_ok     = os.path.exists("evidencias/snapshot_final_005D-12") and len(os.listdir("evidencias/snapshot_final_005D-12")) > 0

resultado = "CONFORME" if (netconf_ok and restconf_ok and diff_ok) else "NO CONFORME"

cert = f"""
==========================================
  CERTIFICADO DE COMPLIANCE - EP3
==========================================
Alumno  : {v['nombre']}
Codigo  : {v['codigo']}
Cliente : {v['cliente']['empresa']}
Hostname: {v['cliente']['hostname']}
Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
------------------------------------------
NETCONF  : {'CONFORME' if netconf_ok else 'NO CONFORME'}
RESTCONF : {'CONFORME' if restconf_ok else 'NO CONFORME'}
DIFF     : {'DETECTADO' if diff_ok else 'SIN CAMBIOS'}
------------------------------------------
RESULTADO FINAL: {resultado}
==========================================
"""
print(cert)
with open("evidencias/certificado_compliance_005D-12.txt", "w") as f:
    f.write(cert)

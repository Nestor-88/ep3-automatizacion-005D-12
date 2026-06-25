# EP3 - Implementación de Automatización de Red con Compliance Auditado

## 1. Objetivo del proyecto
Se implementó la automatización completa de un router Cisco CSR1000v para la empresa Telecom Andinas SpA. El objetivo fue incorporar el equipo a la red corporativa aplicando configuración estándar de forma automatizada y verificable.

## 2. Alcance
Se configuró hostname, banner, NTP, descripción WAN e interfaz Loopback de gestión. Se habilitaron NETCONF y RESTCONF para automatización. No se configuraron protocolos de enrutamiento dinámico ni políticas de seguridad avanzadas. Se usaron pyATS, Ansible, ncclient y requests.

## 3. Infraestructura utilizada
- Router: Cisco CSR1000v (IOS-XE) — IP 192.168.56.101
- Estación de trabajo: DEVASC VM (Ubuntu, labvm)
- Herramientas: Python 3, Ansible, pyATS/Genie, ncclient, requests

## 4. Tecnologías empleadas y justificación
- **pyATS/Genie**: usado en Fase 1 y 5 para capturar y comparar el estado del dispositivo de forma estructurada.
- **Ansible**: usado en Fase 2 para aplicar configuración corporativa de forma idempotente y reproducible.
- **NETCONF**: usado en Fase 3 para validar configuración via protocolo estándar YANG sobre SSH.
- **RESTCONF**: usado en Fase 4 para validar configuración via HTTP/JSON, más simple e integrable con APIs web.

## 5. Configuración aplicada
| Parámetro | Valor |
|---|---|
| Hostname | RTR-TELEAND |
| IP Loopback10 | 10.5.12.1 / 255.255.255.0 |
| Descripción GigabitEthernet1 | Enlace-WAN-Copiapo |
| Banner | ACCESO RESTRINGIDO - TELEAND |
| Servidor NTP | 1.1.1.1 |

## 6. Resultados de validación
| Criterio | NETCONF | RESTCONF |
|---|---|---|
| Hostname RTR-TELEAND | CONFORME | CONFORME |
| Loopback IP 10.5.12.1 | CONFORME | CONFORME |
| Loopback Mask 255.255.255.0 | CONFORME | — |
| Descripción WAN | CONFORME | CONFORME |
| Servidor NTP 1.1.1.1 | CONFORME | CONFORME |

## 7. Conclusiones
El router RTR-TELEAND fue configurado exitosamente y validado mediante NETCONF y RESTCONF con resultado CONFORME en todos los criterios. El equipo queda entregado a operaciones listo para producción. El proceso quedó completamente auditado en este repositorio GitHub.

# Network Architecture & Segmentation, OPNsense & Remote Access Runbook

## 1. Network Topology & Segmentation Overview
To isolate production and untrusted traffic from internal infrastructure services, the homelab utilizes strict network segmentation routed via an OPNsense virtual firewall instance.

* **Edge / WAN Subnet (`192.168.0.0/24`):** 
  * Connects physical Proxmox nodes, the Synology NAS, and edge management interfaces to the primary ISP gateway (`192.168.0.1`).
* **Isolated Lab LAN (`10.0.10.0/24`):**
  * Firewalled internal guest network behind OPNsense (`10.0.10.1`).
  * Hosts core infrastructure (Samba4 AD, Zammad ITSM) and client endpoints (`Client01`–`03`).

---

## 2. OPNsense Firewall Configuration
* **Role:** Acts as the primary router and perimeter firewall between the edge network and the isolated lab.
* **Interfaces:**
  * `WAN`: vtnet0 assigned `192.168.0.202` (Bridged to the physical 192.168.0.0/24 edge network using 192.168.0.1 as its upstream gateway).
  * `LAN`: vtnet1 assigned `10.0.10.1` (Attached to an isolated internal Proxmox Linux Bridge (vmbr1), acting as the gateway for all internal lab VMs and containers).
  * NAT Configuration: Automatic Outbound NAT so 10.0.10.x clients can reach the internet for Windows Updates and package installs without exposing them inbound.

* **Key Firewall Rules:**
  * Inter-VLAN routing rules restrict direct inbound traffic from the external `192.168.0.x` network (except for Admin devices) into the sensitive `10.0.10.x` services, allowing only explicitly approved administrative ports (e.g., RDP / Guacamole).
| Type / Interface | Action | Protocol | Source                | Destination   | Port         | Description                           |
|------------------|--------|----------|-----------------------|---------------|--------------|---------------------------------------|
| Floating         | Pass   | TCP      | 192.168.0.209         | 10.0.10.3     | ldap         | Allow Zammad LDAP to access Samba     |
| Interface (LAN)  | Pass   | TCP/UDP  | 192.168.0.243         | 10.0.10.3     | Any          | AD web interface access               |
| Interface (WAN)  | Pass   | TCP      | Admin_devices (Alias) | 192.168.0.202 | http / https | WAN access to OPNsense WebGUI         |
| Interface (LAN)  | Pass   | TCP      | 192.168.0.146         | 10.0.10.100   | 3389         | Allow Guacamole access to Windows VMs |
| Interface (WAN)  | Pass   | TCP      | 192.168.0.243         | This Firewall | http / https | OPNsense access from main rig         |

---

## 3. Remote Access & Management (Tailscale / Guacamole)
* **Tailscale VPN Integration:** 
  * Integrated directly at the firewall level by running the Tailscale client as a service/plugin on OPNsense, making the firewall an active node in the secure tailnet.
  * Provides zero-trust secure overlay networking into the environment for remote administrative tasks and remote client user access without exposing insecure ports or requiring public port-forwarding.
* **Apache Guacamole (Staging):**
  * Deployed on the internal lab network (`10.0.10.4`) as a clientless HTML5 bastion host.
  * *Status Note:* Currently operating in a staging phase; active fallback relies on native Windows Remote Desktop Protocol (RDP) over secured subnets due to ongoing NLA handshake tuning with Windows 11 domain clients.

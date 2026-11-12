# Identity & Directory Services: Samba4 Active Directory Runbook

## 1. Directory Services Overview
To simulate a realistic corporate IT infrastructure, the homelab utilizes **Samba4** acting as an Active Directory Domain Controller (DC). This provides centralized identity management, Kerberos authentication, LDAP querying, and Group Policy-ready object management for internal lab endpoints and services.

* **Domain Name:** `homelab.internal`
* **Realm:** `HOMELAB.INTERNAL`
* **DC Hostname & IP:** `Samba4-AD` (`10.0.10.3`)

---

## 2. Infrastructure & Network Integration
* **Subnet Placement:** Hosted securely on the isolated lab subnet (`10.0.10.0/24`), shielded from direct internet access and edge networks via OPNsense.
* **Firewall & Port Requirements:** 
  * Strict OPNsense LAN rules permit internal lab clients (`10.0.10.x`) to access the Domain Controller over core Active Directory ports:
    * **DNS (`53 TCP/UDP`):** Name resolution and service discovery.
    * **Kerberos (`88 TCP/UDP`):** Ticket-granting authentication.
    * **LDAP / LDAPS (`389/636 TCP/UDP`):** Directory queries and application integrations (e.g., Zammad ITSM authentication).
    * **SMB / RPC (`445 TCP`, `135-139`):** File sharing and domain replication protocols.

---

## 3. DNS Strategy & Forwarding
* **Primary DNS Role:** The Samba4 DC serves as the primary internal DNS server for all domain-joined endpoints (`Client01`–`03`).
* **Upstream Forwarding / Integration:** 
  * Configured to forward non-domain recursive DNS queries to OPNsense’s **Unbound DNS** service, ensuring seamless internet resolution while keeping internal host records strictly contained within the domain zone.

---

## 4. Service Integrations (LDAP / ITSM)
* **Zammad ITSM Integration:** 
  * Integrated via a secure LDAP floating/interface firewall rule allowing the Zammad application server (`10.0.10.5`) to query the Samba4 DC (`10.0.10.3:389`), enabling centralized user authentication and directory sync.

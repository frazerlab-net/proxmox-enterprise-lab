# IT Service Management (ITSM): Zammad Deployment & Automation Runbook

## 1. ITSM Overview & Architecture
To simulate enterprise-grade IT support workflows, **Zammad** is deployed as the core IT Service Management (ITSM) platform within the isolated lab environment. It provides ticket tracking, agent management, and end-user request handling.

* **Platform:** Zammad ITSM
* **Host IP / Subnet:** `10.0.10.5` (Isolated lab network `10.0.10.0/24`)
* **Role:** Centralized ticketing system for handling simulated user requests, system alerts, and internal lab administration tasks.

---

## 2. Directory Services Integration (Authentication)
* **Active Directory Sync:** Integrated directly with the Samba4 Domain Controller (`10.0.10.3`) via LDAP.
* **Firewall & Routing:** A dedicated floating/interface rule permits secure LDAP queries (`TCP 389`) from the Zammad application server to the Samba4 DC, enabling centralized credential validation and user synchronization.

---

## 3. Automation & Proactive Ticketing
* **Custom Python Automation (End-to-End Simulation):** 
 * Features a custom Python-based automation script (located in the `automation/zammad-ticket-gen/` repository folder) that programmatically generates simulated support tickets via Zammad’s REST API.
  * **Endpoint Issue Injection:** Beyond generating the ITSM ticket, the script simultaneously configures or injects the corresponding issue directly into the target Windows VM (`Client01`–`03`), establishing a live, actionable troubleshooting scenario.
  * Validates queue routing, notifications, and incident remediation workflows without manual intervention.

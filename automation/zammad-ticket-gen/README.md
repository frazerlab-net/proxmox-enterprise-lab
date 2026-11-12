# Zammad Automated Ticket & Incident Generator

## Overview
This Python-based automation script is hosted and executed directly from within the **Zammad Proxmox container/VM console** (`10.0.10.5`) on the isolated lab network.
It programmatically generates simulated support tickets while simultaneously injecting corresponding faults into target Windows VMs (`Client01`–`03`), creating a fully automated, end-to-end incident simulation workflow.

---

## Architecture & Workflow
1. **ITSM Ticket Generation:** Communicates locally/internally with Zammad's REST API to instantiate realistic support tickets with predefined priorities, subjects, and customer mappings.
2.**Remote Endpoint Fault Injection (SSH):** Once a ticket is generated, the script uses **SSH** to securely connect to the target Windows VM (`Client01`–`03`) on the isolated lab network, executing remote commands or scripts to inject the corresponding system issue.
3. **Queue Throttling (Safety Guardrail):** 
   * *Design Note:* To accommodate limited hands-on lab time and prevent queue overload during automated runs, the script includes a built-in threshold check that limits active ticket generation based on current queue depth, but this can be disabled/removed.

---
## Configuration & Setup

1. **Prerequisites:** 
   * Python 3.x installed within the Zammad environment.
   * Required libraries: `requests` and `paramiko` (`pip install requests paramiko`)
2. **Script Parameters:**
   * Open `zammad_ticket_gen.py` and replace the sanitized placeholder strings with your local lab values before running:
     * `Zammad_Base_URL` & `API_Token`: Target Zammad API endpoint and administrative API token.
     * `VMS` Dictionary: Target Windows VM IP addresses (`VM_IP`), Zammad user emails (`ZAMMAD_USER_EMAIL`), and local Windows SSH credentials (`ADMIN_USERNAME` / `ADMIN_PASSWORD`).

## Execution & Automation (Planned)

* **Current Status:** Executed manually on-demand from the Zammad Proxmox console during lab sessions:
  ```bash
  zammad_ticket_gen.py
  ```
### Planned Automation Roadmap:
** Intention: To be integrated into a periodic cron schedule once script reconfigurations are finalized, allowing the lab to continuously generate automated tickets and test incident injection routines without manual oversight

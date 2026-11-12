import random
import requests
import paramiko

# Zammad Configurations
Zammad_Base_URL = "ZAMMAD_URL_OR_IP"
API_Token = "YOUR_API_KEY"
Group_Name = "Users"

# Windows VM & User Assignment Mappings
VMS = [
    {
        "name": "USER1_NAME",
        "ip": "VM_IP",
        "user": "ZAMMAD_USER_EMAIL",
        "ssh_user": "ADMIN_USERNAME",
        "ssh_pass": "ADMIN_PASSWORD"
    },
    {
        "name": "USER2_NAME",
        "ip": "VM_IP",
        "user": "ZAMMAD_USER_EMAIL",
        "ssh_user": "ADMIN_USERNAME",
        "ssh_pass": "ADMIN_PASSWORD"
    },
    {
        "name": "USER3_NAME",
        "ip": "VM_IP",
        "user": "ZAMMAD_USER_EMAIL",
        "ssh_user": "ADMIN_USERNAME",
        "ssh_pass": "ADMIN_PASSWORD!"
    }
]

# Scenario Pool (Remote PowerShell Command + Matching Zammad Ticket Payload)
LAB_SCENARIOS = [
    {
        "id": "UNMAP_DRIVE",
        "command": 'powershell.exe -Command "Remove-PSDrive -Name Z -Force -ErrorAction SilentlyContinue; net use Z: /delete /y"',
        "title": "Cannot access mapped drive Z:",
        "body": "Hi helpdesk, my mapped network drive Z: disappeared when I logged into my desktop today."
    },

    {
        "id": "NETWORK_DOWN",
        "command": 'powershell.exe -Command "ipconfig /release; ipconfig /flushdns"',
        "title": "No internet connection and IP address error",
        "body": "I am getting a network error and cannot reach any websites or internal shares."
    },
    {
        "id": "DOMAIN_TRUST_BROKEN",
        "command": 'powershell.exe -Command "Stop-Service -Name Netlogon -Force"',
        "title": "The trust relationship between this workstation and the primary domain failed",
        "body": "When attempting to log in with my credentials, I get an error about a failed trust relationship?"
    },
    {
        "id": "INVALID_PROXY",
        "command": 'powershell.exe -Command "netsh winhttp set proxy 192.168.1.99:8080"',
        "title": "Web pages won't load in browser (Proxy error)",
        "body": "Hi helpdesk, none of my web browsers will load any external websites. I keep getting a proxy connection error."
    },
    {
        "id": "AUDIO_DOWN",
        "command": 'powershell.exe -Command "Stop-Service -Name Audiosrv -Force"',
        "title": "Audio and microphone not working for calls",
        "body": "I have a meeting starting soon, but my speakers and microphone are grayed out and not producing any sound."
    }
]

# FUNCTIONS
def inject_vm_issue(vm_info, command):
    """Executes the PowerShell command on the target Windows VM over SSH."""
    print(f"[*] Connecting to target VM ({vm_info['ip']}) via SSH...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=vm_info["ip"],
            username=vm_info["ssh_user"],
            password=vm_info["ssh_pass"],
            timeout=10
        )
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()
        ssh.close()
        print(f"[+] Successfully injected chaos command on {vm_info['ip']}.")
        return True
    except Exception as e:
        print(f"[-] SSH Execution failed on {vm_info['ip']}: {e}")
        return False

def create_zammad_ticket(scenario, vm_info):
    """Creates the corresponding ticket in Zammad."""
    url = f"{Zammad_Base_URL}/api/v1/tickets"
    headers = {
        "Authorization": f"Token token={API_Token}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": scenario["title"],
        "group": Group_Name,
        "customer": vm_info["user"],
        "article": {
            "subject": scenario["title"],
            "body": f"{scenario['body']}\n\n[Lab Metadata: Target IP={vm_info['ip']} | Scenario ID={scenario['id']}]",
            "type": "note",
            "sender": "Customer",
            "internal": False
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        print(f"[SUCCESS] Ticket created successfully for {vm_info['user']}!")
    else:
        print(f"[-] Zammad API Error ({response.status_code}): {response.text}")

# LIMIT CHECK FUNCTION
def get_open_ticket_count():
    """Checks Zammad for how many open/unclosed tickets currently exist."""
    url = f"{Zammad_Base_URL}/api/v1/tickets/search?query=state.name:open OR state.name:new"
    headers = {
    "Authorization": f"Token token={API_Token}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tickets = response.json()
            return len(tickets)
        else:
            print(f"[-] Warning: Could not fetch ticket count ({response.status_code}). Proceeding with caution.")
            return 0
    except Exception as e:
        print(f"[-] Error checking ticket count: {e}")
        return 0

# MAIN EXECUTION (DYNAMIC PAIRING WITH TICKET CAP)
if __name__ == "__main__":
        MAX_ALLOWED_OPEN_TICKETS = 4  # Set your maximum limit here

        current_open_tickets = get_open_ticket_count()
        print(f"[*] Current open tickets in queue: {current_open_tickets}/{MAX_ALLOWED_OPEN_TICKETS}")

        if current_open_tickets >= MAX_ALLOWED_OPEN_TICKETS:
            print("[*] Ticket limit reached. Skipping ticket generation and VM chaos until queue clears out.")
            exit(0)

        # 1. Pick a random VM target AND a random issue template independently
        target_vm = random.choice(VMS)
        issue = random.choice(LAB_SCENARIOS)

        print(f"[*] Randomized Selection:")
        print(f"    - Target User: {target_vm['user']} ({target_vm['ip']})")
        print(f"    - Scenario:    {issue['id']}")
        # 2. Inject issue and conditionally create Zammad ticket based on SSH success
        if inject_vm_issue(target_vm, issue["command"]):
           create_zammad_ticket(issue, target_vm)
           print("[SUCCESS] Ticket created because SSH succeeded.")
        else:
           print("[X] Skipped Zammad ticket creation due to SSH FAILURE.")
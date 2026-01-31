# Simulated VM State
VM_STATE = {
    "status": "STOPPED"
}

def start_vm():
    VM_STATE["status"] = "RUNNING"

def stop_vm():
    VM_STATE["status"] = "STOPPED"

def restart_vm():
    VM_STATE["status"] = "RESTARTING"
    VM_STATE["status"] = "RUNNING"

def get_vm_status():
    return VM_STATE["status"]

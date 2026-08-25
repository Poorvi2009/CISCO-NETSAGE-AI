import csv
import sys

def check_ip_mask_mismatch(topology, show_out):
    """Detects subnet mask mismatch issues."""
    if "mask" in show_out.lower() or "subnet" in topology.lower():
        if "255.255.255.0" in show_out and "/28" in topology:
            return "Rule Violation: Subnet Mask Mismatch detected between interfaces."
    return None

def check_admin_down(show_out):
    """Detects administratively down interfaces."""
    if "administratively down" in show_out.lower():
        return "Rule Violation: Interface is administratively down (requires 'no shutdown')."
    return None

def check_vlan_missing(show_out):
    """Detects uncreated or missing VLANs."""
    if "vlan not found" in show_out.lower() or "vlan does not exist" in show_out.lower():
        return "Rule Violation: VLAN is not active or missing in switch database."
    return None

def check_dhcp_exhaustion(show_out):
    """Detects DHCP scope pool exhaustion."""
    if "zero available" in show_out.lower() or "leased 10; zero available" in show_out.lower():
        return "Rule Violation: DHCP scope pool completely exhausted."
    return None

def run_rule_checker(csv_file_path):
    print("=" * 60)
    print("NetSage AI - Deterministic Rule Checker Verification")
    print("=" * 60)
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            flagged_count = 0
            
            for row in reader:
                case_id = row.get('case_id', 'UNKNOWN')
                symptom = row.get('symptom', '')
                topo = row.get('topology_note', '')
                show = row.get('show_outputs', '')
                
                violations = []
                
                res1 = check_admin_down(show)
                if res1: 
                    violations.append(res1)
                
                res2 = check_vlan_missing(show)
                if res2: 
                    violations.append(res2)
                    
                res3 = check_dhcp_exhaustion(show)
                if res3: 
                    violations.append(res3)
                    
                res4 = check_ip_mask_mismatch(topo, show)
                if res4: 
                    violations.append(res4)
                
                if violations:
                    flagged_count += 1
                    print(f"[FLAGGED] {case_id}: {symptom}")
                    for v in violations:
                        print(f"  --> {v}")
                    print("-" * 60)
                    
        print(f"Rule Checker Run Complete: {flagged_count} cases flagged with deterministic errors.")
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file_path}'. Please make sure cases.csv is in the same folder.")

if __name__ == "__main__":
    csv_file = "cases.csv" if len(sys.argv) < 2 else sys.argv[1]
    run_rule_checker(csv_file)
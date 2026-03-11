class Arista:
    def get_version_command(self):
        return 'show version'
    
    def parse_version(self, output):
        for line in output.split('\n'):
            if 'Software image version:' in line:
                parts = line.split(':')[1].strip().split()
                return parts[0] if parts else "unknown"
        return "unknown"
    
    def get_lldp_command(self):
        return 'show lldp neighbors'
    
    def parse_lldp(self, output, own_hostname=None):
        lines = []
        in_table = False
        for line in output.split('\n'):
            if '----' in line:
                in_table = True
                continue
            if in_table and line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    neighbor = parts[1]
                    if neighbor != own_hostname:
                        lines.append(f"{parts[0]},{neighbor},{parts[2]}\n")
        return lines
    
    def get_interface_command(self):
        return 'show ip interface brief'
    
    def parse_interfaces(self, output):
        lines = []
        in_table = False
        for line in output.split('\n'):
            if '---------' in line:
                in_table = True
                continue
            if in_table and line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    ip_with_mask = parts[1]
                    if '/' in ip_with_mask:
                        ip, mask = ip_with_mask.split('/')
                    else:
                        ip = ip_with_mask if ip_with_mask != 'unassigned' else ''
                        mask = ''
                    lines.append(f"{parts[0]},{parts[2]},{ip},{mask}\n")
        return lines
    
    def get_config_command(self):
        return 'show running-config'
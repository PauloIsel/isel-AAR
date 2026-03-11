class MikroTik:
    def get_version_command(self):
        return '/system resource print'
    
    def parse_version(self, output):
        for line in output.split('\n'):
            if 'version:' in line.lower():
                return line.split(':')[1].strip()
        return "unknown"
    
    def get_lldp_command(self):
        return '/ip neighbor print'
    
    def parse_lldp(self, output, own_hostname=None):
        lines = []
        for line in output.split('\n'):
            line = line.strip()
            if line and line[0].isdigit():
                parts = line.split()
                interface = parts[1] if len(parts) > 1 else 'unknown'
                neighbor = 'unknown'
                for i in range(2, len(parts)):
                    if ':' in parts[i] and i+1 < len(parts):
                        neighbor = parts[i+1]
                        break
                if neighbor != 'unknown' and neighbor != own_hostname:
                    lines.append(f"{interface},{neighbor},unknown\n")
        return lines
    
    def get_interface_command(self):
        return '/ip address print'
    
    def parse_interfaces(self, output):
        lines = []
        in_table = False
        for line in output.split('\n'):
            line = line.strip()
            if 'ADDRESS' in line and 'NETWORK' in line:
                in_table = True
                continue
            if in_table and line and line[0].isdigit():
                parts = line.split()
                if len(parts) >= 3:
                    address_with_mask = parts[1]
                    interface = parts[3] if len(parts) > 3 else parts[2]
                    if '/' in address_with_mask:
                        ip, mask = address_with_mask.split('/')
                    else:
                        ip = address_with_mask
                        mask = ''
                    lines.append(f"{interface},up,{ip},{mask}\n")
        return lines
    
    def get_config_command(self):
        return '/export'
class Nokia:
    def get_version_command(self):
        return 'show version'
    
    def parse_version(self, output):
        for line in output.split('\n'):
            if 'Software Version' in line and ':' in line:
                return line.split(':')[1].strip()
        return "unknown"
    
    def get_lldp_command(self):
        return 'show system lldp neighbor'
    
    def parse_lldp(self, output, own_hostname=None):
        lines = []
        in_table = False
        for line in output.split('\n'):
            if '===' in line:
                in_table = True
                continue
            if in_table and '|' in line and not line.strip().startswith('+'):
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 7:
                    neighbor = parts[2]
                    if neighbor != own_hostname:
                        lines.append(f"{parts[0]},{neighbor},{parts[6]}\n")
        return lines
    
    def get_interface_command(self):
        return 'show interface brief'
    
    def parse_interfaces(self, output):
        lines = []
        in_table = False
        for line in output.split('\n'):
            if '===' in line:
                in_table = True
                continue
            if in_table and '|' in line and not line.strip().startswith('+'):
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 3:
                    lines.append(f"{parts[0]},{parts[2]},,\n")
        return lines
    
    def get_config_command(self):
        return 'info flat'
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
        return 'show interface'
    
    def parse_interfaces(self, output):
        lines = []
        interfaces = {}
        current_interface = None
        current_status = None
        
        for line in output.split('\n'):
            line_stripped = line.strip()
            
            if ' is ' in line_stripped and ('up' in line_stripped or 'down' in line_stripped):
                parts = line_stripped.split(' is ')
                if len(parts) >= 2:
                    current_interface = parts[0].strip()
                    current_status = parts[1].split(',')[0].strip()
                    
                    if current_interface not in interfaces:
                        interfaces[current_interface] = {'status': current_status, 'ips': []}
            
            elif 'IPv4 addr' in line and ':' in line and current_interface:
                ip_part = line.split(':', 1)[1].strip().split()[0]
                
                if '/' in ip_part:
                    ip, mask = ip_part.split('/')
                    interfaces[current_interface]['ips'].append((ip, mask))
        
        for interface, data in interfaces.items():
            if data['ips']:
                for ip, mask in data['ips']:
                    lines.append(f"{interface},{data['status']},{ip},{mask}\n")
            else:
                lines.append(f"{interface},{data['status']},,\n")
        
        return lines
    
    def get_config_command(self):
        return 'info flat'
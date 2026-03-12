class MikroTik:
    def get_version_command(self):
        return '/system resource print'
    
    def parse_version(self, output):
        for line in output.split('\n'):
            if 'version:' in line:
                return line.split('version:')[1].strip()
        return "unknown"
    
    def get_lldp_command(self):
        return '/ip neighbor print detail'
    
    def parse_lldp(self, output, own_hostname=None):
        lines = []
        entries = []
        current_entry = []
        
        for line in output.split('\n'):
            line = line.strip()
            if line and line[0].isdigit() and (len(line) > 1 and line[1] == ' '):
                if current_entry:
                    entries.append(' '.join(current_entry))
                current_entry = [line]
            elif current_entry and line and not line.startswith('--'):
                current_entry.append(line)
        
        if current_entry:
            entries.append(' '.join(current_entry))
        
        for entry in entries:
            interface = 'unknown'
            identity = 'unknown'
            neighbor_int = 'unknown'
            
            if 'interface=' in entry:
                interface = entry.split('interface=')[1].split()[0]
            
            if 'identity="' in entry:
                start = entry.find('identity="') + len('identity="')
                end = entry.find('"', start)
                identity = entry[start:end]
            
            if 'interface-name="' in entry:
                start = entry.find('interface-name="') + len('interface-name="')
                end = entry.find('"', start)
                neighbor_int = entry[start:end]
            
            if identity != own_hostname and identity != 'unknown':
                lines.append(f"{interface},{identity},{neighbor_int}\n")
        
        return lines
    
    def get_interface_command(self):
        return '/interface print detail'
    
    def parse_interfaces(self, output):
        lines = []
        entries = []
        current_entry = []
        
        for line in output.split('\n'):
            stripped = line.strip()
            if stripped and stripped[0].isdigit() and 'name=' in stripped:
                if current_entry:
                    entries.append(' '.join(current_entry))
                current_entry = [stripped]
            elif current_entry and stripped and not stripped.startswith('Flags:') and not stripped.startswith('--'):
                current_entry.append(stripped)
        
        if current_entry:
            entries.append(' '.join(current_entry))
        
        for entry in entries:
            interface = 'unknown'
            status = 'unknown'
            
            if 'name="' in entry:
                start = entry.find('name="') + len('name="')
                end = entry.find('"', start)
                interface = entry[start:end]
            
            if ' R ' in entry or entry.startswith('R '):
                status = 'up'
            else:
                status = 'down'
            
            lines.append(f"{interface},{status},,\n")
        
        return lines
    
    def get_config_command(self):
        return '/export'
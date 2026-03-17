from napalm import get_network_driver
import json

driver = get_network_driver("srl")
optional_args = {
	"gnmi_port": 57400,
	"jsonrpc_port": 443,
	"target_name": "clab-aar-lab-r3",
	"tls_ca": "~/AAR/isel-AAR/topology/clab-aar-lab/.tls/ca/ca.pem",
	"encoding": "JSON_IETF"
}

device = driver("clab-aar-lab-r3", "admin", "admin", 60, optional_args)
device.open()
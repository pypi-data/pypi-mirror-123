# ----------------------------------------------------------------------------------------
from nettoolkit import *

from .entity import *
from .static import *

# ----------------------------------------------------------------------------------------
# Control Functions
# ----------------------------------------------------------------------------------------
def network_group_member(spl_line, idx, objectGroups=None):
	"""returns Network group member object from given splitted line, 
	provide index to look at, 
	objectGroups will require if splitted line has object-group.
	"""
	if spl_line[idx] == 'host':
		return Host(spl_line[idx+1])
	elif spl_line[idx] == 'object-group':
		try:
			return ObjectGroup(spl_line[idx+1], objectGroups)		## TBD pass objectGroups
		except:
			return None
	elif spl_line[idx] in ANY:
		return Network(*DEFAULT_ROUTE)
	else: 
		ao = addressing(spl_line[idx])
		if type(ao) == IPv6: 
			return Network(spl_line[idx])
		if type(ao) == IPv4: 
			try:
				return Network(spl_line[idx], spl_line[idx+1])
			except:
				return Network(spl_line[idx])
	raise Exception(f"UndefinedEndPointTypeDetected: {spl_line}\n{idx}")

def port_group_member(spl_line, idx, objectGroups=None):
	"""returns Port group member object from given splitted line, 
	provide index to look at, 
	objectGroups will require if splitted line has object-group.
	"""
	try: spl_line[idx]
	except: return ''
	if 4 < len(spl_line) <= 8:
		pts = Ports("", "")
	elif spl_line[idx] == 'eq':
		pts = Ports(spl_line[idx], spl_line[idx+1])
	elif spl_line[idx] =='range':
		pts = Ports(spl_line[idx], spl_line[idx+1], spl_line[idx+2])
	elif spl_line[idx] == 'object-group':
		try:
			pts = ObjectGroup(spl_line[idx+1], objectGroups)
		except:
			pts = None
			pass													### bypassed temporily
	elif spl_line[idx] in ICMP:
		pts = Ports(spl_line[idx], "")
	elif spl_line[4] == 'icmp':				### Exceptional match for missing icmp ports
		pts = Ports("", 'echo')				  # define port as echo in this case
	elif spl_line[idx] == 'log':
		return ''
	else:
		raise Exception(f"UndefinedPort/TypeDetected: {spl_line} at index {idx}")
	return pts

def icmp_group_member(spl_line):
	pts = IcmpProtocol(spl_line[-1])
	return pts

def protocol_group_member(spl_line):
	pts = NetworkProtocol(spl_line[-1])
	return pts

def group_object_member(spl_line, objectGroups=None):
	try:
		pts = ObjectGroup(spl_line[-1], objectGroups)
	except:
		pts = None	
	return pts


def network_member(network, objs=None):
	"""returns Network group member object for given network, 
	objs will require if network has object-group.
	"""
	if not isinstance(network, str): return network	
	# ----------------------------------------------------
	network = network.strip()
	# ----------------------------------------------------
	if network in ANY: return Network(*DEFAULT_ROUTE)
	# ----------------------------------------------------
	spl_network = network.split("/")
	net_obj = None
	if len(spl_network) == 2:
		net_obj = addressing(network)
		if net_obj:
			mask = int(spl_network[1]) 
			if mask == 32: return Host(spl_network[0])
			return Network(spl_network[0], bin_mask(mask))
	# ----------------------------------------------------
	spl_network = network.split(" ")
	if len(spl_network) == 2:
		if spl_network[0] == 'object-group': return ObjectGroup(spl_network[1], objs)
		mask = to_dec_mask(spl_network[1])
		net = spl_network[0] +"/"+ str(mask)
		net_obj = addressing(net)
		if net_obj: 
			if mask == 32: return Host(spl_network[0])
			return Network(spl_network[0], spl_network[1])
	# ----------------------------------------------------
	else:
		subnet = network + "/32"
		net_obj = addressing(network)
		if net_obj: return Host(network)
	# ----------------------------------------------------
	raise Exception(f"InvalidNetworkOrHost")

def port_member(port, objs):
	"""returns Port group member object for given port, 
	objs will require if port has object-group.
	"""
	port = str(port).strip()
	if port.startswith('eq '): port = port[3:].lstrip()
	if port.startswith('range '): port = port[6:].lstrip()
	if port in ICMP: return Ports("", port)
	# ----------------------------------------------------
	spl_port = port.split(" ")
	if len(spl_port) == 2: 
		if spl_port[0] == 'object-group': return ObjectGroup(spl_port[1], objs)
		return Ports('range', spl_port[0], spl_port[1])
	dspl_port = port.split("-")
	if len(dspl_port) == 2: return Ports('range', dspl_port[0], dspl_port[1])
	elif len(dspl_port) == 1 and len(spl_port) == 1: return Ports('eq', port)
	# ----------------------------------------------------
	raise Exception(f"InvalidPort")

# ----------------------------------------------------------------------------------------

def get_match_dict(request_parameters, objs):
	"""search for request parameters and return matching parameters dictionary.
	(dictionary with attributes require to match in ACL)
	"""
	matching_parameters = ('remark', 'acl_type', 'action', 'protocol', 'source',
		'destination', 'ports',)
	network_member_parameters = ('source', 'destination')
	port_member_parameters = ('ports',)
	matching_dict = {}
	for item in matching_parameters:
		if item in network_member_parameters and item in request_parameters:
			matching_dict[item] = network_member(request_parameters[item], objs)
		elif item in port_member_parameters and item in request_parameters:
			matching_dict[item] = port_member(request_parameters[item], objs)
		elif item in request_parameters:
			matching_dict[item] = request_parameters[item]
	return matching_dict


# ----------------------------------------------------------------------------------------
# Other Functions
# ----------------------------------------------------------------------------------------
def get_port_name(n):
	"""update and return well known port number for port name """
	return PORT_MAPPINGS[n] if PORT_MAPPINGS.get(n) else n

def update_ports_name(requests):
	"""update and return well known port number for port name in given request port"""
	for request in requests: 
		request['ports'] = get_port_name(request['ports'])
	return requests

# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
from nettoolkit import *

from .static import *

# ----------------------------------------------------------------------------------------
# Control Classes
# ----------------------------------------------------------------------------------------
class EntiryProperties():
	def __str__(self): return self._str
	def __repr__(self): return self._str
	def __hash__(self): return self._hash
	def __eq__(self, obj): return str(obj) == str(self)

class Singular(EntiryProperties):
	"""a common class template to create an IcmpProtocol or NetworkProtocol object instance 
	"""
	def __init__(self, _type):
		self._type = _type
		self._str = f'icmp-object {self._type}'.strip()
		self._hash = hash(self._type)
IcmpProtocol = Singular
NetworkProtocol = Singular

class Host(EntiryProperties):
	"""a single ip host object 	"""
	def __init__(self, host):
		self._iphost = addressing(host)
		self._str = f"host {host}"
		self._hash = hash(self._iphost)
		self.version = self._iphost.version
	def split(self): return str(self._iphost).split()

class Network(EntiryProperties):
	"""a network/subnet object 	"""
	def __init__(self, network, dotted_mask=None): 
		if dotted_mask:
			self.mask = to_dec_mask(dotted_mask)
			self._subnet = network + "/" + str(self.mask)
		else:
			self._subnet = network
		self._network = addressing(self._subnet)
		self.version = self._network.version
		self._hash = hash(self._network)
	@property
	def _str(self):
		net = self._network.ipbinmask()
		if net in any4: return 'any4'
		if net in any6: return 'any6'
		return net

class ObjectGroup(EntiryProperties):
	"""networks/ports grouped object """
	def __init__(self, group_name, objectGroups): 
		self.group_name = group_name
		try:
			grp = objectGroups[group_name]
		except:
			raise Exception("ObjectGroupNotPresent")
		self._str = f"object-group {self.group_name}"
		self._hash = grp._hash

class Ports(EntiryProperties):
	"""a port/range-of-ports object """
	def __init__(self, port_type, port, port_range_end='', objectGroups=None): 
		self._set_porttype(port_type)
		# print(">", self.port_type)
		self._set_ports(port, port_range_end, objectGroups)
		# print(">>", self.start, ">>", self.end)
		self._hash = hash(port)

	def split(self): return str(self).split()

	def _set_porttype(self, port_type):
		if port_type in VALID_PORT_MATCHES:
			self.port_type = port_type
			if port_type in ICMP:
				self.port_type = ''
				self.start = port_type				
				self.end = ''
				self._set_mapped_port_numbers(self.start, self.end)
		elif port_type == 'log' or port_type == '':
			self.port_type = ''
			self.start = ''
			self.end = ''
		else:
			raise Exception(f"InvalidPortType{port_type}, Valid options are {VALID_PORT_MATCHES}")

	def _set_mapped_port_numbers(self, start, end):
		# print("___", start, "____", end)
		for k, v in PORT_MAPPINGS.items():
			if v == start: 
				self.start = int(k)
			if v == end: 
				self.end = int(k)
		try: self.end
		except: self.end = ''
		try: self.start
		except: self.start = ''

	def _set_ports(self, start, end, objectGroups):
		if not self.port_type: return None
		if start in PORT_MAPPINGS.values() or end in PORT_MAPPINGS.values():
			self._set_mapped_port_numbers(start, end)
			return
		if self.port_type == 'object-group':
			self.end = ''
			self.start = ObjectGroup(start, objectGroups)
			return
		try:
			self.start = int(start)
		except:
			self.start = start
		try:
			self.end = int(end) if self.port_type == 'range' else ''
		except:
			self.end = end if self.port_type == 'range' else ''

	@property
	def _str(self):
		port = PORT_MAPPINGS[self.start] if self.start in PORT_MAPPINGS else self.start
		port_end = PORT_MAPPINGS[self.end] if self.end in PORT_MAPPINGS else self.end
		port_end = f' {port_end}' if port_end else ''
		port_type = f'{self.port_type} ' if self.port_type else ''
		return f'{port_type}{port}{port_end}'.strip()

	def __contains__(self, port):
		end = self.start if not self.end else self.end
		for k, v in PORT_MAPPINGS.items():
			if v == port: port = k
		try:
			return self.start <= port <= end
		except:
			print(f"Invalid Port to check within [{self.start} <= {port} <= {end}]")


# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------

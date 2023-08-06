# ----------------------------------------------------------------------------------------
from nettoolkit import *
from collections import OrderedDict
from copy import deepcopy

from .acg import OBJ
from .member import *
from .entity import *
from .static import *
from .fwObj import *

# ----------------------------------------------------------------------------------------
# Local Functions
# ----------------------------------------------------------------------------------------
def access_list_list(config_list):
	"""extracts access-lists from provided configuration list ie.config_list.
	returns access-lists lines in a list
	"""
	return [line.rstrip() for line in config_list if line.startswith("access-list ")]


# ----------------------------------------------------------------------------------------
# Access Lists Entries
# ----------------------------------------------------------------------------------------
class ACLS(Plurals):
	"""collection of ACL objects

	:: Instance variables ::
	acls_list : access-lists in a list
	_repr_dic: access-lists (ACL)s  in a dictionary

	"""
	def __init__(self, config_list, objs=None):
		super().__init__()
		self.what = "access-lists"
		self.acls_list = access_list_list(config_list)
		self.set_acl_names()
		self.set_objects(objs)

	def changes(self, change): return super().changes('acl', change)

	# ~~~~~~~~~~~~~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~

	def set_acl_names(self):
		"""sets available access-lists names in _repr_dic (key) """
		for acl_line in self.acls_list:
			spl_acl_line = acl_line.split()
			acl_name = spl_acl_line[1]
			if acl_name not in self._repr_dic: self._repr_dic[acl_name] = []
			self._repr_dic[acl_name].append(acl_line)
		return self._repr_dic

	# def set_acl_objects(self, objs):
	def set_objects(self, objs):
		"""sets access-lists (ACL)s in _repr_dic (value) """
		for acl_name, acl_lines_list in self._repr_dic.items():
			acl =  ACL(acl_name, acl_lines_list, objs)
			acl.parse(objs)
			self._repr_dic[acl_name] = acl

# ----------------------------------------------------------------------------------------
# Access List detail
# ----------------------------------------------------------------------------------------
class ACL(Singulars):
	"""Individual access-list object

	:: Instance variables ::
	acl_name:  access-list name
	acl_lines_list: access-list in list format
	_repr_dic: access-list details in a dictionary format key as acl line number, value as acl line attributes dictionary.

	:: Class variables ::
	end_point_identifiers_pos:  index of src, dst and port on acl line number
	mandatory_item_values_for_str: keys of acl lines

	:: Properties ::
	max: maximum line number on acl
	min: minimum line number on acl
	sequence: boolean property to display/hide line numbers

	"""
	end_point_identifiers_pos = {	# static index points 
		0: 5,						# src
		1: 7,						# dst
		2: 9,						# port
	}
	mandatory_item_values_for_str = ('acl_type', 'action', 'protocol',
		'source', 'destination', 'ports', 'log_warning' )

	def __init__(self, acl_name, acl_lines_list, objs):
		super().__init__(acl_name)
		self.acl_lines_list = acl_lines_list
		self.objs = objs
		self.adds = ''
		self.removals = ''
		self._sequence = False
		self._repr_dic = OrderedDict()
	def __iter__(self):
		for k, v in sorted(self._repr_dic.items()):
			yield (k, v)
	def __getitem__(self, item):
		if isinstance(item, slice):
			return ''.join([self[i] for i in range(*item.indices(len(self)))])
		else:
			try:
				return self._to_str(item)
			except KeyError:
				return None
	def __delitem__(self, item): self.delete(item)
	@property
	def max(self): return max(self._repr_dic.keys())
	@property
	def min(self): return min(self._repr_dic.keys())
	@property 	             ## Boolean: sequence number visibility
	def sequence(self): return self._sequence
	@sequence.setter
	def sequence(self, seq): self._sequence = seq
	def __add__(self, attribs):  return self.copy_and_append(attribs)
	def __sub__(self, n): return self.copy_and_delete(n)
	def __iadd__(self, attribs): 
		self.append(attribs)
		return self
	def __isub__(self, n): 
		self.delete(n)
		return self
	def __eq__(self, obj):
		for k, v in obj:
			if k in self._repr_dic and self._repr_dic[k] == v: continue
			else: return False
		return True
	def __gt__(self, obj):
		diffacl = ACL(self._name, None, self.grp)
		for self_k, self_v in self._repr_dic.items():
			found = False
			for obj_k, obj_v in obj._repr_dic.items():
				found = self_v == obj_v
				if found: break
			if not found: diffacl[self_k] = self_v
		return diffacl
	def __lt__(self, obj):
		diffacl = ACL(self._name, None, self.grp)
		for obj_k, obj_v in obj._repr_dic.items():
			found = False
			for self_k, self_v in self._repr_dic.items():
				found = self_v == obj_v
				if found: break
			if not found: diffacl[obj_k] = obj_v
		return diffacl
	def __contains__(self, item): return self.contains(item)
		
	# ~~~~~~~~~~~~~~~~~~~ EXTERNAL CALLABLES ~~~~~~~~~~~~~~~~~~~

	# String representation of full acl	
	def str(self):
		s = ''
		for k, v in self:
			s += self[k]
		return s

	# String representation of object-group additions / removals
	def add_str(self): return str(self.adds)
	def del_str(self): return str(self.removals)

	# delete a line in acl:  usage= del(acl_name[n])
	def delete(self, attribs, stop=None, step=1): 
		if isinstance(attribs, int):
			if stop and isinstance(stop, int):
				s = ''
				for i in reversed(range(attribs, stop, step)):
					s += self.delete(i)
				return s
			else:
				return self.delete_by_line(attribs)
		elif isinstance(attribs, dict):
			return self.delete_by_attribs(attribs)
		elif isinstance(attribs, slice):
			for i in reversed(range(*attribs.indices(len(self)))):
				self.delete(i)
		else:
			print(f"Incorrect input to delete {attribs}")
			return None

	# delete a line in acl:  usage= del(acl_name[n])
	def delete_by_line(self, line_no):
		removals = self._del_str(line_no)
		self.removals += removals
		self._key_delete(line_no)
		self._key_deflate(line_no)
		return removals

	# delete a line in acl by attrib
	def delete_by_attribs(self, attribs):
		mv = self._matching_value(attribs)
		if mv: return self.delete_by_line(mv)

	# insert a line in acl: usage=  aclname[line_no] = attribs
	def insert(self, line_no, attribs):
		mv = self._matching_value(attribs)
		if not mv:
			self._key_extend(line_no)
			return self._add(line_no, attribs)
		else:
			print(f"MatchingEntryAlreadyexistAtLine-{mv}")

	# append a line in acl: 
	def append(self, attribs):
		mv = self._matching_value(attribs)
		if not mv:
			return self._add(self.max+1, attribs)
		else:
			print(f"MatchingEntryAlreadyexistAtLine-{mv}")


	def has(self, item):
		"""check matching item in acl object src/dst/port, 
		useful for Boolean check (returns a line number if match else False)
		"""
		for line_no, acl_details in  self:
			if not isinstance(acl_details, dict): continue
			acl_src = acl_details['source']
			acl_dst = acl_details['destination']
			acl_prt = acl_details['ports']
			if ((isinstance(acl_src, ObjectGroup) and acl_src.grp == item) 
				or (isinstance(acl_dst, ObjectGroup) and acl_dst.grp == item) 
				or (isinstance(acl_prt, ObjectGroup) and acl_prt.grp == item)
				):
				return line_no
		return False

	def contains(self, item, all=False):
		"""check matching attributes in acl object, 
		return matching acl line numbers list (all matching lines)
		"""
		matching_lines = []
		item = self._update_group_members(item)
		item = self._network_to_host(item)
		for line_no, acl_details in  self:
			if isinstance(acl_details, dict):
				for k, v in item.items():
					if k == 'log_warning': continue
					if isinstance(acl_details[k], ObjectGroup) and isinstance(v, OBJ):
						if len(acl_details[k].grp > v): break
					elif acl_details[k] != v:
						break
				else:
					if not all: return line_no
					matching_lines.append(line_no)
		return matching_lines


	# ---------------- Operate on a Copy --------------- 	

	def copy_and_append(self, attribs):
		"""create duplicate of self, append a new acl line in new object with provided attributes """
		newobj = deepcopy(self)
		newobj.append(attribs)
		return newobj

	def copy_and_delete(self, attribs):
		"""create duplicate of self, delete a line in new acl for given line number/attributes"""
		newobj = deepcopy(self)
		newobj -= attribs
		return newobj

	def copy_and_insert(self, line_no, attribs):
		"""create duplicate of self, insert a new acl line in new acl object,
		with provided attributes at given line number and return new updated object.
		existing object remains untouched
		"""
		newacl = deepcopy(self)
		newacl.insert(line_no, attribs)
		return newacl

	# ~~~~~~~~~~~~~~~~~~~ INTERNALS / SUPPORTIVE ~~~~~~~~~~~~~~~~~~~

	# supportive: insert a new line at position n
	def _key_extend(self, n):
		rvs_keys = list(reversed(self._repr_dic.keys()))
		for key in rvs_keys:
			if key >= n: self[key+1] = self._repr_dic[key]
			else: break

	# supportive: deletes a line
	def _key_delete(self, n):
		try:
			del(self._repr_dic[n])
		except:
			print(f"NoDeletableEntryFoundForLine-{n}-orAlreadyRemoved")

	# supportive: rearranges next lines
	def _key_deflate(self, n):
		last_used_key = self.max
		for key in range(n, last_used_key):
			self[key] = self._repr_dic[key+1]
		del(self._repr_dic[last_used_key])

	# supportive : update member per std and insert entry to acl
	def _add(self, line_no, attribs):
		attribs = self._update_members(attribs)
		attribs = self._update_remarks(line_no, attribs)
		self[line_no] = attribs
		adds = self._to_str(line_no)
		self.adds += adds
		return adds

	# supportive : attributes update as per std source/destination/port/remark
	def _update_members(self, attribs):
		attribs = self._update_group_members(attribs)
		attribs = self._network_to_host(attribs)
		return attribs

	# supportive : attributes update for remark field
	def _update_remarks(self, n, attribs):
		if not attribs.get('remark') :
			attribs['remark'] = self._repr_dic[n-1]['remark']
		return attribs

	# supportive : attributes update as per std source/destination/port
	def _update_group_members(self, attribs):
		attribs['source'] = network_group_member(attribs['source'].split(), idx=0, objectGroups=self.objs)
		attribs['destination'] = network_group_member(attribs['destination'].split(), idx=0, objectGroups=self.objs)
		attribs['ports'] = port_group_member(attribs['ports'].split(), idx=0, objectGroups=self.objs)
		return attribs

	# supportive : attributes change from Network to Host 
	def _network_to_host(self, attribs):
		for k,v in attribs.items():
			if isinstance(v, Network):
				spl_v = str(v).split()
				attribs[k] = Host(spl_v[0])
		return attribs	

	# ----------------- String repr / supportive --------------- #

	# return String representation of an acl-line (n)
	def _to_str(self, n):
		seq = self.sequence
		seq_no = f"line {n} " if seq else ""
		item = self._repr_dic[n]
		if isinstance(item, dict):
			for v in self.mandatory_item_values_for_str:
				if v not in item:
					item[v] = self._normalize(v)
			log_warning = " log warning" if item['log_warning'] else ""
			s = (f"access-list {self._name} {seq_no}"
				 f"{item['acl_type']} {item['action']} {item['protocol']} "
				 f"{item['source']} {item['destination']} {item['ports']}{log_warning}\n")
		else:
			s = f"access-list {self._name} {seq_no}{item}"
		return s

	# return negating string of an acl-line (n)
	# usage: del(acl[n:n+x:step]) to delete acl entry(ies).
	# get deleted entries using property acl.removals
	def _del_str(self, n=0):
		s = ''
		if n and isinstance(n, int): 
			return "no " + self._to_str(n)
		elif n and isinstance(n, (list, tuple, set)):
			for i in n: s += self._del_str(i)
		elif not n:
			for n, v in self: s += self._del_str(n)
		return s 

	## ----------- Other Supportive to Supportives --------- ##

	# line number of an acl for matching attributes
	def _matching_value(self, attribs):
		attribs = self._update_members(attribs)
		for line_no, acl_details in self:
			match = False
			for k_attr, v_attr in attribs.items():
				if isinstance(acl_details, ACL_REMARK): break
				match = acl_details[k_attr] == v_attr
				if not match: break
			if match: return line_no

	# return default attributes for the require item/attribute.
	def _normalize(self, item):
		normalize_item_values = {
			'acl_type': 'extended', 
			# 'action': 'permit', 
			# 'protocol': 'tcp', 
			# 'source': , 
			# 'destination': , 
			# 'ports': , 
			'log_warning': True,
			}
		if normalize_item_values.get(item):
			return normalize_item_values[item]
		else:
			raise Exception(f"MissingMandatoryParameter-{item}, NormalizationNotAvailableForMandatoryField")


	# ~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~~
	# USED WHILE INITIATLIZING / PARSER
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def parse(self, objs):
		"""parse access-list-lines-list and set _repr_dic.  
		objs requires for acl lines having object-group-names
		"""
		remark = None
		for line_no, line in enumerate(self.acl_lines_list):
			test = line.startswith("access-list al_from_blue extended deny tcp any4 any4 object-group INET-TCP-DROP")
			spl_line = line.split()
			# remarks line
			if spl_line[2] == 'remark':
				remark = " ".join(spl_line[3:])
				self._repr_dic[line_no] = ACL_REMARK(remark)
				continue
			# src /dst / ports
			idx_variance = 0
			protocol_variance = 1 if spl_line[4] == "object-group" else 0
			for k, v in self.end_point_identifiers_pos.items():
				pv = v+protocol_variance+idx_variance
				if k == 0: source      = network_group_member(spl_line, idx=pv, objectGroups=objs)
				if k == 1: destination = network_group_member(spl_line, idx=pv, objectGroups=objs)
				if k == 2: ports       = port_group_member(spl_line, idx=pv, objectGroups=objs)
				try:
					if spl_line[pv] in ANY: idx_variance -= 1
				except:
					pass
			# add rest statics and create ACL entry dict
			self._repr_dic[line_no] = {
				'remark': remark,
				'acl_type': spl_line[2],
				'action': spl_line[3],
				'protocol': spl_line[4+protocol_variance],
				'source': source,
				'destination': destination,
				'ports': ports,
				'log_warning': STR.found(line, 'log warnings'),
			}

# ----------------------------------------------------------------------------------------
# Access List Entry Candidates
# ----------------------------------------------------------------------------------------

class ACL_REMARK():
	"""ACL remark object
	:: Instance variables ::
	remark: acl remark ( returns as str of obj )
	"""
	def __init__(self, remark): self.remark = remark
	def __str__(self): return self.str()
	def __repr__(self): return self.remark
	def __eq__(self, obj): return str(obj) == str(self)
	def str(self): return self.remark + "\n"


# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------

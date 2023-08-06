# ----------------------------------------------------------------------------------------
from nettoolkit import *
from collections import OrderedDict
from copy import deepcopy

from .member import *
from .entity import *
from .static import *
from .fwObj import *

# ----------------------------------------------------------------------------------------
# Local Functions
# ----------------------------------------------------------------------------------------

def _object_group_list(config_list):
	"""extracts obect groups from provided configuration list ie.config_list 
	returns object groups (OBJ)s in a list"""
	obj_grp_list = []
	obj_group_started = False
	for line in config_list:
		spaces = STR.indention(line)
		if line.startswith("object-group"): 
			obj_group_started = True
			obj_grp_list.append(line.rstrip())
			continue
		if obj_group_started and spaces > 0:
			obj_grp_list.append(line.rstrip())
			continue
		if obj_group_started:
			break
	return obj_grp_list


def get_member_obj(member_type, member, objs):
	"""convert and provided string member to member object aka: Host, Network, ObjectGroup, Ports based on its member-type provided.
	objs: requires for recursive lookup for ObjectGroup (if any)"""
	member_type_map = {
		'port-object': port_member,
		'network-object': network_member,
		'icmp-object': None,		# TBD
		'group-object': None,		# TBD
		'protocol-object': None,	# TBD
		# ... add more as need
	}
	if member_type not in member_type_map: 
		raise Exception(f"InvalidMemberTypeDefined-{member_type} for member-{member}")
	return member_type_map[member_type](member, objs)



# ----------------------------------------------------------------------------------------
# Collection of Object Group(s) objects
# ----------------------------------------------------------------------------------------
class OBJS(Plurals):
	"""collection of object groups """
	def __init__(self, config_list):
		super().__init__()
		self.what = "object-groups"
		self.obj_grps_list = _object_group_list(config_list)
		self._set_obj_grp_basics()
		self.set_objects()

	def changes(self, change): return super().changes('object-group', change)

	# ~~~~~~~~~~~~~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~

	def get_matching_obj_grps(self, requests):
		"""matches provided (request members) in all object-groups available on device and 
		returns dictionary of object-group names. 
		where object-group matches same members in it.
		requests: list/set/tuple with members of dict, 
		         containing 'source', 'destination', 'ports' as keys.
		--> dict ( include all three, src, dest, port)
		"""
		candidates = {'source': [], 'destination': [], 'ports': []}
		group_names = {}
		if not isinstance(requests, (tuple, list, set)):
			raise Exception(f"NotValidRequestProvided-{requests}")
		for request in requests:
			for loc, member in candidates.items():
				if request[loc] in ANY: continue
				member.append(request[loc])
		for loc, member in candidates.items():
			obj_grps_list = self.matching_obj_grps(member)
			if obj_grps_list:
				group_names[loc] = obj_grps_list
		return group_names

	def matching_obj_grps(self, member):
		"""matches provided [members] in all object-groups available on device and 
		returns list of object-group names. 
		where object-group matches same members in it.
		member: list/set/tuple with members, 
		--> list ( singular )
		"""
		if isinstance(member, str):
			return [obj for name, obj in self if member in obj]
		elif isinstance(member, (tuple, list, set)):
			g = []
			for name, obj in self:
				match = False
				for m in member:
					match = m in obj
					if not match: break
				if match and len(obj) == len(member): g.append(obj)
			return g

	# ~~~~~~~~~~~~~~~~~~~ INTERNALS ~~~~~~~~~~~~~~~~~~~

	# set basic information of each object-group.
	def _set_obj_grp_basics(self):
		obj_grp_name = None
		for obj_grps_line in self.obj_grps_list:
			spaces = STR.indention(obj_grps_line)
			if spaces == 0:
				spl_obj_grps_line = obj_grps_line.split()
				obj_grp_type = spl_obj_grps_line[1]
				obj_grp_name = spl_obj_grps_line[2]
				if obj_grp_name not in self._repr_dic: self._repr_dic[obj_grp_name] = {}
				self._repr_dic[obj_grp_name]['type'] = obj_grp_type
				self._repr_dic[obj_grp_name]['candiates_list'] = []
				try:
					obj_grp_svc_filter = spl_obj_grps_line[3]
					self._repr_dic[obj_grp_name]['svc_filter'] = obj_grp_svc_filter
				except:
					self._repr_dic[obj_grp_name]['svc_filter'] = ""
			else:
				self._repr_dic[obj_grp_name]['candiates_list'].append(obj_grps_line)
		return self._repr_dic

	# set extended information of each object-group.
	def set_objects(self):
		h = 0
		for obj_grp_name, obj_grp_details in self._repr_dic.items():
			obj_grp = OBJ(obj_grp_name, h)
			obj_grp.set_instance_primary_details(obj_grp_details)
			obj_grp.parent = self
			obj_grp.parse()
			self._repr_dic[obj_grp_name] = obj_grp
			h += 1

# ----------------------------------------------------------------------------------------
# Object Group Detail
# ----------------------------------------------------------------------------------------
class OBJ(Singulars):
	"""Individual group object """

	# valid_member_types = VALID_MEMBER_TYPES

	def __init__(self, obj_grp_name, _hash):
		super().__init__(obj_grp_name)
		self.description = ""
		self.removals = {}
		self.adds = {}
		self._hash = _hash
	def __eq__(self, obj): 
		return (((self>obj) is None) 
			and ((obj>self) is None) 
			# and (self.description == obj.description)
			)
	def __len__(self): return self._len_of_members()
	def __contains__(self, member): return self._contains(member)
	def __iadd__(self, n): 
		self._add(n)
		return self
	def __isub__(self, n): 
		self._delete(n)
		return self
	def __gt__(self, obj):
		diffs = self._missing(obj)
		obj_grp = self._blank_copy_of_self()
		obj_grp._repr_dic = diffs
		if diffs: return obj_grp
	def __lt__(self, obj):
		diffs = obj._missing(self)
		obj_grp = self._blank_copy_of_self()
		obj_grp._repr_dic = diffs
		if diffs: return obj_grp
	def __add__(self, attribs): 
		newobj = deepcopy(self)
		newobj += attribs
		return newobj
	def __sub__(self, attribs): 
		newobj = deepcopy(self)
		newobj._delete(attribs)
		return newobj

	# ~~~~~~~~~~~~~~~~~~~ EXTERNAL CALLABLES ~~~~~~~~~~~~~~~~~~~

	# String representation of full object-group
	def str(self):
		s = self._group_head()
		s += self._group_description()
		s += self._to_str(self._repr_dic, header=False)
		return s

	# object-group additions / removals
	def add(self, *arg): return self._add(*arg)
	def delete(self, *arg): return self._delete(*arg)

	# String representation of object-group additions / removals
	def add_str(self, header=True): return self._to_str(self.adds)
	def del_str(self, header=False): return self._to_str(self.removals)


	# ---------------- Operate on a Copy --------------- 	

	# create and return a copy of original instance
	def _blank_copy_of_self(self):
		obj_grp = OBJ(self._name, self._hash*1)
		obj_grp.set_instance_primary_details(self.grp_details)
		return obj_grp


	# ~~~~~~~~~~~~~~~~~~~ INTERNALS / SUPPORTIVE ~~~~~~~~~~~~~~~~~~~

	# supporting len() : count of total members
	def _len_of_members(self):
		l = 0
		for v in self._repr_dic.values():
			l += len(v)
		return l

	# supporting - x in/not in instance: 
	# check existance of member(s) in object instance
	def _contains(self, member):
		if isinstance(member, (str, int)):
			member_type = self._get_member_type(member)
			member_obj = get_member_obj(member_type, member, self.parent)
			if isinstance(member_obj, Host):
				member_obj = Network(member_obj.split()[-1])
			if not self[member_type]: return None
			for _ in self[member_type]:
				if member_obj == _: 
					return _
				elif isinstance(_, ObjectGroup):
					if self.parent[_.group_name]._contains(member):
						return _
		elif isinstance(member, (list,set,tuple)):
			for m in member:
				if m not in self: return False
			return True

	# supporting inst.add(member) : method for setting key/value for instance
	def _add(self, item):
		if isinstance(item, (tuple, set, list)):
			s = ''
			for _ in item:  
				s += self._add(_)
			return s
		elif isinstance(item, (str, int)):
			item_type = self._get_member_type(item)
			updated_item = self._get_item_object(item_type, item)
			return self._obj_add(item_type, updated_item)
		else:
			raise Exception(f"IncorrectIteminItemType-{item}")


	# supporting inst.delete(member) : method for removing key/value for instance
	def _delete(self, item):
		if isinstance(item, (tuple, set, list)):
			s = ''
			for _ in item: 
				s += str(self._delete(_))
			return s
		elif isinstance(item, (str, int)):
			item_type = self._get_member_type(item)
			updated_item = self._get_item_object(item_type, item)
			return self._obj_delete(item_type, updated_item)
		else:
			raise Exception(f"IncorrectIteminItemType-{item}")

	# supporting in comparision between to instances (a > b, a < b):
	# compare and return differences in dictionary,
	def _missing(self, obj):
		diffs = {}
		t = self.obj_grp_type == obj.obj_grp_type
		s = self.obj_grp_svc_filter == obj.obj_grp_svc_filter
		if not t or not s:
			return diffs

		for self_k, self_v in self._repr_dic.items():
			obj_v = obj[self_k]
			if obj_v is None:
				diffs[self_k] = self_v
			else:
				found = self_v == obj_v
				if found: continue
				diffs[self_k] = self_v.difference(obj_v)
		return diffs


	# ----------------- String repr / supportive --------------- #

	# return String representation of object-group header/name line
	def _group_head(self):
		return (f"object-group {self.obj_grp_type} {self._name} {self.obj_grp_svc_filter}\n")

	# return String representation of object-group description line
	def _group_description(self):
		return (f" description {self.description}\n")

	# return String representation of object-group ( add/remove )
	def _to_str(self, dic, header=True):
		s = self._group_head() if header else ""		
		m = ''
		negate = 'no ' if dic is self.removals else ''
		for _type, candidates in dic.items():
			for c in candidates:
				m += f" {negate}{_type} {c}\n"
		s += m
		return s if m else m

	## ----------- Other Supportive to Supportives --------- ##

	# supporting method for retriving member-type/member pair for for a member
	def _get_item_object(self, item_type, item):
		spl_line = [item_type]
		spl_line.extend(item.split())
		updated_item = self._get_member(item_type, spl_line)
		return updated_item

	# supporting method for retriving member object for provided object-type 
	# ex: Host, Network…
	def _get_member(self, obj_type, spl_line):
		if obj_type == 'network-object':
			member = network_group_member(spl_line, 1, self.parent)
		elif obj_type == 'port-object':
			member = port_group_member(spl_line, 1, self.parent)
		elif obj_type == 'icmp-object':
			member = icmp_group_member(spl_line)
		elif obj_type == 'protocol-object':
			member = protocol_group_member(spl_line)
		elif obj_type == 'group-object':
			member = group_object_member(spl_line, self.parent)
		else:
			raise Exception(f"InvalidGroupMemberType-Noticed-[{obj_type}]\n{spl_line}")
		return member

	# supporting method for setting key/value for instance
	def _obj_add(self, item_type, item):
		if not self.adds.get(item_type): self.adds[item_type] = set()
		if not self._repr_dic.get(item_type): self._repr_dic[item_type] = set()
		self._repr_dic[item_type].add(item)
		self.adds[item_type].add(item)
		return f" {item_type} {item}\n"

	# supporting method for removing key/value for instance
	def _obj_delete(self, item_type, item):
		if not self.removals.get(item_type): self.removals[item_type] = set()
		try:
			self._repr_dic[item_type].remove(item)
			self.removals[item_type].add(item)
			if len(self._repr_dic[item_type]) == 0:
				del(self._repr_dic[item_type])
			return f" no {item_type} {item}\n"
		except:
			print(f"NoValidCandidateFoundToRemove/OrAlreadyRemoved-\n{item_type}: {item}")			

	# dynamic detection of member-type for given member
	def _get_member_type(self, member):
		for k, v in MEMBERS_MEMBERTYPES.items():
			if member in k: return v
		try:
			network_member(member, self.parent)
			return 'network-object'
		except:
			pass
		try:
			port_member(member, self.parent)
			return 'port-object'
		except:
			pass
		if isinstance(member, str) and member in self.parent:
			return 'group-object'
		raise Exception(f"InvalidMemberFound:{member}, unable to generate member type for it.")



	# ~~~~~~ CALLABLE ~~~~~~~~~~~~~~~~~~~
	# USED WHILE INITIATLIZING / PARSER
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def set_instance_primary_details(self, obj_grp_details):
		"""set primary variable details of instance """
		self.obj_grp_lines_list = obj_grp_details['candiates_list']
		self.obj_grp_type = obj_grp_details['type']
		self.obj_grp_svc_filter = obj_grp_details['svc_filter']

	def parse(self):
		"""parse object-group-config-lines-list and set extended variables of instance """
		for line in self.obj_grp_lines_list:
			spl_line = line.lstrip().split()
			sub_obj_type = spl_line[0]
			if sub_obj_type == 'description':
				self.description = line[13:]
				continue
			member = self._get_member(spl_line[0], spl_line)
			if not self._repr_dic.get(spl_line[0]): self._repr_dic[spl_line[0]] = set()
			self._repr_dic[spl_line[0]].add(member)

	# ~~~~~~~~~~~~~~~~~~~ PROPERTIES ~~~~~~~~~~~~~~~~~~~

	@property
	def grp_details(self):
		"""object group details in dictionary (helpful in generating copy) """
		_grp_details = {
			'type': self.obj_grp_type,
			'svc_filter': self.obj_grp_svc_filter,
			'candiates_list': [],
		}
		return _grp_details
	


# ----------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------------------------

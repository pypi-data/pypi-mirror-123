from .static import *

# what = acl/object-group
# name = acl/object-group name 
# change = adds/removals
def heading(what, name, change):	
	matter = f'! {change} - for the {what}: {name}\n'
	return LINE_SNG+matter+LINE_SNG
from mojo.roboFont import CurrentFont

def make_component_current_font():
	f = CurrentFont()
	keys = f.keys()

	for key in keys:
		name = 'uni%x' %f[key].unicode
		f.newGlyph(name)
		f[name].appendComponent(key)
		f[name].width = f[key].width
		f[name].leftMargin = f[key].leftMargin
		f[name].rightMargin = f[key].rightMargin
		f[name].unicodes = f[key].unicodes

make_component_current_font()
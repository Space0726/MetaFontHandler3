import os
import contour_parser1
import contour_parser2
import contour_parser3

def base_maker(wd):
	contour_parser1.contour_parser1(wd)
	contour_parser2.contour_parser2(wd)
	contour_parser3.contour_parser3(wd)

	amolang_start = '''<?xml version="1.0" encoding="UTF-8"?>
	<glyph name="1" format="1">
		<advance width="1000"/>
		<outline>
	'''
	amolang_end = '''\t</outline>\n</glyph>'''

	path = wd + '/glyphs/'
	dir_list = os.listdir(path)
	os.chdir(path)
	for glyph in dir_list:
		os.chdir(glyph)
		glif_list = os.listdir('.')
		if glyph + '.glif' in glif_list:
			glif_list.remove(glyph + '.glif')
		for junk in glif_list:
			if 'junk' in junk:
				unicod = junk.replace('.junk', '')
				glif_list.remove(junk)
				os.system('rm ' + unicod + '.junk')

		f = open(glyph + '.glif', 'w')
		amolang_fixed = amolang_start.replace('<outline>', '<unicode hex="' + unicod + '"/>\n\t<outline>')
		amolang_fixed = amolang_fixed.replace('name="1"', 'name="' + glyph + '"')
		f.write(amolang_fixed)

		sorting = []

		for glif in glif_list:
			f.write('\t\t<component base="' + glif.replace('.glif', '') + '"/>\n')

		f.write(amolang_end)
		f.close()
		os.chdir('..')

	return path



'''
<?xml version="1.0" encoding="UTF-8"?>
<glyph name="1" format="1">
    <advance width="1000"/>
    <outline>
        <component base="meup_i"/>
        <component base="meup_ii"/>
        <component base="meup_iii"/>
        <component base="meup_iv"/>
        <component base="meup_v"/>
    </outline>
</glyph>
'''

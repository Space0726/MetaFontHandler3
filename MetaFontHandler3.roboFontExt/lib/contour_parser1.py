#coding: utf-8
import os, sys, pickle , getpass
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, SubElement, dump
from xml.etree.ElementTree import ElementTree

def contour_parser1(wd):
	indices = { 'giyeok': 0xAC00, 'db_giyeok': 0xAE4C, 'nieun': 0xB098, 'digeut': 0xB2E4 , 'db_digeut': 0xB530, 'rieul': 0xB77C, 'mieum': 0xB9C8, 'bieup': 0xBC14, 'db_bieup': 0xBE60,
	          'siot': 0xC0AC, 'db_siot': 0xC2F8, 'ieung': 0xC544, 'jieut': 0xC790, 'db_jieut': 0xC9DC, 'chieut': 0xCC28, 'kieuk': 0xCE74, 'tieut': 0xD0C0, 'pieup': 0xD30C, 'hieut': 0xD558 }
	middle1 = { 'a': 0, 'ae': 1, 'ya': 2, 'yae': 3, 'eo': 4, 'e': 5, 'yeo': 6, 'ye': 7, 'o': 8, 'wa': 9, 'wae': 10,
	          'oe': 11, 'yo': 12, 'u': 13, 'wo': 14, 'we': 15, 'wi': 16, 'yu': 17, 'eu': 18, 'ui': 19, 'i': 20 }
	middle = { 0: 'a', 1: 'ae', 2: 'ya', 3: 'yae', 4: 'eo', 5: 'e', 6: 'yeo', 7: 'ye', 8: 'o', 9: 'wa', 10: 'wae',
	           11: 'oe', 12: 'yo', 13: 'u', 14: 'wo', 15: 'we', 16: 'wi', 17: 'yu', 18: 'eu', 19: 'ui', 20: 'i' }
	indices1 = { 'g': 0xAC00, 'gg': 0xAE4C, 'n': 0xB098, 'd': 0xB2E4 , 'dd': 0xB530, 'r': 0xB77C, 'm': 0xB9C8, 'b': 0xBC14, 'bb': 0xBE60,
	          's': 0xC0AC, 'ss': 0xC2F8, '': 0xC544, 'j': 0xC790, 'jj': 0xC9DC, 'ch': 0xCC28, 'k': 0xCE74, 't': 0xD0C0, 'p': 0xD30C, 'h': 0xD558 }
	final = { 0: '', 1: 'g', 2: 'gg', 3: 'gs', 4: 'n', 5: 'nj', 6: 'nh', 7: 'd', 8: 'l', 9: 'lg', 10: 'lm', 11: 'lb', 12: 'ls', 13: 'lt', 14: 'lp', 15: 'lh', 16: 'm', 17: 'b', 18: 'bs', 19: 's', 20: 'ss', 21: 'ng', 22: 'j', 23: 'ch', 24: 'k', 25: 't', 26: 'p', 27: 'h' }

	roman = { 1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi', 7: 'vii', 8: 'viii', 9: 'ix', 10: 'x' }

	initial = { 'g': 'giyeok', 'gg': 'double_giyeok', 'n': 'nieun', 'd': 'digeut', 'dd': 'double_digeut', 'r': 'rieul', 'm': 'mieum', 'b': 'bieup', 'bb': 'double_bieip', 's': 'siot', 'ss': 'double_siot', '': 'ieung', 'j': 'jieut', 'jj': 'double_jieut', 'ch': 'chieut', 'k': 'kieuk', 't': 'tieut', 'p': 'pieup', 'h': 'hieut' }
	batchim = { '': '', 'g': 'giyeok', 'gg': 'double_giyeok', 'gs': 'giyeok_siot', 'n': 'nieun', 'nj': 'nieun_jieut', 'nh': 'nieun_hieut', 'd': 'digeut', 'l': 'rieul', 'lg': 'rieul_giyeok', 'lm': 'rieul_mieum', 'lb': 'rieul_bieup', 'ls': 'rieul_siot', 'lt': 'rieul_tieut', 'lp': 'rieul_pieup', 'lh': 'rieul_hieut', 'm': 'mieum', 'b': 'bieup', 'bs': 'bieup_siot', 's': 'siot', 'ss': 'double_siot', 'ng': 'ieung', 'j': 'jieut', 'ch': 'chieut', 'k': 'kieuk', 't': 'tieut', 'p': 'pieup', 'h': 'hieut' }


	base_glif = '''<?xml version="1.0" encoding="UTF-8"?>
	<glyph name="1" format="1">
		<advance width="1000"/>
		<outline>
	place holder
		</outline>
	</glyph>
	'''
	base_glif_backup = base_glif
	replacer = '''<component base="'''

	amolang_start = '''<glyph format="1" name="putnamehere">
		<advance width="973" />
	'''
	amolang_end = '''</glyph>
	'''


	cho = 0
	joong = 0
	jong = 0


	path = wd + '/glyphs1/'
	os.chdir(path)

	glif_list = os.listdir(path)
	glif_name = ''
	uni_dic = {}
	contour = []
	parts_num = 1
	userpath = '/Users/'+getpass.getuser()

	for glif in glif_list:
		if glif.endswith('.plist'):
			continue

		elif glif.endswith('.glif') and glif.startswith('uni'):
			f = open(path + glif, 'r')
			g = open(userpath + '/Library/Application Support/RoboFont/plugins/MetaFontHandler.roboFontExt/lib/hanuni.txt', 'r')

			hanuni = g.readlines()
			for each in hanuni:
				each = each.split('\t')
				each[1] = each[1].rstrip('\r\n')
				uni_dic[each[1]] = each[0]
			g.close()

			glif_name = glif.rstrip('_.glif')	
			glif_name = glif_name.rstrip('_')	
			glif_name = glif_name.rstrip('_')			
			glif_name = glif_name.rstrip('_')			
			glif_name = glif_name.rstrip('_')			
			glif_name = glif_name.rstrip('_')			
			glif_name = glif_name.lstrip('uni')

			temp = 0x024C
			for index in indices1:
				value = ord(unicode(uni_dic[glif_name], 'utf8')) - indices1[index]
				if 0 <= value and value < temp:
					temp = value
					cho = index
					joong = middle[temp // 28]
					jong = temp % 28
					jong = final[jong]

			if not os.path.exists('../glyphs/' + cho+joong+jong):
				os.makedirs('../glyphs/' + cho+joong+jong)

			os.chdir('../glyphs/' + cho+joong+jong)
			h = open(glif_name + '.junk', 'w')
			h.write(glif_name)
			h.close()

			c = open(cho+joong+jong + '_' + initial[cho] + '.glif', 'w')
			while True:
				line = f.readline()
				if '<outline>' in line:
					c.write(amolang_start.replace("putnamehere", cho+joong+jong + '_' + initial[cho]))
					c.write(line)

					while '</outline>' not in line:
						line = f.readline()
						c.write('\t')
						c.write(line)
					c.write(amolang_end)

				if not line:
					break

			c.close()
			f.close()

			tree = parse(cho+joong+jong + '_' + initial[cho] + '.glif')
			glif_root = tree.getroot()
			conts = glif_root.getchildren()[1].getchildren()
			counter = 1
			for cont in conts:
				first_point = cont.find("point")
				points = cont.findall("point")


				if first_point != None:
					first_point.attrib["innerType"] = "fill"
				'''
				if points != None:
					odd = True
					even = False
					n = 0
					for point in points:
						if 'type' in point.keys():
							if odd:
	#							if point == points[-3]:
	#								pass	
	#							else:
								point.attrib["penPair"] = "z" + str(counter) + "l"
								odd = False
								even = True
								n = point
								continue
							if even:
								point.attrib["penPair"] = "z" + str(counter) + "r"
								odd = True
								even = False
								counter += 1
					if even == True:	
						del n.attrib["penPair"]
				'''
				
				ElementTree(glif_root).write(cho+joong+jong + '_' + initial[cho] + '.glif')
				
			os.chdir('../../glyphs1/')
			
	os.chdir('..')

'''		
		while True:
			c = open(cho+joong+jong + '_final_' + batchim[jong] + '.glif', 'w')
			line = f.readline()
			if '<contour>' in line:
				# c = open(cho+joong+jong + '_' + roman[parts_num] + '.glif', 'w')
				# print(cho+joong+jong)
				c.write(amolang_start.replace("putnamehere", cho+joong+jong + '_final_' + batchim[jong]))
				# print(cho+joong+jong)
				# c.write(amolang_start)
				c.write('\t')

				c.write(line)

				base_glif = base_glif.replace('place holder', '\t\t' + replacer + cho+joong+jong + '_final_' + batchim[jong] + '"/>\nplace holder')

				parts_num += 1
				while '</contour>' not in line:

					# print(line)
					line = f.readline()
					c.write('\t')
					c.write(line)
				c.write(amolang_end)
				c.close()	


				tree = parse(cho+joong+jong + '_final_' + batchim[jong] + '.glif')
				glif_root = tree.getroot()
				# con = cont.getiterator("contour")
				cont = glif_root.getchildren()[1].getchildren()[0]
				print(cont)
				first_point = cont.find("point")
				points = cont.findall("point")
				if first_point != None:
					# print(first_point.items())	
					first_point.attrib["innerType"] = "fill"
					# ElementTree(glif_root).write(cho+joong+jong + str(parts_num - 1) + 'i' + '.glif')
				# if points != None:
					# for point in points:
						# if 'type' in point.keys():
							# print(point.items())
							# x = point.get('x')
							# y = point.get('y')
							# print(x, y)

					odd = True
					even = False
					counter = 1
					for point in points:
						if 'type' in point.keys():
							if odd:
								point.attrib["penPair"] = "z" + str(counter) + "l"
								odd = False
								even = True
								continue
							if even:
								point.attrib["penPair"] = "z" + str(counter) + "r"
								odd = True
								even = False
								counter += 1
				
				ElementTree(glif_root).write(cho+joong+jong + '_final_' + batchim[jong] + '.glif')

				# first_point = cont.find("point")
				# print(first_point)
				# if cont[0] != None:
					# print(cont[0])

			if not line:
				break
		c.close()
			'''

'''
과관공금긋긒까깨꽃끗
꽹꿱넘농늚늠늣늪늰다
떻때땜땟땡땧뗀뗏뜬뜻
른를마매맘맴먐먬멈멤
몀몌몸몽묨뭄뮴므믐믓
믚뫄뫔뫠뫰뭐뭠뭬뭼믜
믬미밈뿌뺑사섬듦슴솩
솬쉰아애액앰얗응윷읗
와완왕웬웰징종차참책
챈챔쳉촐총촤췰편펫픔
하함핵홀홅홍후흉휄
'''

'''
감게공과관글금긋긒깊
까깨꽃꽹꿱끗난넘년농
늚늠늣늪늰니다대드들
듦따때땜땟땡땧떻뗀뗏
뜬뜻라람로롭른를름리
마만맘매맴먐먬멈멤몀
몌몸몽뫄뫔뫠뫰묨뭄뭐
뭠뭬뭼뮴므믐믓믚믜믬
미밈백별빛뺑뿌사새섬
소솩솬수쉡쉰슮슴아안
애액앰얗에여와완왕용
웬웰윷은응읗의이일전
절종징차참책챈챔천쳉
촐총촤췰탄팔펫편픔하
할함핵혜홀홅홍후휄흉
'''

'''
lines = f.readlines()
for line in lines:
    print(line)
f.close()
'''
'''
while True:
    line = f.readline()
    if not line: break
    print(line)
f.close()
'''




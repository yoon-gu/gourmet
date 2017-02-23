import xml.etree.ElementTree
tree = xml.etree.ElementTree.parse('vincent_legacy.kml')
root = tree.getroot()
for place in tree.findall('.//name'):
	print(place.text)
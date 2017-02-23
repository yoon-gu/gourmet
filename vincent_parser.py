import xml.etree.ElementTree
tree = xml.etree.ElementTree.parse('vincent_legacy.kml')
root = tree.getroot()
for place in tree.findall('.//Placemark'):
	name = place.find('name').text
	coord = place.find('Point/coordinates').text
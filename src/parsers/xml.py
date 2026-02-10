import xml.etree.ElementTree as ET

def parse_xml(xml_data: bytes):
	root = ET.fromstring(xml_data)
	rows = root.find('.//rows').findall('row')
	return [
		{k: v for k, v in row.items()}
		for row in rows
	]
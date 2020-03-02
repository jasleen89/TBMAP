from Bio import Entrez, SeqIO
import xml.etree.ElementTree as ET
import pandas as pd
Entrez.email = "jasleenkochar89@gmail.com" 

retstart = [0, 10000, 20000, 30000, 40000, 50000, 60000]
retmax = [10000, 10000, 10000, 10000, 10000, 10000, 10000]
data = [['----', '----', '----', '----', '----', '-----', '-----']]
df = pd.DataFrame(data, columns = ['Id', 'BioSampleID','SRA Accession No.', 'Organism', 'Location', 'Center Name', 'Project Name'])
for start, maximum in zip(retstart, retmax):
	handle = Entrez.esearch(db="BioSample", term="(Mycobacterium tuberculosis) AND biosample_sra[filter] AND public[filter]", retstart = start, retmax = maximum)
	record = Entrez.read(handle)
	record_count = record["Count"]
	record_idlist = record["IdList"]
	id_str = ",".join(record_idlist)
	#print (id_str)
	number = len(id_str.split(','))
	#print (number)

	handle = Entrez.efetch(db="BioSample", id=id_str, rettype="gb", retmode="xml")
	text = handle.read()
	with open("Biosamplenew.xml", "w") as outfile:
		outfile.write(text)

	tree = ET.parse('Biosamplenew.xml')
	root = tree.getroot()

	for i in range(len(record_idlist)):

		Id = record_idlist[i]
		try:
			info_biosample = root[i][0]
			for child_biosample in info_biosample:
				dict1 = child_biosample.attrib
				if ('BioSample') in dict1.values():
					biosample_id = child_biosample.text
					break;
				else: 
					biosample_id = "Not applicable"

		except IndexError:
			biosample_id = "Not applicable"

		try:
			info_sra = root[i][0]
			for child_sra in info_sra:
				dict2 = child_sra.attrib
				if ('SRA') in dict2.values():
					sra_accession_no = child_sra.text
					break;
				else: 
					sra_accession_no = "Not applicable"
		except IndexError:
			sra_accession_no = "Not applicable"

		try:
			organism = root[i][1][1][0].text
		except IndexError:
			organism = "Not applicable"
		
		try:
			info_geo = root[i][5]
			for child in info_geo:
				dict1 = child.attrib
				if ('geographic location' or 'Country' or 'geo_loc_name') in dict1.values():
					geo_location = child.text
					break;
				else: 
					geo_location = "Not applicable"
		except IndexError:
			geo_location = "Not applicable"

		try:
			info_center = root[i][5]
			for child_center in info_center:
				dict2 = child_center.attrib
				if ('INSDC center name') in dict2.values():
					center_name = child_center.text
					break;
				else:
					center_name = "Not applicable"
		except IndexError:
			center_name = "Not applicable"

		try:
			info_project = root[i][5]
			for child_project in info_project:
				dict3 = child_project.attrib
				if ('project_name' or 'project name') in dict3.values():
					project_name = child_project.text
					break;
				else:
					project_name = "Not applicable"
		except IndexError:
			project_name = "Not applicable"

		df2 = {'Id':Id, 'BioSampleID':biosample_id,'SRA Accession No.':sra_accession_no, 'Organism':organism, 'Location':geo_location, 'Center Name':center_name, 'Project Name': project_name}
		df = df.append(df2, ignore_index=True)

df.to_csv("biosample.csv", index= False)
print (df)


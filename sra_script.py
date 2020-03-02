from Bio import Entrez, SeqIO
import xml.etree.ElementTree as ET
import pandas as pd
Entrez.email = "jasleenkochar89@gmail.com" 

retstart = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000]
retmax = [10000, 10000, 10000, 10000, 10000, 10000, 10000, 8278]
data = [['----', '----', '----', '----', '----', '-----']]
df = pd.DataFrame(data, columns = ['Id', 'Exp Accession Number','Submit By', 'Study Accession Number', 'BioSample Id','Bioproject Number'])
for start, maximum in zip(retstart, retmax):
	handle = Entrez.esearch(db="SRA", term="Mycobacterium tuberculosis", retstart = start, retmax = maximum)
	record = Entrez.read(handle)
	record_count = record["Count"]
	record_idlist = record["IdList"]

	id_str = ",".join(record_idlist)
	#print (id_str)
	number = len(id_str.split(','))
	#print (number)
	handle = Entrez.efetch(db="SRA", id=id_str, rettype="gb", retmode="xml")
	text = handle.read()
	with open("sra.xml", "w") as outfile:
		outfile.write(text)

	tree = ET.parse('sra.xml')
	root = tree.getroot()

	for i in range(len(record_idlist)):

		Id = record_idlist[i]
		try:
			experiment = root[i][0].attrib
			exp_accession_number = experiment['accession']
		except IndexError:
			exp_accession_number = "Not applicable"

		try:
			center_name = root[i][2][0].text
		except IndexError:
			center_name ="Not applicable"

		try:
			study = root[i][3].attrib
			study_accesion_number = study['accession']
		except IndexError:
			study_accesion_number = "Not applicable"		
		
		try:
			bioproject_number = root[i][3][0][1].text
		except IndexError:
			bioproject_number = "Not applicable"

		try:
			biosample_id = root[i][4][0][1].text
		except IndexError:
			biosample_id = "Not applicable"

		df2 = {'Id':Id, 'Exp Accession Number':exp_accession_number,'Submit By':center_name, 'Study Accession Number':study_accesion_number, 'BioSample Id':biosample_id, 'Bioproject Number':bioproject_number}
		df = df.append(df2, ignore_index=True)

df.to_csv("sra.csv", index= False)
print (df)

	

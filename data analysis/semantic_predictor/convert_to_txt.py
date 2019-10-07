from document_class import *
import os

def main():
	directory = "/Volumes/NATHAN/out/films/"

	folder_list = [f for f in os.listdir(directory) if not f.startswith('.')]

	file_list = []

	for folder in folder_list:
		file_list+=([directory+folder+"/"+f for f in os.listdir(directory+folder) if not f.startswith('.')])

	for file in file_list:
		document = read_json(file)
		string = ''

		for key,value in document.added.items():
			i = 0
			while i < value:
				string += key + ' '
				i += 1

		outfile = open('/Volumes/NATHAN/out/changes_as_text/films/' + file, 'a+')
		outfile.write(string)
		outfile.close


if __name__ == '__main__':
	main()
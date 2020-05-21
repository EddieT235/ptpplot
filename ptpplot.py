import getopt
import sys
import re
import csv
import os.path

# Requires python 3 (built with 3.8.2)

version = "0.0.1"
verbose = False

def usage():
	print("PTP stats log plotter version ",version)
	print("Provide input filename FOLLOWED BY list of clock indexes on command line")
	print(" ")
	print("example: ptpplot.py -i stats.log 3 2 1")
	print("Will generate .csv files: phc3.csv phc2.csv and phc1.csv")

def make_csv(infile, clockidx):
	time = ""
	offset = ""
	clockstr = ""
	count = 0
	
	clockstr = "->phc" + clockidx
	
	# 
	# always open output .csv file:
	#
	outfile = clockstr.lstrip("->") + ".csv"
	f = open(outfile, "a")
	
	for line in open(infile):
		if clockstr in line:
			count += 1
			# 
			# timestamp occupies fixed position always:
			#
			time = line[11:19] 

			# 
			# get offset value (could be minus value):
			#
			sline = line.split()
			offset = sline[4].rstrip(",")
			
			# 
			# append time/offset to output file (clockstr.csv):
			#
			print(time, ',', offset, file=f, sep = '')
	
	#infile.close()
	f.close()
			
def main(argv):
	inputfile = r"D:\python\ptpplot\default.log"   
	
	try:
		opts, args = getopt.getopt(argv,"hi:",["infile="])
	except getopt.GetoptError:
		print("ERROR: command line")
		sys.exit(2)
		
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-i", "--infile"):
			inputfile = arg
		
	if not (os.path.isfile(inputfile)):
		print("ERROR: file does not exist: " + inputfile)
		sys.exit(2)
		
	# 
	# Pass each clock index to parser:
	#
	n = len(argv) -1
	while (n >= 2):
		make_csv(inputfile, argv[n])
		n -= 1
		
	# 
	# Generate matlib plot:
	#	
	

if __name__ == "__main__":
	main(sys.argv[1:])


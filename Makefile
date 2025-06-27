all:
	echo "Hello, World"

clean:
	rm -f blah blah.o blah.c

clean_data:
	python tasks/medicare_data/clean_data.py

# Rule for generic "major_procedure_extract_<year>.csv"
tasks/medicare_data/output/major_procedure_extract_%.csv:
	python tasks/medicare_data/major_procedure_extract.py $*

# Rule for alternative naming like "medicare_data_<year>_cleaned.csv"
tasks/medicare_data/output/medicare_data_%_cleaned.csv:
	python tasks/medicare_data/major_procedure_extract.py $*

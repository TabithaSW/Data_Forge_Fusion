# Test read/write funcs

import DataConverterMain
import Convert_Funcs
import os

# Test CSV Read
Data_Test = Convert_Funcs.read_csv_file('crime.csv')
print(Data_Test)

# Test other read/write if need be.


# Test file extension check:
def detect_file(file_path):
        # When user is prompted to choose a file, we need to ensure it is correctly identified before conversion.
        x, file_extension = os.path.splitext(file_path.lower())
        print(file_extension)
detect_file('crime.csv')


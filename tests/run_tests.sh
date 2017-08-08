echo "#Compile:";
echo "+--------------------+";
python test.py < compile_tests.txt;
echo "+--------------------+";
echo "#Interp:";
echo "+--------------------+";
python test.py < interp_tests.txt;
echo "+--------------------+";
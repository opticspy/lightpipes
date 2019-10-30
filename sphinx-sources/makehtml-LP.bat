xcopy /S /Y /I ..\Examples .\Examples
cd ..
python  setup.py build_ext --inplace
cd ./sphinx-sources
copy /b command-reference.rst+
make html

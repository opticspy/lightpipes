xcopy /S /Y /I ..\Examples .\Examples
cd ..
py -2  setup.py build_ext --inplace
cd ./sphinx-sources
copy /b command-reference.rst+
make html

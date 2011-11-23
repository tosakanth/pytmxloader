rem del /F /S /Q dist
del /F /S /Q MANIFEST
del /F /Q *.pyc
del /F /Q *.pyo

cd doc
call make.bat html

cd ..
python setup.py sdist
pause
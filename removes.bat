
del /F /Q /S  *.pyc *.zip

rmdir /Q /S logs

for /R %%s in (__pycache__) do ( 
 rd /s/q %%s
)
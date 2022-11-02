@ECHO OFF
make
for %%I in (*.cbp) do set CurrProjectName=%%~nI
for %%I in (.) do set CurrDirName=%%~nI
if not exist "%CurrProjectName%.bat" (
	echo @ECHO OFF >> %CurrProjectName%.bat
	echo 3dslink -a 192.168.1.37 %CurrDirName%.3dsx >> %CurrProjectName%.bat
)
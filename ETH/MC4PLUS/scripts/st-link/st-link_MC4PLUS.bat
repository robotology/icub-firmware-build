:start
@echo off

reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT

if %OS%==32BIT set PATH=%ProgramFiles%
if %OS%==64BIT set PATH=%ProgramFiles(x86)%

"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -ME
echo;
echo;
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -c -P "..\..\bin\environment\mc4plusLoader.hex"
echo;
echo;
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -c -P "..\..\bin\environment\mc4plusUpdater.hex"
echo;
echo;
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -c -P "..\..\bin\application\mc4plus.hex"
echo;
echo;
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -Rst -Run
echo;
echo;
IF %errorlevel% NEQ 0 GOTO :error
GOTO :end
:error
echo There was an error.
EXIT 1
:end
echo End.
EXIT 0
:start
@echo off

reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT

if %OS%==32BIT set PATH=%ProgramFiles%
if %OS%==64BIT set PATH=%ProgramFiles(x86)%

echo;
echo Select the target:
echo [1] iCub3
echo [2] R1
set choice=
set /p choice=Type the number: 
if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='1' goto :iCub3
if '%choice%'=='2' goto :R1
echo "%choice%" is not valid, try again
echo;
goto :start
:iCub3
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -ME
echo;
echo Programming BAT with target iCub3
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -c -P "..\bat_1.2.0_icub3.hex"
echo;
echo;
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -Rst -Run
echo;
echo;
if  %errorlevel% NEQ 0 goto :error
goto :end
:R1
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -ME
echo;
echo Programming BAT with target R1
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -c -P "..\bat_1.2.0_r1.hex"
echo;
echo;
"%PATH%\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe" -Rst -Run
echo;
echo;
if %errorlevel% NEQ 0 goto :error
goto :end
:error
echo There was an error.
EXIT 1
:end
echo End.
EXIT 0
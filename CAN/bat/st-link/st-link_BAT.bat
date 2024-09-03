:start
@echo off

set PATH=%ProgramFiles%

echo;
echo Select the target:
echo [1] iCub-ergoCub
echo [2] R1
set choice=
set /p choice=Type the number: 
if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='1' goto :iCub-ergoCub
if '%choice%'=='2' goto :R1
echo "%choice%" is not valid, try again
echo;
goto :start
:iCub-ergoCub
echo Connecting BAT to the STLink-v3
"%PATH%\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe" -c port=SWD freq=8000 ap=0 reset=SWrst
echo;
echo;
echo Programming BAT with target iCub-ergoCub
"%PATH%\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe" -c port=SWD -d "..\bat.hex" 0x08000000 --verify
echo;
echo;
"%PATH%\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe" -c port=SWD -Rst -Run
echo;
echo;
if  %errorlevel% NEQ 0 goto :error
goto :end
:R1
"%PATH%\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe" -c port=SWD freq=8000 ap=0 reset=SWrst
echo;
echo Programming BAT with target R1
"%PATH%\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe" -c port=SWD -d "..\bat.r1.hex" 0x08000000 --verify
echo;
echo;
"%PATH%\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe" -c port=SWD -Rst -Run
echo;
echo;
if %errorlevel% NEQ 0 goto :error
goto :end
:error
echo There was an error.
PAUSE
EXIT 1
:end
echo End.
PAUSE
EXIT 0

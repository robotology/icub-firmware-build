
@ECHO OFF
 
IF "%1"=="" ( 
    SET "Programmer=UL2" 
    
    GOTO TAGstart
    
    ) ELSE ( 
        IF "%1"=="-programmer" (  
            SET "Programmer=%2" 
        ) ELSE IF "%1"=="-help" ( 
            GOTO TAGhelp 
        ) ELSE ( 
            GOTO TAGsyntaxerror 
        )

        GOTO TAGstart
) 



:TAGsyntaxerror
ECHO SYNTAX ERROR use "command -help" for command syntax 
GOTO TAGend


:TAGhelp
ECHO USAGE
ECHO command -help                  : prints this help
ECHO command -programmer [ULPRO, UL2]   : uses UlinkPro (default) or Ulink2
ECHO command                        : the same as -programmer ULPRO
GOTO TAGend


:TAGruntimeerror
ECHO RUNTIME ERROR
GOTO TAGend

:TAGunrecognisedprogrammer
ECHO ERROR: unrecognised programmer
GOTO TAGend


REM begin-work

:TAGstart

ECHO Programming flash-eeprom-eraser with %Programmer% (use command line option "-help" to see how to change programmer)

IF %Programmer%==ULPRO (  
            SET "target=ems4ulproeraseburn" 
            ECHO Programming with %Programmer%
            ECHO use option -programmer 
        ) ELSE IF %Programmer%==UL2 ( 
            SET "target=ems4ul2eraseburn" 
        ) ELSE ( 
            GOTO TAGunrecognisedprogrammer 
        )

rem section for eraser
mkdir reports
copy ..\bin\environment\emsEEPROMerase.hex reports
copy reports\emsEEPROMerase.hex tools\target.hex 
C:\Keil_v5\UV4\UV4 -f tools\burn_target.uvprojx -o ..\reports\emsEEPROMerase_burn_report.txt -t %target%
del /F tools\*.bak
del /F tools\*.dep
del /F tools\*.plg
del /F tools\*.uvgui*
del /F tools\*.htm
del /F tools\target.hex


GOTO TAGend

REM end-of-work

:TAGend
ECHO The script is over: BYE BYE


mkdir reports
copy ..\bin\environment\mc4plusEEPROMerase.hex reports
copy reports\mc4plusEEPROMerase.hex tools\target.hex 
C:\Keil_v5\UV4\UV4 -f tools\burn_target.uvprojx -o ..\reports\mc4plusEEPROMerase_burn_report.txt -t ems4ulproeraseburn
del /F tools\*.bak
del /F tools\*.dep
del /F tools\*.plg
del /F tools\*.uvgui*
del /F tools\*.htm
del /F tools\target.hex

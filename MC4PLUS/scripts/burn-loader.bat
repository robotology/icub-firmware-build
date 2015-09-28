mkdir reports
copy ..\bin\environment\mc4plusLoader.hex reports
copy reports\mc4plusLoader.hex tools\target.hex 
C:\Keil_v5\UV4\UV4 -f tools\burn_target.uvprojx -o ..\reports\mc4plusLoader_burn_report.txt -t ems4ulproburn
del /F tools\*.bak
del /F tools\*.dep
del /F tools\*.plg
del /F tools\*.uvgui*
del /F tools\*.htm
del /F tools\target.hex

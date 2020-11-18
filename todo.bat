@echo off
set arguments=
:copie
if "%~1"=="" goto fin
set arguments=%arguments% %~1
shift
goto copie
:fin
py C:\Users\marti\source\repos\Todo_List\Todo_List\Todo_List.py%arguments%
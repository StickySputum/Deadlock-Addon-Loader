@echo off
setlocal enabledelayedexpansion
set "output=project_structure.txt"

REM Удаляем существующий файл, если он есть
if exist %output% del %output%

REM Начинаем запись структуры с корневой папки (текущая директория)
echo %~nx0 > %output%
call :display_structure "." 0 >> %output%

echo Структура проекта записана в %output%
exit /b

REM Функция для отображения структуры каталога
:display_structure
setlocal
set "folder=%~1"
set /a indent=%~2

for /f "delims=" %%f in ('dir "%folder%" /b /a-d 2^>nul') do (
    call :print_line "├── " "%%f" %indent%
)

for /f "delims=" %%d in ('dir "%folder%" /b /ad 2^>nul') do (
    call :print_line "├── " "%%d" %indent%
    call :display_structure "%folder%\%%d" %indent%+1
)

endlocal
exit /b

REM Функция для отображения строки с отступом
:print_line
setlocal enabledelayedexpansion
set "line="
for /L %%i in (1,1,%~3) do set "line=!line!│   "
echo !line!%~1%~2
endlocal
exit /b

@echo off
setlocal EnableDelayedExpansion
set a=0

for %%n in (*.gif) do (
ren "%%n" "!a!.gif"
set /A a+=1
)
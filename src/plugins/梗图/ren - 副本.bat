@echo off
setlocal EnableDelayedExpansion
set a=0

for %%n in (*.png) do (
ren "%%n" "!a!.png"
set /A a+=1
)
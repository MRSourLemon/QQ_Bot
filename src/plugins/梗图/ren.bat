@echo off
setlocal EnableDelayedExpansion
set a=0

for %%n in (*.jpg) do (
ren "%%n" "!a!.jpg"
set /A a+=1
)
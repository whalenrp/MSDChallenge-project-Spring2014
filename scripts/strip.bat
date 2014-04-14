:: Jenna Careccia, script for scrubbing h5 files for metadata

:: pulled from http://stackoverflow.com/
::				questions/8397674/windows-batch-file-
::				looping-through-directories-to-process-files
:: reference: http://www.hdfgroup.org/HDF5/doc/RM/Tools.html#Tools-Copy
@echo off
call :treeProcess
goto :eof

startingDir="C:\Users\Aluminum\Documents\Academics\2014Spring\CS 292\Final Project\Subset\MillionSongSubset\data\A\A\"

:treeProcess
for %%f in (*.h5) do h5copy -i %%f -o C:\Users\Aluminum\Desktop\B\%%f -s metadata -d metadata
for /D %%d in (*) do (
	cd %%d
	call :treeProcess
	cd ..
)
exit /b
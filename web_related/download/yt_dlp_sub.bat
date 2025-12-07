@echo off
REM ============================================
REM yt-dlp Subtitle Downloader (TXT version)
REM Usage: yt_subs_txt.bat VIDEO_URL
REM Example: yt_subs_txt.bat https://youtu.be/VIDEO_ID
REM ============================================

set URL=%1

if "%URL%"=="" (
    echo Usage: yt_subs_txt.bat VIDEO_URL
    exit /b 1
)

echo Downloading subtitles (TXT) for %URL% ...

REM 1. Uploaded subtitles in TXT
yt-dlp --skip-download --write-subs --sub-lang en --convert-subs txt %URL%

REM 2. Auto-generated captions in TXT
yt-dlp --skip-download --write-auto-subs --sub-lang en --convert-subs txt %URL%

echo Subtitle downloads complete!
pause
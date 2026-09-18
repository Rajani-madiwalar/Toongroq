@echo off
title ToonGroq AI Studio - Cartoon Mascot, Blazer Decorator & Java Tutor
echo =====================================================================
echo           Starting ToonGroq AI Chatbot Studio...
echo =====================================================================
echo.

if exist "C:\Users\ise\anaconda3\python.exe" (
    echo Using Anaconda Python...
    "C:\Users\ise\anaconda3\python.exe" app.py
) else (
    echo Using System Python...
    python app.py
)

pause

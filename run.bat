@echo off
REM ============================================================
REM  BackMirror 실행 (Windows)
REM  반드시 파이썬 3.13 으로 띄웁니다 — ultralytics / torch 가
REM  설치된 환경이라 real YOLO26n 검출이 동작합니다.
REM
REM  파이썬 3.14 등 ultralytics 가 없는 환경으로 app.py 를 직접
REM  실행하면 검출이 mock 으로 떨어집니다(콘솔에
REM  "[detector] ultralytics not installed" 경고가 뜸).
REM  py 런처가 3.13 을 골라 그 문제를 막아줍니다.
REM ============================================================
cd /d "%~dp0"
py -3.13 app.py

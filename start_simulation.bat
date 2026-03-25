@echo off
title Market Simulation Lab
echo.
echo ============================================================
echo  Market Simulation Lab - Phase 6 and 7 Simulation Backend
echo ============================================================
echo.
echo Starting simulation backend on http://localhost:5501
echo Opening index.html in browser...
echo.

:: Open the main UI
start "" "index.html"

:: Start the simulation server
python simulation_server.py

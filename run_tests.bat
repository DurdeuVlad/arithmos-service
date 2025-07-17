@echo off
REM run_tests.bat - Script pentru pornirea containerelor și testarea endpoint-urilor API Arithmos în CMD

REM 1. Pornire containere necesare
echo.
echo === Pornire containere necesare ===
for %%c in (oracle-db sqlserver arithmos_api arithmos_rabbitmq arithmos_redis) do (
    echo Pornesc containerul %%c...
    docker start %%c >nul 2>&1 && echo   %%c este pornit || echo   Nu am putut porni %%c
)

REM Așteaptă 5 secunde pentru startup
echo.
timeout /t 5 /nobreak >nul

REM 2. Health-check
echo.
echo === Health-check ===
curl -s -w "Health status: %{http_code}\n" http://localhost:8000/health

REM 3. Testare endpoint-uri matematice
echo.
echo === Testare endpoint-uri matematice ===

echo POST http://localhost:8000/api/pow
curl -s -X POST http://localhost:8000/api/pow -H "Content-Type: application/json" -d "{\"base\":2,\"exp\":8}" && echo.

echo GET http://localhost:8000/api/fib/10
curl -s http://localhost:8000/api/fib/10 && echo.

echo GET http://localhost:8000/api/fact/5
curl -s http://localhost:8000/api/fact/5 && echo.

echo.
echo === Sfârșit testare ===
pause

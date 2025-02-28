@echo off
REM Number of patients per state
set POPULATION=2000

for %%S in (
  "California" "Texas" "New York" "Florida" "Illinois" "Pennsylvania" "Ohio" "Georgia"
) do (
    echo Generating data for %%~S...
    java -jar synthea-with-dependencies.jar ^
        -p %POPULATION% ^
        --exporter.fhir.export=false ^
        --exporter.csv.export=true ^
        --exporter.csv.folder_per_run=true ^
        %%~S
)


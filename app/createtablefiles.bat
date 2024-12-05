echo off
powershell -Command "(Get-Content ./app/templatefiles/schema.py) -replace 'ReplaceTitle', '%1' | Out-File -encoding UTF8 ./app/schemas/sch_%3.py"
powershell -Command "(Get-Content ./app/templatefiles/model.py) | Foreach-Object { $_.replace('ReplaceTitle', '%1') } | Out-File -encoding UTF8 ./app/models/mdl_%3.py"
powershell -Command "(Get-Content ./app/templatefiles/crud.py) | Foreach-Object { $_.replace('ReplaceTitle', '%1').replace('ReplaceLowercase', '%2').replace('ReplaceFileName', '%3') } | Out-File -encoding UTF8 ./app/crud/rep_%3.py"
powershell -Command "(Get-Content ./app/templatefiles/api.py) | Foreach-Object { $_.replace('ReplaceTitle', '%1').replace('ReplaceLowercase', '%2').replace('ReplaceFileName', '%3') } | Out-File -encoding UTF8 ./app/api/api_v1/endpoints/api_%3.py"

# Script para probar la API de Ensamble
$baseUrl = if ($env:API_BASE_URL) { $env:API_BASE_URL } else { "http://localhost:8000" }

Write-Host "=== Pruebas de API Ensamble ===" -ForegroundColor Magenta
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: GET /health - Verificar estado de la API" -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get
    Write-Host "Respuesta exitosa:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 2: Model Info
Write-Host "Test 2: GET /info - Obtener informacion del modelo" -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/info" -Method Get
    Write-Host "Respuesta exitosa:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 3: Prediccion - Setosa
Write-Host "Test 3: POST /predict - Prediccion Setosa" -ForegroundColor Cyan
$bodySetosa = @{
    features = @(5.1, 3.5, 1.4, 0.2)
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/predict" -Method Post -Body $bodySetosa -ContentType "application/json"
    Write-Host "Prediccion exitosa:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 4: Prediccion - Versicolor
Write-Host "Test 4: POST /predict - Prediccion Versicolor" -ForegroundColor Cyan
$bodyVersicolor = @{
    features = @(6.4, 3.2, 4.5, 1.5)
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/predict" -Method Post -Body $bodyVersicolor -ContentType "application/json"
    Write-Host "Prediccion exitosa:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 5: Prediccion - Virginica
Write-Host "Test 5: POST /predict - Prediccion Virginica" -ForegroundColor Cyan
$bodyVirginica = @{
    features = @(7.2, 3.6, 6.1, 2.5)
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/predict" -Method Post -Body $bodyVirginica -ContentType "application/json"
    Write-Host "Prediccion exitosa:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 6: Prediccion con datos invalidos (menos de 4 features)
Write-Host "Test 6: POST /predict - Datos invalidos (menos features)" -ForegroundColor Cyan
$bodyInvalid1 = @{
    features = @(5.1, 3.5, 1.4)
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/predict" -Method Post -Body $bodyInvalid1 -ContentType "application/json"
    Write-Host "Prediccion exitosa:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error esperado (validacion):" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}

Write-Host "`n---`n"

# Test 7: Prediccion con valores negativos
Write-Host "Test 7: POST /predict - Valores negativos" -ForegroundColor Cyan
$bodyInvalid2 = @{
    features = @(-1.0, 3.5, 1.4, 0.2)
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/predict" -Method Post -Body $bodyInvalid2 -ContentType "application/json"
    Write-Host "Prediccion exitosa:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error esperado (validacion):" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}

Write-Host "`n---`n"

# Test 8: Ruta no encontrada
Write-Host "Test 8: GET /ruta-inexistente - Probar catch-all" -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/ruta-inexistente" -Method Get
    Write-Host "Respuesta:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error esperado (404):" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}

Write-Host "`n=== Pruebas completadas ===" -ForegroundColor Magenta
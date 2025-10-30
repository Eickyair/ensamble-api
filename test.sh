#!/bin/bash

# Script para probar la API de Ensamble
BASE_URL="${API_BASE_URL:-http://localhost:8000}"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${MAGENTA}=== Pruebas de API Ensamble ===${NC}"
echo ""

# Test 1: Health Check
echo -e "${CYAN}Test 1: GET /health - Verificar estado de la API${NC}"
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/health")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}Respuesta exitosa:${NC}"
    echo "$body" | jq .
else
    echo -e "${RED}Error: HTTP $http_code${NC}"
    echo "$body"
fi

echo -e "\n---\n"

# Test 2: Model Info
echo -e "${CYAN}Test 2: GET /info - Obtener informacion del modelo${NC}"
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/info")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}Respuesta exitosa:${NC}"
    echo "$body" | jq .
else
    echo -e "${RED}Error: HTTP $http_code${NC}"
    echo "$body"
fi

echo -e "\n---\n"

# Test 3: Prediccion - Setosa
echo -e "${CYAN}Test 3: POST /predict - Prediccion Setosa${NC}"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [5.1, 3.5, 1.4, 0.2]}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}Prediccion exitosa:${NC}"
    echo "$body" | jq .
else
    echo -e "${RED}Error: HTTP $http_code${NC}"
    echo "$body"
fi

echo -e "\n---\n"

# Test 4: Prediccion - Versicolor
echo -e "${CYAN}Test 4: POST /predict - Prediccion Versicolor${NC}"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [6.4, 3.2, 4.5, 1.5]}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}Prediccion exitosa:${NC}"
    echo "$body" | jq .
else
    echo -e "${RED}Error: HTTP $http_code${NC}"
    echo "$body"
fi

echo -e "\n---\n"

# Test 5: Prediccion - Virginica
echo -e "${CYAN}Test 5: POST /predict - Prediccion Virginica${NC}"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [7.2, 3.6, 6.1, 2.5]}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}Prediccion exitosa:${NC}"
    echo "$body" | jq .
else
    echo -e "${RED}Error: HTTP $http_code${NC}"
    echo "$body"
fi

echo -e "\n---\n"

# Test 6: Prediccion con datos invalidos (menos de 4 features)
echo -e "${CYAN}Test 6: POST /predict - Datos invalidos (menos features)${NC}"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [5.1, 3.5, 1.4]}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 422 ]; then
    echo -e "${YELLOW}Error esperado (validacion):${NC}"
    echo "$body" | jq .
else
    echo -e "${RED}Error inesperado: HTTP $http_code${NC}"
    echo "$body"
fi

echo -e "\n---\n"

# Test 7: Prediccion con valores negativos
echo -e "${CYAN}Test 7: POST /predict - Valores negativos${NC}"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [-1.0, 3.5, 1.4, 0.2]}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 422 ]; then
    echo -e "${YELLOW}Error esperado (validacion):${NC}"
    echo "$body" | jq .
else
    echo -e "${RED}Error inesperado: HTTP $http_code${NC}"
    echo "$body"
fi

echo -e "\n---\n"

# Test 8: Ruta no encontrada
echo -e "${CYAN}Test 8: GET /ruta-inexistente - Probar catch-all${NC}"
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/ruta-inexistente")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 404 ]; then
    echo -e "${YELLOW}Error esperado (404):${NC}"
    echo "$body" | jq .
else
    echo -e "${RED}Error inesperado: HTTP $http_code${NC}"
    echo "$body"
fi

echo -e "\n${MAGENTA}=== Pruebas completadas ===${NC}"
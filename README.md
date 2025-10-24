# FoodBot AI

**Progresywna aplikacja webowa (PWA)** do planowania posiłków, liczenia makroskładników i zarządzania przepisami.  
Cel: otwarta, rozszerzalna i bezkosztowa w utrzymaniu aplikacja działająca na telefonie i w przeglądarce.

# 1) klon repo i wejście do katalogu infra
git clone <URL_DO_REPO>
cd foodbot-ai/infra

# 2) budowa i uruchomienie
docker compose build
docker compose up -d

# 3) sprawdzenie
docker compose ps
# Web UI:    http://localhost:8080
# Health UI: http://localhost:8080/healthz
# API (via gateway): GET http://localhost:8080/api/v1/ingredients

# 4) zatrzymanie środowiska (opcjonalnie)
docker compose down

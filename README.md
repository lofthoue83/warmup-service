# Supabase Cache Warmup Service

Automatischer Cron-Service für Railway, der alle 30 Minuten den User-Cache aufwärmt.

## Deployment auf Railway

1. **Neues Railway Projekt erstellen:**
   ```bash
   cd warmup-service
   railway login
   railway init
   ```

2. **Environment Variables setzen:**
   ```bash
   railway variables set SUPABASE_URL=https://dein-projekt.supabase.co
   railway variables set SUPABASE_ANON_KEY=dein-anon-key
   railway variables set USER_COUNT=10
   ```

3. **Deployen:**
   ```bash
   railway up
   ```

## Funktionsweise

- Läuft als Docker Container mit Cron
- Ruft alle 30 Minuten die Edge Function auf
- Hält 10 User im Cache warm
- Logs sind in Railway Dashboard sichtbar

## Lokaler Test

```bash
# Environment variables setzen
cp .env.example .env
# .env mit deinen Werten editieren

# Script testen
python warmup.py
```

## Monitoring

Railway zeigt automatisch:
- Container Logs
- CPU/Memory Usage
- Deployment Status

## Anpassungen

- **Intervall ändern:** `crontab` Datei editieren
- **User-Anzahl:** `USER_COUNT` Environment Variable
- **Timeout:** In `warmup.py` anpassen
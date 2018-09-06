# DX Automator React Client

**Run these commands from the root directory and not from /client-react**

### Export localhost for development

```bash
export REACT_APP_TASKS_SERVICE_URL=http://localhost
```

### Get Docker running

```bash
docker-compose -f docker-compose-prod.yml up -d --build
```

### Create and populate DB

```bash
docker-compose -f docker-compose-dev.yml run tasks python manage.py recreate_db
docker-compose -f docker-compose-dev.yml run tasks python manage.py seed_db
```

If bash doesn't recognize the **REACT_APP_TASKS_SERVICE_URL** environment variable just export it and run the last two commands again.

### Open up a browser

You should find the React client at http://localhost:3000/
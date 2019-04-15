# DX Automator React Client

**Run these commands from the root directory and not from the /client-react**

### Export localhost for development

```bash
export REACT_APP_TASKS_SERVICE_URL=http://localhost
```

### Get Docker running

```bash
docker-compose -f docker-compose-prod.yml up -d --build
```
OR
```bash
./scripts/run-local-react-client
```

### Create and populate DB

```bash
docker-compose -f docker-compose-dev.yml run tasks python manage.py recreate_db
docker-compose -f docker-compose-dev.yml run tasks python manage.py seed_db
```
OR
```bash
./scripts/setup-local-db
```

If bash doesn't recognize the **REACT_APP_TASKS_SERVICE_URL** environment variable, just export it and run the last two commands again.

### Open up a browser

You should find the React client at http://localhost:3000/


### To stop the running Docker container
```bash
docker-compose -f docker-compose-dev.yml down
```
OR
```bash
./scripts/stop-local-react-client
```

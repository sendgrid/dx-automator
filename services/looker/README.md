**Goal**  
-
API to read/write data to and from Looker.


**Structure**  
-

SendsByLibrary / InvoicingByLibrary
- inherits schema from DXLooker, with appropriate table name

LookerAPIHandler  
- handles authentication of Looker API
- uses credentials to pull latest look data from Looker 

DBCache
- queries database to store all rows locally for faster access

Look
- Stores Looker look id and LookerApiHandler instance

JsonCleaner
- cleans JSON objects to fit DB model schema

DXLookerService
- container to hold objects necessary for DX Looker API

**To Run**  
- 
**Create services/looker/.env file with Looker API credentials**
```
LOOKER_CLIENT_ID=client_id_goes_here
LOOKER_CLIENT_SECRET=client_secret_goes_here
LOOKER_ENDPOINT=looker_endpoint_goes_here (e.g. https://yourdomain.looker.com:port)
```
Then export the variables:

```
$ cd services/looker/
$ export $(grep -v '^#' .env | xargs)
```

**Build and Run Docker Containers** 
```
docker-compose -f docker-compose-dev.yml up -d --build
```

**Rebuild DB table for a given look id**
```
docker-compose -f docker-compose-dev.yml run looker python main.py recreate-db -l <look_id>
```

**Populate DB table with data from a given look_id**  
```
docker-compose -f docker-compose-dev.yml run looker python main.py pull-looks -l <look_id>
```

**See look data**  
```
docker-compose -f docker-compose-dev.yml run looker
```
The data will be available at `http://localhost:5001/dx_looker/<look_id>`

**To Do**
-
- make table names configurable
- build API routes (basic calls in place, but not configurable, 
see project/api/routes.py)

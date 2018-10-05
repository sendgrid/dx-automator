**Goal**  
-
API to read/write the data to and from Looker.


**Structure**  
-

SendsByLibrary / InvoicingByLibrary
- Inherits the schema from DXLooker, with appropriate table name

LookerAPIHandler  
- Handles the authentication of theLooker API
- Uses the credentials to pull the latest look data fromthe  Looker 

DBCache
- Queries database to store all the rows locally for faster access

Look
- Stores Looker look the id and LookerApiHandler instance

JsonCleaner
- Cleans JSON objects to fit the DB model schema

DXLookerService
- Container to hold the objects necessary for DX Looker API

**To Run**  
- 
**Create ~/services/looker/.env file with Looker API credentials**
```
LOOKER_CLIENT_ID=client_id_goes_here
LOOKER_CLIENT_SECRET=client_secret_goes_here
LOOKER_ENDPOINT=looker_endpoint_goes_here (e.g. https://yourdomain.looker.com:port)
```

**Build and Run Docker Containers** 
```
docker-compose -f docker-compose-dev.yml up -d --build
```

**Rebuild DB table for a given look id**
```
docker-compose -f docker-compose-dev.yml run looker python main.py recreate_db -l <look_id>
```

**Populate DB table with data from a given look_id**  
```
docker-compose -f docker-compose-dev.yml run looker python main.py pull_looks -l <look_id>
```

**See look data**  
```
docker-compose -f docker-compose-dev.yml run looker
```
The data will be available at `http://localhost:5001/dx_looker/<look_id>`

**To Do**
-
- Make table names configurable
- Build the API routes (Basic calls in place but not configurable and see project/api/routes.py)

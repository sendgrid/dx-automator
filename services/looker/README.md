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

**To Do**
- make table names configurable
- build API routes (basic calls in place, but not configurable, 
see project/api/routes.py)

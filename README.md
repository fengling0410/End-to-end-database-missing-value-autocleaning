# Frontend

pre-install： yarn install, pip install aiofiles, pip install -U scikit-learn scipy matplotlib 
front end start ： yarn start

# FastAPI 
backend start: uvicorn backend.main:app --reload 

# Example Inputs

## Example 1 
Test categorical prediction: 
- Table to impute: rail_ridership
- Column to impute: time_period_id
- Input query: NA
- Foreign keys: line_id:lines,line_id; station_id:stations,station_id; time_period_id:time_periods,time_period_id
- Database to impute: test-DB1

## Example 2 
Test subset imputation: 
- Table to impute: rail_ridership
- Column to impute: time_period_id
- Input query: SELECT * FROM rail_ridership r WHERE r.line_id = "blue"
- Foreign keys: line_id:lines,line_id; station_id:stations,station_id; time_period_id:time_periods,time_period_id
- Database to impute: test-DB1

## Example 3
Test numerical prediction: 
- Table to impute: rail_ridership
- Column to impute: average_flow
- Input query: NA
- Foreign keys: line_id:lines,line_id; station_id:stations,station_id; time_period_id:time_periods,time_period_id
- Database to impute: test-DB3

## Example 3
Test numerical prediction with multiple query conditions: 
- Table to impute: rail_ridership
- Column to impute: average_flow
- Input query: SELECT * FROM rail_ridership r WHERE r.line_id = "blue" and r.time_period_id = "time_period_02"
- Foreign keys: line_id:lines,line_id; station_id:stations,station_id; time_period_id:time_periods,time_period_id
- Database to impute: test-DB3

#  Exception Handling 

## Example 1
Test unique value exception error: 
- Table to impute: lines
- Column to impute: line_name
- Input query: NA
- Foreign keys: NA
- Database to impute: test-DB3


## Example 2
Test invalid format error(e.g. wrong foreign keys): 
- Table to impute: rail_ridership
- Column to impute: average_flow
- Input query: SELECT * FROM rail_ridership r WHERE r.line_id = "blue" and r.time_period_id = "time_period_02"
- Foreign keys: line_id; lines,line_id; station_id:stations,station_id; time_period_id:time_periods,time_period_id
- Database to impute: test-DB3



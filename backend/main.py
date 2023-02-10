from fileinput import filename
from operator import index
from time import process_time
from tracemalloc import start
from urllib import response
from fastapi import FastAPI, UploadFile, File, Form, status, HTTPException
from fastapi.responses import FileResponse
import time
from fastapi.middleware.cors import CORSMiddleware

from tempfile import TemporaryDirectory
import os

from pandas import DataFrame
from py import process
from backend import imputation
from numpy import outer
import aiofiles
from typing import List
from pydantic import BaseModel
import pandas as pd
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse


class EndException(Exception):
    def __init__(self, status_code: status, msg: str):
        self.msg = msg
        self.status_code = status_code


app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.table_to_impute = "rail_ridership"
app.column_to_impute =  "average_flow" # "average_flow" 
app.input_query = "SELECT * FROM rail_ridership r WHERE r.line_id = \"blue\""
# app.input_query = "SELECT * FROM rail_ridership"
app.foreign_keys = "line_id:lines,line_id;station_id:stations, station_id;  time_period_id:time_periods, time_period_id"

@app.exception_handler(EndException)
async def exception_handler(request: Request, exc: EndException):
    return JSONResponse(status_code=exc.status_code, 
        content={"message": exc.msg})


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sendqueries")
async def getQueryStr(table:str = Form(), column:str = Form(), foreignKey = Form(), query = Form()):
    if foreignKey == "NA":
        foreignKey = ""
    if query == "NA":
        query = ""
        
    print(f"Input table to impute: {table}")
    print(f"Input column to impute: {column}")
    print(f"Input foreign keys: {foreignKey}")
    print(f"Input query: {query}")

    app.table_to_impute = table
    app.column_to_impute = column
    app.foreign_keys = foreignKey
    app.input_query = query
 

@app.post("/upload")
async def impute(newFile: UploadFile = File()):

    print(f"User uploaded database: {newFile.filename}")
    print(f"table to impute: {app.table_to_impute}")
    print(f"column to impute: {app.column_to_impute}")
    print(f"foreign keys: {app.foreign_keys}")
    print(f"query: {app.input_query}")

    with TemporaryDirectory() as sql_dir:
        sql_path = os.path.join(sql_dir, newFile.filename)
        async with aiofiles.open(sql_path, 'wb') as out_file:
            content = await newFile.read()  # async read
            await out_file.write(content)  # async write

            try:
                start_time = time.time()
               # print("********", imputation.impute_missing_values(sql_path, app.table_to_impute, app.column_to_impute, app.input_query, app.foreign_keys))
                processed_data, eval_metric = imputation.impute_missing_values(sql_path, app.table_to_impute, app.column_to_impute, app.input_query, app.foreign_keys)
                end_time = time.time()    
                print("Time for imputation: %.4f s" % (end_time - start_time))
                fname = "%s.csv" % (eval_metric)
                file_path = os.path.join("persistant_folder", fname)

                # append the metric to the end of csv 
                type, val = eval_metric.split('_')
                processed_data = processed_data.append(pd.Series(eval_metric, dtype=str, name=type))
                processed_data.to_csv(file_path, index=False)
                print("successful!")
                return FileResponse(file_path, filename = fname)       
            except:
                # other unknown error
                traceback.print_exc()
                if eval_metric == "unique value error":
                    raise EndException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
                            msg ="Cannot impute when unique value percentage is larger than 0.5")
                elif eval_metric == "invalid input":
                    raise EndException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
                            msg ="Cannot impute when input(Table/Column/Foreign Key/Query) is invalid")
                raise EndException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
                            msg ="Unknown error")
                




import React, { useEffect, useRef, useState } from 'react';
import MyImage from '../Images/missing.png';

function Home(){
    // Create your own Mock API: https://mockapi.io/
    // const url = `https://5e9623dc5b19f10016b5e31f.mockapi.io/api/v1/products?page=1&limit=10`
    // let products = useAxiosGet(url)

    // Component States
    const [file, setFile] = useState(null)
    const [table, setTable] = useState(null)
    const [column, setColumn] = useState(null)

    function getFile(event) {
        setFile(event.target.files[0])
        console.warn(event.target.files[0])
      }
    
      function getTable(event){
        setTable(event.target.value)
        console.warn(event.target.value)
      }

      function getColumn(event){
        setColumn(event.target.value)
        console.warn(event.target.value)
      }

      function getSubmit(){
        // here do database file processing

      }

    
    let content = 
        <div className="mb-2 p-3 content-center">
            This is our project for missing value imputation, upload a database to get started!
            <p>
                <h1> Input table name: </h1>
            <input type="text" name="tablename" onChange={getTable}/>
            </p>

            <p>
                <h1> Input column name:</h1>
                <input type="text" name="column" onChange={getColumn} />
            </p>

            <p className='content-center'>
                <input type="file" onChange={getFile} />
                <button type="submit" onClick={getSubmit}>Upload</button>
            </p>

            <p className='content-center bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded'>
                <button type="submit" onClick={getSubmit}>Impute Missing Value</button>                
            </p>
        {/* <img src={MyImage} alt="horse" /> */}
        </div>


    return (
        <div className="container mx-auto">
            <h1 className="font-bold text-2xl mb-3 text-center">
                Database Missing Value Imputation
            </h1>
            <div className="md:flex flex-wrap md:-mx-3">
                { content } 
            </div>
        </div>
    )
}

export default Home
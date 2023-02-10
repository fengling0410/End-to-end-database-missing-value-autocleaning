import React from 'react'

function Documentation(){
    return (
        <div>
            <h1 className="font-bold text-2xl mb-3">Documentation</h1>
            <p>
                Here is a short demo of how to make use of web application:
            </p>
            <ul>
                <li>Step 1: The user should input the name of the table they want to impute missing value for, 
                    the name of the column that contains the missing value,
                    the foreign key pair of the targeting column (help to do table merging),
                    and also the query they want to perform on the database to the corresponding textbox.
                    After input all the required fields, user should click the "submit" button.</li>
                <li>Step 2: After submiting string inputs as stated above, the user should upload a "sqlite" file through the file uploading section.
                    After clicking the "Upload" button, the user's local file directory will pop-up and user should choose the corresponding sqlite file
                    they want to do imputation on. 
                </li>
                <li>Step 3: After the file have been uploaded, the sqlite file will be processed and that could take up to 60 seconds
                    depending on the hardware. We appreciate your patience.
                </li>
                <li>Step 4: The processed imputed table will be automatically downloaded through the web browser as a csv file if it is successfully imputed. The imputation accuracy
                    can be read from the file. Otherwise, an error message will pop-up to inform the user about the type of the error ecountered.
                </li>
            </ul>

            <p>
                Hope this documentation has clarified any confusion about using our web appication. Please let us know if you have any suggestions on the any part of the current workflow. Enjoy!!
            </p>
        </div>
    )
}

export default Documentation
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import "./FileUpload.scss";
import axios from "axios";

const downloadFile = (response) => {
  const url = window.URL.createObjectURL(new Blob([response.data])) 
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', "Imputed_Table.csv")
  document.body.appendChild(link)
  link.click()
}

const FileUpload = ({ file, setFile, setLoad }) => {
  const uploadHandler = (event) => {
    file = event.target.files[0];
    if (!file) return;
    setFile(file);
    // upload file
    const formData = new FormData();
    formData.append("newFile", file, file.name);

    const config = {
      headers: { "content-type": "multipart/form-data" },
    };

    axios
      .post("http://localhost:8000/upload", formData, config)
      .then((response) => {
        setLoad(false);
        console.log(response)
        downloadFile(response)
      })
      .catch((error) => {
        // inform the user
        setLoad(false);
        console.log(error.response)
        alert(error.response.data['message']);
      });
  };

  return (
    <>
      <div className="file-card">
        <div className="file-inputs">
          <input type="file" onChange={uploadHandler} />
          <button>
            <i>
              <FontAwesomeIcon icon={faPlus} />
            </i>
            Upload
          </button>
        </div>
        <p className="main">Supported type</p>
        <p className="info">SQL</p>
      </div>
    </>
  );
};

export default FileUpload;

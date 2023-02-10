import React, { useState } from "react";
import "./App.scss";
import FileUpload from "./FileUpload/FileUpload";
import FileItem from "./FileItem/FileItem";
import TextBoxs from "./TextBoxs/TextBoxs";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";
import About from "./Views/About";
import Documentation from "./Views/Documentation";

function App() {
  const [file, setFile] = useState(null);
  const [load, setLoad] = useState(true);
  const [queryStr, setQueryStr] = useState({});

  const removeFile = () => {
    setFile(null);
  };

  const handleChange = (data) => {
    setQueryStr(data);
  };

  return (
    <div className="relative pb-10 min-h-screen">
      <Router>
        <Header />
        <div className="p-3">
          <Switch>
            <Route exact path="/">
              <div className="font-bold">User Inputs</div>
              <TextBoxs onChange={handleChange} queryStr={queryStr} />
              <FileUpload
                file={file}
                setFile={setFile}
                removeFile={removeFile}
                setLoad={setLoad}
                queryStr={queryStr}
              />
              {file && (
                <FileItem file={file} load={load} removeFile={removeFile} />
              )}
            </Route>
            <Route path="/about">
              <About />
            </Route>
            <Route exact path="/doc">
              <Documentation />
            </Route>
          </Switch>
        </div>
        <Footer />
      </Router>
    </div>
  );
}

export default App;

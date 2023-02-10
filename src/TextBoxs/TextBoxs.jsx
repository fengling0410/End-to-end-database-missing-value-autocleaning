import { useEffect, useState } from "react";
import "./TextBoxs.scss";
import axios from "axios";

const TextBoxs = ({ onChange }) => {
  const [table, setTableName] = useState("");
  const [column, setColumnName] = useState("");
  const [foreignKey, setForeignKey] = useState("");
  const [query, setqueryName] = useState("");

  const queryStr = new FormData();
  queryStr.append("table", table);
  queryStr.append("column", column);
  queryStr.append("foreignKey", foreignKey);
  queryStr.append("query", query);

  const sendStringsHandler = () => {
    axios
      .post("http://localhost:8000/sendqueries", queryStr)
      .then((res) => {})
      .catch((err) => {
        console.error(err);
      });
  };

  useEffect(() => {
    onChange && onChange({ table, column, foreignKey, query });
  }, [table, column, foreignKey, query]);

  return (
    <li className="textBoxs">
      <form>
        <label>Table Name: (e.g. users)</label>
        <textarea
          required
          onChange={(e) => setTableName(e.target.value)}
        ></textarea>
        <label>Column Name: (e.g. user_id)</label>
        <textarea
          required
          onChange={(e) => setColumnName(e.target.value)}
        ></textarea>
        <label>Foreign Key: (e.g. left_table_attribute:right_table_name,right_table_attribute; or NA if no foreign key)</label>
        <textarea
          required 
          onChange={(e) => setForeignKey(e.target.value)}
        ></textarea>
        <label>SQL query you want to perform: (e.g. SELECT user_id from users; or NA if no sql query)</label>
        <textarea
          required
          onChange={(e) => setqueryName(e.target.value)}
        ></textarea>
        <button onClick={sendStringsHandler}>submit </button>
      </form>
    </li>
  );
};

export default TextBoxs;

import React from "react";
import ReactDOM from "react-dom";
import "./CSS/index.css";
import App from "./App";
import { BrowserRouter } from "react-router-dom";

// It is necessary to have the browser router wrapped around the app itself. the public url is used to set the base url to which all derived pages are relative. Generally speaking don't touch this page.

ReactDOM.render(
  <BrowserRouter basename={process.env.PUBLIC_URL}>
    <App id="content" />
  </BrowserRouter>,
  document.getElementById("root")
);

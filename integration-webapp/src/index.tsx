import React from "react";
import { createRoot } from "react-dom/client";
import { Main } from "./components/Main"

const root = createRoot(document.getElementById("root") as HTMLElement);
root.render(
    <React.StrictMode>
        <Main/>
    </React.StrictMode>
);
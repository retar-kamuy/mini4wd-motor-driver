import React from "react";
import { Header } from "./components/header";
import { RulesEditor } from "./components/rules-editor";
import { LapTimer } from "./components/lap-timer";
import { Wizard } from "./components/wizard";

const App: React.FC = () => {
  return (
    <>
      <Header />
      <main style={{ padding: "1rem" }}>
        <RulesEditor />
        <LapTimer />
        <Wizard />
      </main>
    </>
  );
};

export default App;

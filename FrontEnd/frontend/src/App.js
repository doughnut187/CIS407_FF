import styled from "styled-components";
import { Routes, Route } from "react-router";

import { ColorProvider } from "./ContextProviders/ColorContext";

import LandingPage from "./Pages/LandingPage";
import CreateProfilePage from "./Pages/CreateProfilePage";
import SignInPage from "./Pages/SignInPage";
import MonsterPage from "./Pages/MonsterPage";
import AccountPage from "./Pages/AccountPage";
import WorkoutLogPage from "./Pages/WorkoutLogPage";
import PastWorkoutsPage from "./Pages/PastWorkoutsPage";
import FirstTimeQuizPage from "./Pages/FirstTimeQuizPage";

function App() {
  return (
    <ColorProvider>
      {/* This ColorProvider Object provides color context for all things inside it. */}
      <Body>
        {/* The Routes object acts as a router for the single app, moving between provided routes */}
        <Routes>
          {/* each route provides a path relative to the root, and the element object passed into it as a prop is the page that it loads when the router is given that path */}
          <Route path="/" exact element={<LandingPage />} />
          <Route path="/CreateProfile" element={<CreateProfilePage />} />
          <Route path="/SignIn" element={<SignInPage />} />
          <Route path="/MonsterPage" element={<MonsterPage />} />
          <Route path="/AccountPage" element={<AccountPage />} />
          <Route path="/WorkoutLogPage" element={<WorkoutLogPage />} />
          <Route path="/PastWorkoutsPage" element={<PastWorkoutsPage />} />
          <Route path="/FirstTimeQuizPage" element={<FirstTimeQuizPage />} />
        </Routes>
      </Body>
    </ColorProvider>
  );
}

export default App;

const Body = styled.div``;

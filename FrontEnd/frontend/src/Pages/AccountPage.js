import { useContext } from "react";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";
import RibbonBar from "../Components/RibbonBar";

function AccountPage() {
  // used to provide the "theme" color prop to all elements the reference the prop in their css
  const theme = useContext(ColorContext);
  // page targets and page titles are distributed individually to each page. We don't want a page to have a load button for the page that it is already on. Make sure that the page targets correlate correctly to the page titles. They will be unpacked in the same order.
  const pageTargets = ["/MonsterPage", "/WorkoutLogPage", "/PastWorkoutsPage"];
  const pageTitles = [
    "Your Monster",
    "Daily Workout Log",
    "Your Past Workouts",
  ];
  return (
    <Body theme={theme}>
      <RibbonBar pageTitles={pageTitles} pageTargets={pageTargets} />
    </Body>
  );
}

export default AccountPage;

const Body = styled.div`
  background-color: ${(props) => props.theme.primaryBackground};
  width: 100vw;
  height: 100vh;
`;

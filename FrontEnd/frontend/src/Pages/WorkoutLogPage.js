import { useContext } from "react";
import styled from "styled-components";
import RibbonBar from "../Components/RibbonBar";
import { ColorContext } from "../ContextProviders/ColorContext";

function WorkoutLogPage() {
  // this is so we can distribute the color context to the individual components.
  const theme = useContext(ColorContext);
  const [loading, setLoading] = useContext(true);
  // page targets and page titles are distributed individually to each page. We don't want a page to have a load button for the page that it is already on. Make sure that the page targets correlate correctly to the page titles. They will be unpacked in the same order.
  const pageTargets = ["/AccountPage", "/MonsterPage", "/PastWorkoutsPage"];
  const pageTitles = [
    "Your Account Info",
    "Your Monster",
    "Your Past Workouts",
  ];

  if (loading) {
    return (
      <LoadingWrapper theme={theme}>
        <LoadingText theme={theme}>
          <LoadingTextWrapper theme={theme}>Loading...</LoadingTextWrapper>
        </LoadingText>
      </LoadingWrapper>
    );
  } else {
    return (
      <Body theme={theme}>
        <RibbonBar pageTitles={pageTitles} pageTargets={pageTargets} />
      </Body>
    );
  }
}

export default WorkoutLogPage;

const Body = styled.div`
  width: 100vw;
  height: 100vh;
  background-color: ${(props) => props.theme.primaryBackground};
`;

const LoadingWrapper = styled.div`
  background-color: ${(props) => props.theme.primaryBackground};
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
`;

const LoadingTextWrapper = styled.div`
  background-color: ${(props) => props.theme.secondaryBackground};
  display: flex;
  justify-content: center;
  align-items: center;
  width: max(20vw, 200px);
  height: 10vh;
  border-radius: 20px;
  box-shadow: -4px 4px 14px black;
`;

const LoadingText = styled.h1`
  color: ${(props) => props.theme.primaryText};
  font-weight: bolder;
  text-align: center;
`;

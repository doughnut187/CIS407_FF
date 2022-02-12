import styled from "styled-components";
import { useContext } from "react";
import { ColorContext } from "../ContextProviders/ColorContext";
import { useNavigate } from "react-router";

function LandingPage() {
  // This is a simple landing page. Eventually we will have display on this page about all the technology and work that went into its creation. Group photo of us at the bottom?

  // This provides color theme as a prop for each element that requires it.
  const theme = useContext(ColorContext);
  // this function is used to forcefully navigate the user.
  const navigate = useNavigate();
  return (
    <Body theme={theme}>
      <LogoContainer theme={theme}>
        <Logo>
          My Fitness Fiend
          <sup>
            <sup style={{ fontSize: "small" }}>TM</sup>
          </sup>
        </Logo>
      </LogoContainer>
      <LandingButton
        theme={theme}
        onClick={() => {
          navigate("/SignIn");
        }}
      >
        Start Fiending
      </LandingButton>
    </Body>
  );
}

export default LandingPage;

const Body = styled.div`
  color: ${(props) => props.theme.primaryText};
  height: 100vh;
  width: 100vw;
  background-color: ${(props) => props.theme.primaryBackground};
`;

const Logo = styled.h1`
  color: white;
  padding: 20px;
  border-radius: 20px;
  font-size: min(10vw, 55px);
`;

const LogoContainer = styled.div`
  align-content: center;
  justify-content: center;
  transform: translate(-50%, -50%);
  position: absolute;
  top: 30vh;
  left: 45vw;
  display: flex;
  width: 90vw;
`;

const LandingButton = styled.button`
  outline: none;
  border: 3px solid ${(props) => props.theme.primaryButtonOutline};
  text-decoration: none;
  color: white;
  position: absolute;
  transform: translate(-50%, -50%);
  top: 65vh;
  left: 65vw;
  background-color: ${(props) => props.theme.primaryButton};
  width: max(120px, 10vw);
  padding-top: 20px;
  padding-bottom: 20px;
  width: max(120px, 10vw);
  text-overflow: clip;
  justify-content: center;
  align-content: center;
  text-align: center;
  text-justify: center;
  border-radius: 6px;
  transition: ease all 1s;

  :hover {
    background-color: ${(props) => props.theme.primaryButtonAltHover};
    box-shadow: 10px 10px 10px
      ${(props) => props.theme.secondaryBackgroundShadow};
  }
`;

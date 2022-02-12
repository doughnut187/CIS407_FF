import { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";
import { useNavigate } from "react-router-dom";
import jwtDecode from "jwt-decode";

function CreateProfilePage() {
  // used to navigate between pages
  const navigate = useNavigate();
  // passes off theme context
  const theme = useContext(ColorContext);
  // the states we use to track user input
  const [email, setEmail] = useState(null);
  const [password, setPassword] = useState(null);
  const [username, setUsername] = useState(null);

  // This is used to update the value of an input field as it changes. Notice that it is tied to the onChange event handler
  function ChangHandler(value, setFunction) {
    setFunction(value);
  }

  // This is tied to the outermost div of the page. This handles key presses. If the enter key is pressed the submit function is called
  const HandleEnterPress = (e) => {
    if (e.key === "Enter") {
      SubmitHandler();
    }
  };

  // this useEffect pulls the user token from local storage. If the user token exists then it is queried for age. If it is still valid, then the user is redirected to the monster page
  useEffect(() => {
    let userToken = localStorage.getItem("id_token");
    if (userToken) {
      userToken = jwtDecode(userToken);
      if (userToken.exp * 1000 > Date.now()) {
        navigate("/MonsterPage");
      }
    }
  });

  // this function handles submitting the data
  function SubmitHandler() {
    // error checks
    if (email === null || email === "") {
      alert("Not a valid email");
      return;
    } else if (username === null || username === "") {
      alert("Not a valid username");
      return;
    } else if (password === null || password === "") {
      alert("Not a valid password");
      return;
    }

    //TODO: update this to use the RESTful api that Jordan made
    const accountInfo = {
      method: "POST",
      headers: {
        "Content-Type": "application/JSON",
        Contents: "accountInfo",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    };

    fetch("/create_account", accountInfo).then((response) => {
      console.log(response);
      if (response.status === 201) {
        response.json().then((json) => {
          localStorage.setItem("id_token", json.token);
          navigate("/monsterpage");
        });
      } else if (response.status === 409) {
        alert("That user already exists!");
      } else if (response.status === 500) {
        alert("Unable to connect to server! Please try again later!");
      } else {
        alert("Failed to create profile!");
      }
    });
  }

  return (
    <Body theme={theme} onKeyDown={HandleEnterPress}>
      <LoginWrapper theme={theme} id={"identif"}>
        <LoginTitle theme={theme}>Create Profile</LoginTitle>
        <LoginInputWrapper>
          <LoginInput
            theme={theme}
            placeholder="Username"
            onChange={(e) => ChangHandler(e.target.value, setUsername)}
          ></LoginInput>
          <LoginInput
            theme={theme}
            placeholder="Email"
            onChange={(e) => ChangHandler(e.target.value, setEmail)}
            type="email"
          ></LoginInput>
          <LoginInput
            theme={theme}
            placeholder="Password"
            onChange={(e) => ChangHandler(e.target.value, setPassword)}
            type="password"
          ></LoginInput>
          <SubmitSwitchWrapper>
            {/* TODO: change this to a button with a navigate() function, and move the stylings into a styled div below */}
            <Link
              to="/SignIn"
              style={{
                margin: "auto",
                textAlign: "center",
                color: `${theme.primaryText}`,
                textDecoration: "none",
                width: "50%",
                fontSize: "2.2vh",
                fontWeight: "bolder",
                lineHeight: "2",
              }}
            >
              Already a fiender?
              <br />
              Sign In
            </Link>
            <SubmitButton theme={theme} onClick={SubmitHandler}>
              Create
            </SubmitButton>
          </SubmitSwitchWrapper>
        </LoginInputWrapper>
      </LoginWrapper>
    </Body>
  );
}

export default CreateProfilePage;

const Body = styled.div`
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: ${(props) => props.theme.primaryBackground};
  justify-content: center;
  align-items: center;
`;

const LoginWrapper = styled.div`
  border: 2px solid black;
  margin-bottom: 20vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 70vh;
  width: min(80vw, 500px);
  background-color: ${(props) => props.theme.secondaryBackground};
  box-shadow: -8px 8px 20px ${(props) => props.theme.secondaryBackgroundShadow};
  border-radius: 20px;
`;

const LoginTitle = styled.h2`
  padding-bottom: 0;
  margin-bottom: 0;
  margin-top: auto;
  text-align: center;
  font-size: max(3vw, 5vh);
  color: ${(props) => props.theme.primaryText};
  //text-shadow: -8px 8px 6px black; // I don't know how I feel about the font shadowing on this
`;

const LoginInputWrapper = styled.div`
  display: flex;
  margin: auto;
  height: 60%;
  width: 90%;
  align-items: center;
  flex-direction: column;
  justify-content: space-evenly;
`;

const LoginInput = styled.input`
  width: 85%;
  border-radius: 8px;
  height: min(16%, 35px);
  outline: none;
  text-align: center;
  font-size: max(2.2vh, 110%);
  transition: ease all 0.2s;

  :focus {
    box-shadow: -4px 4px 10px
      ${(props) => props.theme.secondaryBackgroundShadow};
    border: 4px solid ${(props) => props.theme.primaryInputOutline};
  }
`;

// this controls the row spacing of the submit button and the sign in link
const SubmitSwitchWrapper = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  width: 100%;
  height: 25%;
  padding-top: 20px;
`;

const SubmitButton = styled.button`
  width: 40%;
  background-color: ${(props) => props.theme.primaryButton};
  color: ${(props) => props.theme.primaryText};
  border-radius: 15px;
  border: 3px solid ${(props) => props.theme.primaryButtonOutline};
  transition: ease all 0.2s;
  font-size: 2.5vh;
  font-weight: bold;

  :hover {
    box-shadow: -3px 3px 6px ${(props) => props.theme.secondaryBackgroundShadow};
    border: 3px solid ${(props) => props.theme.primaryButtonHoverOutline};
  }
`;

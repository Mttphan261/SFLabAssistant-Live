import React, { useState, useContext } from "react";
import UserContext from "../../context/UserContext";
import { Link } from "react-router-dom";
import { Nav, Navbar, Container, Image, Button } from "react-bootstrap";


function Header() {
  const { user, setUser } = useContext(UserContext);
  const [alertMessage, setAlertMessage] = useState("");


  // **** ALERT MESSAGE ****
  const showAlert = (message) => {
    setAlertMessage(message);
    alert(message);
    setTimeout(() => {
      setAlertMessage("");
    }, 3000);
  };

  const handleLogout = async () => {
    try {
      await fetch("/api/logout", {
        method: "POST",
        credentials: "same-origin",
      });
      setUser(null);
      showAlert("You have logged out. We await your return, warrior!")
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Navbar>
      <Container>
        <Navbar.Brand>
          <Link to="/">SF6 Lab Assistant</Link>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav
            className="custom-header justify-content-end"
            style={{ width: "100%" }}
          >
            {user ? (
              <>
                <Nav.Link as={Link} to="/profile">
                  Profile
                </Nav.Link>
                <Nav.Link as={Link} to="/" onClick={handleLogout}>
                  Logout
                </Nav.Link>
              </>
            ) : (
              <>
                <Nav.Link as={Link} to="/signup">
                  Sign Up
                </Nav.Link>
                <Nav.Link as={Link} to="/login">
                  Login
                </Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;

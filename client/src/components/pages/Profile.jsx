import React, { useState, useEffect, useContext } from "react";
import { Link, useParams } from "react-router-dom";
import UserContext from "../../context/UserContext";
import { Row, Col, Container, Image, Card } from "react-bootstrap";

function Profile() {
  const { user, setUser } = useContext(UserContext);
  const [userCharacter, setUserCharacter] = useState([]);

  useEffect(() => {
    if (user) {
      fetch("/api/users", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((userData) => {
          console.log(userData.user_characters);
          setUserCharacter(userData.user_characters);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [user]);

  const handleDeleteCharacter = async (userCharacterId) => {

    const confirmed = window.confirm("Are you sure you want to delete this character from your roster?");

    if(!confirmed) {
      return;
    }

    try {
      const response = await fetch(`/api/usercharacters/${userCharacterId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        setUser((prevUser) => ({
          ...prevUser,
          user_characters: prevUser.user_characters.filter(
            (uc) => uc.id !== userCharacterId
          ),
        }));
        console.log("Character deleted from user roster");
      } else {
        console.error(
          "Failed to delete character from user roster",
          response.status
        );
      }
    } catch (error) {
      console.error("Failed to delete character from user roster", error);
    }
  };

  return user ? (
    <>
      <div className="profile-jumbotron jumbotron-fluid">
        <Container>
          <h1
            className='profile-greeting'
          >
            Welcome back to the lab, {user.username} !
          </h1>
        </Container>
      </div>
      <Container>
        <Row
          style={{
            marginTop: "50px",
            marginBottom: "10px",
          }}
        >
          <Col
            style={{
              marginTop: "5%",
            }}
          >
            <h2>{user.username}</h2>
            <h2>{user.email}</h2>
            <p>Member since: {user.created_at}</p>
          </Col>
          <Col className="profile-roster">
            <h2>Roster:</h2>
            {userCharacter.length <= 0 ? (
              <h4>No fighters in your roster</h4>
            ) : (
              <Row className="seperator">
                {userCharacter.map((uc) => (
                  <Col key={uc.id} md={4} className="seperator">
                    <Link to={`/characters/${uc.character.name}`}>
                      <Image
                        // className="circle"
                        className="profileRosterIcon"
                        src={uc.character.head_img}
                        alt={uc.character.name}
                      />
                    </Link>
                    <Col
                      style={{
                        marginTop: "5px",
                      }}
                    >
                      <button
                        onClick={() => handleDeleteCharacter(uc.id)}
                        style={{
                          padding: "10px",
                        }}
                      >
                        Delete From Roster
                      </button>
                    </Col>
                  </Col>
                ))}
              </Row>
            )}
            {/* <Row className="seperator">
        {userCharacter.map((uc) => (
          <Col key={uc.id} md={4} className="seperator">
            <Link to={`/characters/${uc.character.name}`}>
            <Image
              // className="circle"
              className="profileRosterIcon"
              src={uc.character.head_img}
              alt={uc.character.name}
            />
            </Link>
            <Col style={{
              marginTop: '5px'
            }}>
            <button onClick={() => handleDeleteCharacter(uc.id)} style={{
              padding: "10px",
            }}>Delete From Roster</button>
            </Col>
          </Col>
        ))}
        </Row> */}
          </Col>
        </Row>
      </Container>
    </>
  ) : (
    <h2>Please login or signup to view your profile</h2>
  );
}

export default Profile;

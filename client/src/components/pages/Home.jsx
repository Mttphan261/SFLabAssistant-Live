import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Card, Container, Image, Row, Col } from "react-bootstrap";
import { FaDatabase, FaClipboardList } from "react-icons/fa";
import { GiWeightLiftingUp } from "react-icons/gi";

const Home = () => {
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
    fetch(`/api/characters`)
      .then((r) => r.json())
      .then((data) => setCharacters(data))
      .catch((error) => {
        console.log(error);
      });
  }, []);


  const characterDisplay = characters.map((character) => {
    return (
      <Col xs={4} sm={4} md={2} className='fighter-icon'>
        <div className="circle">
          <Link to={`/characters/${character.name}`} key={character.id}>
            <Image
              // className="circle"
              className="rosterIcon"
              roundedCircle
              src={character.head_img}
              alt={character.name}
            />
          </Link>
          <Image
            className="splatter"
            src="https://raw.githubusercontent.com/Mttphan261/SFLabAssistant/9088c2605aae9b049aa5789e86d77be1d7ce10d8/.github/imgs/HomePage/InkSplatter.svg"
          />
        </div>
      </Col>
    );
  });

  return (
    <div
      style={{
        marginBottom: "3%",
      }}
    >
      <div className="home-jumbotron jumbotron-fluid">
        <Container>
          <h1
            style={{
              color: "#fff",
              textShadow: "2px 2px 4px rgba(0, 0, 0, 0.8)",
              fontWeight: "700",
            }}
          >
            Welcome to the SF6 Lab Assistant
          </h1>
          <h2
            style={{
              color: "#fff",
              textShadow: "2px 2px 4px rgba(0, 0, 0, 0.8)",
              fontWeight: "500",
            }}
          >
            Take your training to the next level{" "}
          </h2>
        </Container>
      </div>
      <Container className="featureBanner">
        <Row>
          <Col md={4}>
            <div className="feature-box text-center">
              <FaDatabase className="feature-icon" />
              <h3>Explore Fighter Data</h3>
              <p>
                Dive into each fighter's page, complete with move lists and
                video libraries.
              </p>
            </div>
          </Col>
          <Col md={4}>
            <div className="feature-box text-center">
              <GiWeightLiftingUp className="feature-icon" />
              <h3>Build Your Personal Roster</h3>
              <p>
                Curate your own individualized roster to keep track of your
                favorite fighters.
              </p>
            </div>
          </Col>
          <Col md={4}>
            <div className="feature-box text-center">
              <FaClipboardList className="feature-icon" />
              <h3>Create Training Journals </h3>
              <p>
                Maintain training notes for each character, making it easy to
                reference your progress.
              </p>
            </div>
          </Col>
        </Row>
      </Container>
      <Container>
        <Row>{characterDisplay}</Row>
      </Container>
    </div>
  );
};

export default Home;

import { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import reactLogo from "./assets/react.svg";
import Home from "./components/pages/Home.jsx";
import Fighter from "./components/pages/Fighter";
import Header from "./components/pages/Header";
import SignUp from "./components/pages/SignUp";
import SignIn from "./components/pages/SignIn";
import Profile from "./components/pages/Profile";
import viteLogo from "/vite.svg";
import 'bootstrap/dist/css/bootstrap.css';
import "./App.css";
import UserContext from "./context/UserContext";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (user == null) {
      fetch("/api/check_session").then((r) => {
        if (r.ok) {
          r.json().then((user) => {
            setUser(user);
          });
        }
      });
    }
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <div className='App'>
        <Router>
          <Header />
          <Routes>
            <Route path="/" index element={<Home />} />
            <Route path="/characters/:name" element={<Fighter />} />
            <Route path="/signUp" element = {<SignUp />} />
            <Route path="/login" element = {<SignIn />} />
            <Route path="/profile" element = {<Profile />} />
          </Routes>
        </Router>
      </div>
    </UserContext.Provider>
  );
}

export default App;

import logo from "./logo.svg";
import "./App.css";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Homepage from "./pages/Homepage";
import IncidentPage from "./pages/IncidentPage";
import CustomAppBar from "./elements/CustomAppBar";

function App() {
  return (
    <div className="Apps">

      <CustomAppBar/>
      <Router>
        <Routes>
        <Route exact path="/" element={<Homepage/>} />
        <Route exact path="/incidents/:id" element={<IncidentPage/>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

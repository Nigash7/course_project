import { HashRouter, Routes, Route } from "react-router-dom";
import Login from "./login";
import Home from "./home";
import CourseVideo from "./CourseVideo";
import Logout from "./logout";

function App() {
  return (
   <HashRouter>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<Home />} />
      <Route path="/course/:id" element={<CourseVideo />} />
      <Route path="/logout" element={<Logout />} />
    </Routes>
  </HashRouter>
  );
}

export default App;
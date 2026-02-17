import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Home() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);

 useEffect(() => {
  const token = localStorage.getItem("token");

  if (!token) {
    navigate("/");
    return;
  }

  axios
    .get("https://course-project-66az.onrender.com/api/my-courses/", {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    .then((response) => {
      setCourses(response.data);
    })
    .catch((error) => {
      console.error(error);
      localStorage.removeItem("token");
      navigate("/");
    });
}, []);
  return (
    <div>
      {/* Navbar */}
      <nav className="navbar navbar-dark bg-primary">
        <div className="container">
          <span className="navbar-brand mb-0 h1">Course Portal</span>

          <button onClick={handleLogout} className="btn btn-light">
            Logout
          </button>
        </div>
      </nav>

      {/* Course Section */}
      <div className="container mt-5">
        <h2 className="text-center mb-4">My Courses</h2>

        <div className="row">
          {courses.length > 0 ? (
            courses.map((course) => (
              <div className="col-md-4 mb-4" key={course.id}>
                <div className="card shadow h-100">
                  <div className="card-body">
                    <h5 className="card-title">{course.title}</h5>
                    <p className="card-text">{course.description}</p>
                   <button
                        onClick={() => handleVideo(course)}
                           className="btn btn-primary">
                               View Course
                   </button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-center">No enrolled courses available</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;
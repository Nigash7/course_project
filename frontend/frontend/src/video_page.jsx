import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

function VideoPage() {
  const { id } = useParams(); // course ID from URL
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/"); // if not logged in, go to login
      return;
    }

    // Fetch course by ID
    axios
      .get(`http://127.0.0.1:8000/api/courses/${id}/`, {
        headers: {
          Authorization: `Token ${token}`, // or Bearer if using JWT
        },
      })
      .then((response) => {
        setCourse(response.data);
      })
      .catch((error) => {
        console.error(error);
        navigate("/home"); // go back to courses if error
      });
  }, [id, navigate]);

  if (!course) {
    return <p className="text-center mt-5">Loading course...</p>;
  }

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">{course.title}</h2>
      <p>{course.description}</p>

      {/* Video Section */}
      {course.video_url ? (
        <div className="text-center">
          <video width="720" controls>
            <source src={course.video_url} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      ) : (
        <p>No video available for this course.</p>
      )}

      <div className="text-center mt-4">
        <button className="btn btn-primary" onClick={() => navigate("/home")}>
          Back to Courses
        </button>
      </div>
    </div>
  );
}

export default VideoPage;
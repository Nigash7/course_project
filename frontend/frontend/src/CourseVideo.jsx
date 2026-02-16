import { useLocation, useNavigate } from "react-router-dom";

function VideoPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const course = location.state?.course;

  if (!course) {
    return <p className="text-center mt-5">Course not found</p>;
  }

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">{course.title}</h2>
      <p>{course.description}</p>

      {course.embed_url ? (
        <div className="text-center">
          <iframe
            width="100%"
            height="500"
            src={course.embed_url}
            title={course.title}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      ) : (
        <p className="text-danger">No video available for this course.</p>
      )}

      <div className="text-center mt-4">
        <button
          className="btn btn-primary"
          onClick={() => navigate("/home")}
        >
          Back to Courses
        </button>
      </div>
    </div>
  );
}

export default VideoPage;
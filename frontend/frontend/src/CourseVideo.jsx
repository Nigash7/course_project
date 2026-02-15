import { useLocation, useNavigate } from "react-router-dom";

function VideoPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const course = location.state?.course; // get course from Home.js

  if (!course) {
    return <p className="text-center mt-5">Course not found</p>;
  }

  // Convert YouTube URLs to embed format
  const getYouTubeEmbed = (url) => {
    if (!url) return null;

    let videoId = null;

    if (url.includes("youtu.be")) videoId = url.split("youtu.be/")[1];
    else if (url.includes("youtube.com/watch?v="))
      videoId = url.split("v=")[1].split("&")[0];
    else if (url.includes("youtube.com/embed/")) return url;

    return `https://www.youtube.com/embed/${videoId}`;
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">{course.title}</h2>
      <p>{course.description}</p>

      {course.video_url ? (
        <div className="text-center">
          <iframe
            width="720"
            height="405"
            src={getYouTubeEmbed(course.video_url)}
            title={course.title}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
          
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
import axios from "axios";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    const logoutUser = async () => {
      try {
        const token = localStorage.getItem("token");

        await axios.post(
          "http://127.0.0.1:8000/api/logout/",
          {},
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        // ✅ Delete local storage token
        localStorage.removeItem("token");

        navigate("/");

      } catch (error) {
        console.log(error);

        // Even if API fails, remove token
        localStorage.removeItem("token");
        navigate("/");
      }
    };

    logoutUser();
  }, [navigate]);

  return <h3>Logging out...</h3>;
}

export default Logout;
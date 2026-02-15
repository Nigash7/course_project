import { useState, useEffect } from "react";
import axios from "axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // ✅ Check token when component loads
      useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
          window.location.href = "/home";
        }
      }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/student_login/",
        {
          email: email,
          password: password,
        }
      );

      // Store token
      localStorage.setItem("token", response.data.token);

      alert("Login Successful");

      window.location.href = "/home";
    } catch (error) {
      alert("Invalid Email or Password");
    }
  };

  return (
    <div className="vh-100 d-flex justify-content-center align-items-center bg-light">
      <div
        className="card shadow-lg p-4"
        style={{ width: "350px", borderRadius: "15px" }}
      >
        <h3 className="text-center mb-4">Login</h3>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Email address</label>
            <input
              type="email"
              className="form-control"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn btn-primary w-100">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
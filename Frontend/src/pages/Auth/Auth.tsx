/* eslint-disable @typescript-eslint/no-explicit-any */
import "./Auth.css";

import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { login, register } from "../../api/authApi";

const Auth = () => {
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);

  const [formData, setFormData] = useState({
    username: "",

    email: "",

    password: "",

    confirmPassword: "",
  });

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [animate, setAnimate] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,

      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setError("");

    setLoading(true);

    try {
      if (isLogin) {
        const data = await login(
          formData.username,

          formData.password,
        );

        localStorage.setItem(
          "access_token",

          data.access,
        );

        localStorage.setItem(
          "refresh_token",

          data.refresh,
        );

        localStorage.setItem(
          "user",

          JSON.stringify(data.user),
        );

        navigate("/workspaces");
      } else {
        if (formData.password !== formData.confirmPassword) {
          setError("Passwords do not match");

          setLoading(false);

          return;
        }

        await register({
          username: formData.username,

          email: formData.email,

          password: formData.password,
        });

        setIsLogin(true);

        setFormData({
          username: formData.username,

          email: "",

          password: "",

          confirmPassword: "",
        });

        setError("");
      }
    } catch (err: any) {
      console.log(err);

      if (err.response?.data) {
        const errors = err.response.data;

        if (typeof errors === "string") {
          setError(errors);
        } else if (errors.detail) {
          setError(errors.detail);
        } else {
          const firstError = Object.values(errors)[0];

          setError(
            Array.isArray(firstError) ? firstError[0] : String(firstError),
          );
        }
      } else {
        setError("Something went wrong");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-left">
        <div className="logo">INFRAMIND</div>

        <h1>
          AI Infrastructure
          <br />
          Analysis
        </h1>

        <div className="tagline">
          <span>Monitor.</span>

          <span>Predict.</span>

          <span>Resolve.</span>
        </div>

        <div className="features">
          <div>✓ AI Root Cause Analysis</div>

          <div>✓ Predict Infrastructure Risks</div>

          <div>✓ Trend Analysis</div>

          <div>✓ Recommended Actions</div>
        </div>
      </div>

      <div className="auth-right">
        <form
          className={`auth-form

        ${animate ? "fade-out" : "fade-in"}

        `}
          onSubmit={handleSubmit}
        >
          <h2>{isLogin ? "Welcome Back" : "Create Account"}</h2>

          <p>
            {isLogin
              ? "Sign in to continue to InfraMind"
              : "Start your AI monitoring journey"}
          </p>

          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
          />

          {!isLogin && (
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          )}

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />

          {!isLogin && (
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
          )}

          {error && <div className="error">{error}</div>}

          <button type="submit" disabled={loading}>
            {loading
              ? "Please wait..."
              : isLogin
                ? "Sign In"
                : "Create Account"}
          </button>

          <div className="switch-auth">
            {isLogin ? "New to InfraMind?" : "Already have an account?"}

            <span
              onClick={() => {
                setAnimate(true);

                setTimeout(() => {
                  setIsLogin(!isLogin);

                  setError("");

                  setAnimate(false);
                }, 200);
              }}
            >
              {isLogin ? " Create Account" : " Sign In"}
            </span>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Auth;

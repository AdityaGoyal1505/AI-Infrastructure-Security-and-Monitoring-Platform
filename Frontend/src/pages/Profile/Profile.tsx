import "./Profile.css";

import { useNavigate } from "react-router-dom";

import { ArrowLeft, Calendar, IdCard, LogOut, Mail, User } from "lucide-react";

const Profile = () => {
  const navigate = useNavigate();

  const user = {
    id: 1,

    username: "Aditya Goyal",

    email: "aditya@example.com",

    created_at: "2026-05-18",
  };

  const logout = () => {
    localStorage.clear();

    navigate("/home");
  };

  return (
    <div className="profile-page">
      <div className="profile-topbar">
        <button className="top-btn" onClick={() => navigate(-1)}>
          <ArrowLeft size={18} />
          Back to Home
        </button>

        <button className="top-btn log-btn" onClick={logout}>
          <LogOut size={18} />
          Logout
        </button>
      </div>

      <div className="profile-header">
        <div className="profile-avatar">
          {user.username

            .charAt(0)

            .toUpperCase()}
        </div>

        <h1>{user.username}</h1>

        <p>Software Developer</p>

        <div className="profile-divider"></div>
      </div>

      <div className="profile-info">
        <div className="info-row">
          <div className="info-left">
            <User size={18} />

            <span>Username</span>
          </div>

          <div className="info-right">{user.username}</div>
        </div>

        <div className="info-row">
          <div className="info-left">
            <Mail size={18} />

            <span>Email</span>
          </div>

          <div className="info-right">{user.email}</div>
        </div>

        <div className="info-row">
          <div className="info-left">
            <IdCard size={18} />

            <span>User ID</span>
          </div>

          <div className="info-right">{user.id}</div>
        </div>

        <div className="info-row">
          <div className="info-left">
            <Calendar size={18} />

            <span>Joined</span>
          </div>

          <div className="info-right">18 May 2026</div>
        </div>
      </div>
    </div>
  );
};

export default Profile;

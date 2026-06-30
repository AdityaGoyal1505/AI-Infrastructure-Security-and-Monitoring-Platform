import { useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import "./Header.css";

import { FiBell, FiSearch, FiSettings } from "react-icons/fi";

const Header = () => {
  const location = useLocation();

  const navigate = useNavigate();

  const { id } = useParams();

  const [search, setSearch] = useState("");

  const getTitle = () => {
    if (location.pathname.includes("/dashboard")) {
      return "Dashboard";
    }

    if (location.pathname.includes("/insights")) {
      return "AI Analysis";
    }

    if (location.pathname.includes("/predictions")) {
      return "Predictions";
    }

    if (location.pathname.includes("/trends")) {
      return "Trends";
    }

    if (location.pathname.includes("/setup")) {
      return "Configuration";
    }

    return "";
  };

  const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key !== "Enter") {
      return;
    }

    const query = search

      .toLowerCase()

      .trim();

    if (
      query.includes("dashboard") ||
      query.includes("anomaly") ||
      query.includes("recommendation")
    ) {
      navigate(`/workspaces/${id}/dashboard`);
    } else if (
      query.includes("ai") ||
      query.includes("insight") ||
      query.includes("rca") ||
      query.includes("root cause") ||
      query.includes("incident")
    ) {
      navigate(`/workspaces/${id}/insights`);
    } else if (query.includes("risk") || query.includes("prediction")) {
      navigate(`/workspaces/${id}/predictions`);
    } else if (query.includes("trend")) {
      navigate(`/workspaces/${id}/trends`);
    } else if (
      query.includes("setup") ||
      query.includes("config") ||
      query.includes("configuration") ||
      query.includes("agent") ||
      query.includes("delete")
    ) {
      navigate(`/workspaces/${id}/setup`);
    }
  };

  return (
    <header className="header">
      <div className="header-left">
        <h1>{getTitle()}</h1>

        {/* <div className="workspace-pill">

          <span className="workspace-dot"></span>



          {

            workspace?.name

            ||

            "No Workspace"

          }

        </div> */}
      </div>

      <div className="header-center">
        <div className="search-box">
          <FiSearch />

          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={handleSearch}
            placeholder="Search pages, RCA, risks..."
          />
        </div>
      </div>

      <div className="header-right">
        <div className="ai-pill">✨ AI Engine Active</div>

        <button className="icon-btn">
          <FiBell />
        </button>

        <button className="icon-btn" onClick={() => navigate("/profile")}>
          <FiSettings />
        </button>

        <div className="avatar">G</div>
      </div>
    </header>
  );
};

export default Header;

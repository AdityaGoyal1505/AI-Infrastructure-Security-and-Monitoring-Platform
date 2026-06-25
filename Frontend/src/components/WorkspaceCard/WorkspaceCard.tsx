import "./WorkspaceCard.css";

import { useNavigate } from "react-router-dom";

import type { Workspace } from "../../pages/Workspaces/Workspaces";

import { useWorkspace } from "../../context/WorkspaceContext";

interface WorkspaceCardProps {
  workspace: Workspace;
}

const WorkspaceCard = ({ workspace }: WorkspaceCardProps) => {
  const navigate = useNavigate();

  const { setWorkspace } = useWorkspace();

  const openWorkspace = () => {
    setWorkspace({
      id: workspace.id,

      name: workspace.name,

      is_active: workspace.is_active,
    });

    navigate(`/workspaces/${workspace.id}/dashboard`);
  };

  return (
    <div className="workspace-card">
      <div className="workspace-info">
        <h2>{workspace.name}</h2>

        <p className="workspace-description">
          {workspace.description || "No description provided"}
        </p>

        <div className="workspace-meta">
          <div>
            <span>Created</span>

            <p>
              {new Date(workspace.created_at).toLocaleDateString(
                "en-IN",

                {
                  day: "numeric",

                  month: "long",

                  year: "numeric",
                },
              )}
            </p>
          </div>

          <div>
            <span>Status</span>

            <p
              className={
                workspace.is_active ? "status active" : "status inactive"
              }
            >
              {workspace.is_active ? "Active" : "Inactive"}
            </p>
          </div>
        </div>
      </div>

      <button className="open-workspace-btn" onClick={openWorkspace}>
        Open →
      </button>
    </div>
  );
};

export default WorkspaceCard;

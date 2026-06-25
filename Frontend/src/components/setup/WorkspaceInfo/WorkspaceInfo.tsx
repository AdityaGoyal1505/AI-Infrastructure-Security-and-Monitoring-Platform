import "./WorkspaceInfo.css";

import { useWorkspace } from "../../../context/WorkspaceContext";

const WorkspaceInfo = () => {
  const { workspace } = useWorkspace();

  return (
    <div className="workspace-info-card">
      <h2>Workspace Information</h2>

      <div className="workspace-grid">
        <div>
          <span>Name</span>

          <h3>{workspace.name}</h3>
        </div>

        <div>
          <span>Status</span>

          <h3>{workspace.is_active ? "Healthy" : "Inactive"}</h3>
        </div>

        <div>
          <span>Workspace ID</span>

          <h3>{workspace.id}</h3>
        </div>
      </div>
    </div>
  );
};

export default WorkspaceInfo;

import "./DangerZone.css";
import { useNavigate, useParams } from "react-router-dom";
import { deleteWorkspace as apiDeleteWorkspace } from "../../../api/workspaceApi";

const DangerZone = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const handleDelete = async () => {
    if (!id) {
      alert("Workspace ID not found.");
      return;
    }
    if (!window.confirm("Are you sure you want to delete this workspace? This action cannot be undone.")) {
      return;
    }
    try {
      await apiDeleteWorkspace(Number(id));
      alert("Workspace deleted successfully.");
      navigate("/workspaces");
    } catch (error) {
      console.error(error);
      alert("Failed to delete workspace. Please try again.");
    }
  };

  return (
    <div className="danger-zone">
      <h2>Danger Zone</h2>

      <p>Deleting a workspace cannot be undone.</p>

      <button onClick={handleDelete}>Delete Workspace</button>
    </div>
  );
};

export default DangerZone;

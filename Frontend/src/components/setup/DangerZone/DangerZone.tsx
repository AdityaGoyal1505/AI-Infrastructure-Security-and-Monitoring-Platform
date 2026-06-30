import { useParams, useNavigate } from "react-router-dom";
import { deleteWorkspace } from "../../api/workspaceApi";
import "./DangerZone.css";

const DangerZone = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this workspace? This action cannot be undone.")) {
      try {
        await deleteWorkspace(Number(id));
        navigate("/workspaces");
      } catch (error) {
        console.error("Failed to delete workspace", error);
        alert("Failed to delete workspace. Please try again.");
      }
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

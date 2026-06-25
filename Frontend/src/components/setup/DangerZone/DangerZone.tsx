import "./DangerZone.css";

const DangerZone = () => {
  const deleteWorkspace = () => {
    alert("Delete API will be added later");
  };

  return (
    <div className="danger-zone">
      <h2>Danger Zone</h2>

      <p>Deleting a workspace cannot be undone.</p>

      <button onClick={deleteWorkspace}>Delete Workspace</button>
    </div>
  );
};

export default DangerZone;

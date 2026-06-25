/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";

import "./CreateWorkspaceModal.css";

import api from "../../api/axios";

interface Props {
  onClose: () => void;
  onSuccess: () => void;
}

const CreateWorkspaceModal = ({ onClose, onSuccess }: Props) => {
  const [name, setName] = useState("");

  const [description, setDescription] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const createWorkspace = async () => {
    if (!name.trim()) {
      setError("Workspace name is required");

      return;
    }

    try {
      setLoading(true);

      setError("");

      await api.post(
        "/workspaces/",

        {
          name,

          description,
        },
      );

      onSuccess();
    } catch (err: any) {
      console.log(err);

      setError(err.response?.data?.detail || "Unable to create workspace");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-icon">⚡</div>

          <div>
            <h2>Create Workspace</h2>

            <p>Create an environment to monitor your infrastructure.</p>
          </div>
        </div>

        <div className="form-group">
          <label>Workspace Name</label>

          <input
            type="text"
            placeholder="Production Environment"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>
            Description
            <span>Optional</span>
          </label>

          <input
            type="text"
            placeholder="Main production servers"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        {error && <p className="error-text">{error}</p>}

        <div className="modal-actions">
          <button className="cancel-btn" onClick={onClose}>
            Cancel
          </button>

          <button
            className="create-btn"
            onClick={createWorkspace}
            disabled={loading}
          >
            {loading ? "Creating..." : "Create Workspace →"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateWorkspaceModal;

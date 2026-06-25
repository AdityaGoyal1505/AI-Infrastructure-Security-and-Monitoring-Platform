/* eslint-disable react-hooks/set-state-in-effect */
import { useEffect, useState } from "react";

import "./Workspaces.css";

import PublicHeader from "../../components/PublicHeader/PublicHeader";

import WorkspaceCard from "../../components/WorkspaceCard/WorkspaceCard";

import CreateWorkspaceModal from "../../components/CreateWorkspaceModal/CreateWorkspaceModal";

import api from "../../api/axios";

export interface Workspace {
  id: number;

  name: string;

  description: string;

  api_key: string;

  is_active: boolean;

  created_at: string;
}

const Workspaces = () => {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);

  const [loading, setLoading] = useState(true);

  const [showModal, setShowModal] = useState(false);

  const fetchWorkspaces = async () => {
    try {
      const response = await api.get("/workspaces/");

      setWorkspaces(response.data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkspaces();
  }, []);

  return (
    <div className="workspaces-page">
      <PublicHeader />

      <div className="workspaces-container">
        <div className="workspace-top">
          <div>
            <h1>Your Workspaces</h1>

            <p>Choose an environment to monitor and manage.</p>
          </div>

          <button
            className="new-workspace-btn"
            onClick={() => setShowModal(true)}
          >
            + New Workspace
          </button>
        </div>

        {loading ? (
          <div className="empty-state">Loading...</div>
        ) : workspaces.length === 0 ? (
          <div className="empty-state">
            <h2>No Workspaces Yet</h2>

            <p>
              Create your first workspace and start monitoring your
              infrastructure.
            </p>

            <button
              className="new-workspace-btn"
              onClick={() => setShowModal(true)}
            >
              Create Workspace
            </button>
          </div>
        ) : (
          <div className="workspace-grid">
            {workspaces.map((workspace) => (
              <WorkspaceCard key={workspace.id} workspace={workspace} />
            ))}
          </div>
        )}

        {showModal && (
          <CreateWorkspaceModal
            onClose={() => setShowModal(false)}
            onSuccess={() => {
              fetchWorkspaces();

              setShowModal(false);
            }}
          />
        )}
      </div>
    </div>
  );
};

export default Workspaces;

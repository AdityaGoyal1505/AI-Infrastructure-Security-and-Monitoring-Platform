import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import "./WorkspaceSetup.css";

import AgentStatus from "../../components/setup/AgentStatus/AgentStatus";
import AIFeatures from "../../components/setup/AIFeatures/AIFeatures";
import DangerZone from "../../components/setup/DangerZone/DangerZone";
import InfrastructureOverview from "../../components/setup/InfrastructureOverview/InfrastructureOverview";
import WorkspaceInfo from "../../components/setup/WorkspaceInfo/WorkspaceInfo";

import { getWorkspaceSetup } from "../../api/agentApi";

interface SetupData {
  workspace_id: number;

  workspace_name: string;

  api_key: string;

  download_url: string;
}

const Setup = () => {
  const { id } = useParams();

  const [setup, setSetup] = useState<SetupData | null>(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSetup = async () => {
      try {
        const response = await getWorkspaceSetup(Number(id));

        setSetup(response);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };

    fetchSetup();
  }, [id]);

  return (
    <div className="setup-page">
      <div className="setup-header">
        <h1>Setup</h1>

        <p>
          Configure your infrastructure, AI modules and monitoring preferences.
        </p>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <WorkspaceInfo />

          <AgentStatus setup={setup} />

          <AIFeatures />

          <InfrastructureOverview />

          <DangerZone />
        </>
      )}
    </div>
  );
};

export default Setup;

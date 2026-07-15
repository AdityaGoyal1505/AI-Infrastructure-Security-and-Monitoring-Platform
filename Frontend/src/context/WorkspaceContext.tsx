/* eslint-disable react-refresh/only-export-components */
/* eslint-disable react-hooks/set-state-in-effect */
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export interface Workspace {
  id: number | null;

  name: string;

  is_active: boolean;
}

interface WorkspaceContextType {
  workspace: Workspace;

  setWorkspace: (data: Workspace) => void;

  clearWorkspace: () => void;
}

const defaultWorkspace: Workspace = {
  id: null,

  name: "No Workspace",

  is_active: false,
};

const WorkspaceContext = createContext<WorkspaceContextType | null>(null);

interface WorkspaceProviderProps {
  children: ReactNode;
}

export const WorkspaceProvider = ({ children }: WorkspaceProviderProps) => {
  const [workspace, setWorkspaceState] = useState<Workspace>(defaultWorkspace);

  useEffect(() => {
    const stored = localStorage.getItem("selected_workspace");

    if (stored) {
      try {
        const parsed: Workspace = JSON.parse(stored);

        setWorkspaceState(parsed);
      } catch (error) {
        console.error(
          "Invalid workspace in localStorage",

          error,
        );

        localStorage.removeItem("selected_workspace");
      }
    }
  }, []);

  const setWorkspace = (data: Workspace) => {
    setWorkspaceState(data);

    localStorage.setItem(
      "selected_workspace",

      JSON.stringify(data),
    );
  };

  const clearWorkspace = () => {
    setWorkspaceState(defaultWorkspace);

    localStorage.removeItem("selected_workspace");
  };

  return (
    <WorkspaceContext.Provider
      value={{
        workspace,

        setWorkspace,

        clearWorkspace,
      }}
    >
      {children}
    </WorkspaceContext.Provider>
  );
};

export const useWorkspace = () => {
  const context = useContext(WorkspaceContext);

  if (!context) {
    throw new Error("useWorkspace must be used within WorkspaceProvider");
  }

  return context;
};

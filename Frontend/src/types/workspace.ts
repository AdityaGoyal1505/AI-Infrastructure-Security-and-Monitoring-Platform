export interface Workspace {
  id: number;
  name: string;
  description: string;
  api_key: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface WorkspaceSetup {
  workspace_id: number;
  workspace_name: string;
  api_key: string;
  download_url: string;
}

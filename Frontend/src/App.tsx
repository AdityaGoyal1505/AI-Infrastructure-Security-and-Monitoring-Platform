import AppRoutes from "./routes/AppRoutes";

import { AuthProvider } from "./context/AuthContext";

import { WorkspaceProvider } from "./context/WorkspaceContext";

function App() {
  return (
    <AuthProvider>
      <WorkspaceProvider>
        <AppRoutes />
      </WorkspaceProvider>
    </AuthProvider>
  );
}

export default App;

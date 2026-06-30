import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

const GuestRoute = ({ children }: Props) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    return <Navigate to="/workspaces" replace />;
  }

  return <>{children}</>;
};

export default GuestRoute;

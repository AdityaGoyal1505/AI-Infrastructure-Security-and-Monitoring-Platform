import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Auth from "../pages/Auth/Auth";
import Home from "../pages/Home/Home";
import Workspaces from "../pages/Workspaces/Workspaces";

import WorkspaceSetup from "../pages/WorkspaceSetup/WorkspaceSetup";

import Dashboard from "../pages/Dashboard/Dashboard";

import Insights from "../pages/Insights/Insights";

import Predictions from "../pages/Predictions/Predictions";

import Trends from "../pages/Trends/Trends";

import Profile from "../pages/Profile/Profile";

import MainLayout from "../components/layout/MainLayout/MainLayout";
import About from "../pages/About/About";
import Features from "../pages/Features/Features";
import ProtectedRoute from "./ProtectedRoute";
import GuestRoute from "./GuestRoute";

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Default route redirects to auth/guest route checking */}
        <Route path="/" element={<Navigate to="/home" replace />} />

        {/* Public Routes (Only for unauthenticated users) */}
        <Route
          path="/auth"
          element={
            <GuestRoute>
              <Auth />
            </GuestRoute>
          }
        />
        <Route path="/home" element={<Home />} />
        <Route path="/features" element={<Features />} />
        <Route path="/about" element={<About />} />

        {/* Protected Routes (Only for authenticated users) */}
        <Route
          path="/workspaces"
          element={
            <ProtectedRoute>
              <Workspaces />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/workspaces/:id/setup" element={<WorkspaceSetup />} />

          <Route path="/workspaces/:id/dashboard" element={<Dashboard />} />

          <Route path="/workspaces/:id/insights" element={<Insights />} />

          <Route path="/workspaces/:id/predictions" element={<Predictions />} />

          <Route path="/workspaces/:id/trends" element={<Trends />} />
        </Route>

        <Route path="*" element={<Navigate to="/home" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;

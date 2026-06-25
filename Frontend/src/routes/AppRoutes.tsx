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

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/auth" replace />} />

        <Route path="/auth" element={<Auth />} />

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
          path="/home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />

        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />

        <Route
          path="/features"
          element={
            <ProtectedRoute>
              <Features />
            </ProtectedRoute>
          }
        />

        <Route
          path="/about"
          element={
            <ProtectedRoute>
              <About />
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

        <Route path="*" element={<Navigate to="/auth" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;

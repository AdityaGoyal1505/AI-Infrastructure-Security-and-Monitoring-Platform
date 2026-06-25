import { Outlet } from "react-router-dom";
import Header from "../Header/Header.tsx";
import Sidebar from "../Sidebar/Sidebar.tsx";
import "./MainLayout.css";

const MainLayout = () => {
  return (
    <div className="main-layout">
      <Sidebar />
      <div className="main-content">
        <Header />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default MainLayout;

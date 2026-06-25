import Navbar from "../components/layout/Navbar.tsx";
import Sidebar from "../components/layout/Sidebar.tsx";

interface Props {
  children: React.ReactNode;
}

export default function MainLayout({ children }: Props) {
  return (
    <div className="layout">
      <Sidebar />

      <div className="content-wrapper">
        <Navbar />

        <main className="main-content">{children}</main>
      </div>
    </div>
  );
}

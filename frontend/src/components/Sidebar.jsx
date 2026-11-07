
import { NavLink } from "react-router-dom";

import {
  LayoutDashboard,
  Users,
  FileText,
  ShieldCheck,
  AlertTriangle,
  ClipboardList,
  History,
  Settings,
} from "lucide-react";

const menuItems = [
  { name: "Dashboard", path: "/", icon: LayoutDashboard },
  { name: "Customers", path: "/customers", icon: Users },
  { name: "Documents", path: "/documents", icon: FileText },
  { name: "Risk Management", path: "/risk-management", icon: ShieldCheck },
  { name: "Reviews", path: "/reviews", icon: ClipboardList },
  { name: "Alerts", path: "/alerts", icon: AlertTriangle },
  { name: "Audit Logs", path: "/audit-logs", icon: History },
];

function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="sidebar-brand">
        <ShieldCheck size={30} />
        <h2>KYC Secure</h2>
      </div>

      <p className="menu-label">MAIN MENU</p>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
  key={item.path}
  to={item.path}
  end={item.path === "/"}
  className={({ isActive }) =>
    isActive ? "menu-item active" : "menu-item"
  }
  onClick={() => console.log("Navigating to:", item.path)}
>
              <Icon size={20} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <Settings size={20} />
        <span>Settings</span>
      </div>

    </aside>
  );
}

export default Sidebar;

import { Search, Bell, UserCircle } from "lucide-react";

function Header() {
  return (
    <header className="header">
      <div>
        <h2>Dashboard Overview</h2>
        <p>Welcome to your KYC compliance workspace</p>
      </div>

      <div className="header-actions">
        <div className="search-box">
          <Search size={18} />
          <input placeholder="Search..." />
        </div>

        <Bell size={22} />

        <div className="profile">
          <UserCircle size={28} />
          <span>Admin</span>
        </div>
      </div>
    </header>
  );
}

export default Header;
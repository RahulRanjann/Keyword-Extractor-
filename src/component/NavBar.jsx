import React from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="flex justify-between items-center bg-gray-800 p-4 text-white">
      <div className="text-lg font-bold">Ads Tools</div>
      <ul className="flex space-x-6">
        <li>
          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive ? "text-yellow-400 font-bold border-b-2 border-yellow-400" : "text-white hover:text-yellow-200"
            }
          >
            Keyword Extractor
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/profitability"
            className={({ isActive }) =>
              isActive ? "text-yellow-400 font-bold border-b-2 border-yellow-400" : "text-white hover:text-yellow-200"
            }
          >
            Profitability
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

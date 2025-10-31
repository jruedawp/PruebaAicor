import React from "react";
import { Link, useNavigate } from "react-router-dom"; 
import { useAuth } from "../contexts/AuthContext";
import { FaShoppingCart, FaBox } from "react-icons/fa"; 

export default function Navbar() {
  const { user, cart, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();        // cerrar sesión
    navigate("/");   // redirigir al menú principal
  };

  return (
    <nav className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center shadow">
      {/* Logo */}
      <Link to="/" className="text-2xl font-bold tracking-wide">
        AicorShop
      </Link>

      {/* Menú */}
      <div className="flex items-center gap-6">
        {/* Productos */}
        <Link
          to="/"
          className="bg-blue-500 hover:bg-blue-700 px-4 py-2 rounded transition"
        >
          Productos
        </Link>

        {/* Carrito → solo si hay usuario */}
        {user && (
          <Link to="/cart" className="relative flex items-center">
            <FaShoppingCart size={22} />
            {cart.length > 0 && (
              <span className="absolute -top-2 -right-3 bg-red-500 text-xs px-2 py-0.5 rounded-full">
                {cart.length}
              </span>
            )}
          </Link>
        )}

        {/* Pedidos → solo si hay usuario */}
        {user && (
          <Link
            to="/orders"
            className="flex items-center gap-2 bg-indigo-500 hover:bg-indigo-600 px-4 py-2 rounded transition"
          >
            <FaBox />
            <span>Pedidos</span>
          </Link>
        )}

        {/* Login / Logout */}
        {user ? (
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded transition"
          >
            Cerrar sesión
          </button>
        ) : (
          <Link
            to="/login"
            className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded transition"
          >
            Iniciar sesión
          </Link>
        )}
      </div>
    </nav>
  );
}

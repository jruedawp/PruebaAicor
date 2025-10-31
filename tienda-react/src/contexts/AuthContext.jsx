import React, { createContext, useContext, useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode"; 
import api from "../services/api";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const u = localStorage.getItem("user");
    return u ? JSON.parse(u) : null;
  });
  const [access, setAccess] = useState(() => localStorage.getItem("access"));
  const [refresh, setRefresh] = useState(() => localStorage.getItem("refresh"));
  const [cart, setCart] = useState(() => {
    const c = localStorage.getItem("cart");
    return c ? JSON.parse(c) : [];
  });

  // Guardar en localStorage cuando cambian
  useEffect(() => {
    access ? localStorage.setItem("access", access) : localStorage.removeItem("access");
    refresh ? localStorage.setItem("refresh", refresh) : localStorage.removeItem("refresh");
    user ? localStorage.setItem("user", JSON.stringify(user)) : localStorage.removeItem("user");
  }, [access, refresh, user]);

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(cart));
  }, [cart]);

  // Login con tokens (desde backend)
  const loginWithTokens = (accessToken, refreshToken, userObj) => {
    setAccess(accessToken);
    setRefresh(refreshToken);
    setUser(userObj || (accessToken ? jwtDecode(accessToken) : null));
  };

  // Logout
  const logout = () => {
    setAccess(null);
    setRefresh(null);
    setUser(null);
    setCart([]);
    localStorage.clear();
  };

  // Carrito local
  const addToCartLocal = (product, qty = 1) => {
    setCart((prev) => {
      const idx = prev.findIndex((i) => i.product.id === product.id);
      if (idx >= 0) {
        const copy = [...prev];
        copy[idx].quantity += qty;
        return copy;
      }
      return [...prev, { product, quantity: qty }];
    });
  };

  const removeFromCartLocal = (productId) => {
    setCart((prev) => prev.filter((i) => i.product.id !== productId));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        access,
        refresh,
        cart,
        loginWithTokens,
        logout,
        addToCartLocal,
        removeFromCartLocal,
        setCart,
        setAccess,
        setRefresh,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

import React, { useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import { useNavigate } from "react-router-dom"; // 👈 importar navigate

// Para Google
import { GoogleLogin } from "@react-oauth/google";

export default function Login() {
  const { loginWithTokens } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate(); // 👈 inicializar navigate

  // 🔑 Login clásico con username/password
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/token/", { username, password });
      loginWithTokens(res.data.access, res.data.refresh, { username });
      navigate("/"); // 👈 redirigir al inicio
    } catch (err) {
      setError("Usuario o contraseña incorrectos");
    }
  };

  // 🔑 Login con Google
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const res = await api.post("/inicio/", {
        id_token: credentialResponse.credential,
      });
      loginWithTokens(res.data.access, res.data.refresh, res.data.user);
      navigate("/"); // 👈 redirigir al inicio
    } catch (err) {
      setError("Error al iniciar sesión con Google");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-lg shadow bg-white">
      <h2 className="text-2xl font-bold mb-4 text-center">Iniciar Sesión</h2>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      {/* Formulario clásico */}
      <form onSubmit={handleLogin} className="space-y-4">
        <input
          type="text"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full border px-3 py-2 rounded"
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border px-3 py-2 rounded"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Entrar
        </button>
      </form>

      <div className="my-6 text-center text-gray-500">o</div>

      {/* Botón de Google */}
      <div className="flex justify-center">
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => setError("Error en Google Login")}
        />
      </div>
    </div>
  );
}

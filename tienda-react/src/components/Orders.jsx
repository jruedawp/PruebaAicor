import { useEffect, useState } from "react";
import api from "../services/api";

export default function Orders() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("orders/").then(res => setOrders(res.data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">📦 Mis pedidos</h1>
      {orders.length === 0 ? (
        <p>No tienes pedidos todavía</p>
      ) : (
        <div className="space-y-4">
          {orders.map(order => (
            <div
              key={order.id}
              className="border p-4 rounded shadow flex justify-between items-center"
            >
              <div>
                <p className="font-semibold">Pedido #{order.id}</p>
                <p className="text-sm text-gray-600">
                  Fecha: {new Date(order.created_at).toLocaleString()}
                </p>
                <p className="text-sm text-gray-600">
                  Total: {order.total} €
                </p>
              </div>
              <span
                className={`px-3 py-1 rounded text-white ${
                  order.status === "PENDING"
                    ? "bg-yellow-500"
                    : order.status === "PAID"
                    ? "bg-green-600"
                    : "bg-red-600"
                }`}
              >
                {order.status_display}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

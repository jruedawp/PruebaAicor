import { useEffect, useState } from 'react';
import api from "../services/api";

export default function Cart() {
  const [items, setItems] = useState([]);
  const [showModal, setShowModal] = useState(false); 

  useEffect(() => {
    api.get('cart/').then(res => setItems(res.data));
  }, []);

  const deleteItem = (id) => {
    api.delete(`cart/${id}/`).then(() => {
      setItems(items.filter(i => i.id !== id));
    });
  };

  const checkout = () => {
    api.post('orders/').then(() => {
      setItems([]);
      setShowModal(true);
    });
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">🛒 Tu carrito</h1>
      {items.length === 0 ? (
        <p>El carrito está vacío</p>
      ) : (
        <>
          {items.map(i => (
            <div key={i.id} className="flex justify-between items-center border-b py-2">
              <span>{i.product.name} x{i.quantity}</span>
              <button onClick={() => deleteItem(i.id)} className="text-red-600">Eliminar</button>
            </div>
          ))}
          <button onClick={checkout} className="mt-4 bg-green-600 text-white px-4 py-2 rounded">
            Confirmar compra
          </button>
        </>
      )}

      {/* Modal de confirmación */}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-8 rounded shadow-lg text-center">
            <h2 className="text-2xl font-bold mb-4">Pedido confirmado</h2>
            <p className="mb-6">Tu compra se ha realizado con éxito.</p>
            <button
              onClick={() => setShowModal(false)}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

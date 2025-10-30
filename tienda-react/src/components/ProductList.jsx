import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    api.get('productos/')
      .then(res => setProducts(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">
      {products.map(p => (
        <div key={p.id} className="bg-white shadow-md rounded-lg p-4 text-center">
          <Link to={`/product/${p.id}`}>
            <img
              src={p.image_url || 'https://via.placeholder.com/150'}
              alt={p.name}
              className="w-full h-40 object-cover rounded hover:opacity-80 transition"
            />
            <h2 className="text-lg font-bold mt-2">{p.name}</h2>
          </Link>
          <p className="text-gray-600">{p.price} €</p>

          {user && (
            <button
              onClick={() => api.post('cart/', { product_id: p.id, quantity: 1 })}
              className="bg-blue-500 text-white mt-3 px-4 py-2 rounded"
            >
              Añadir
            </button>
          )}
        </div>
      ))}
    </div>
  );
}


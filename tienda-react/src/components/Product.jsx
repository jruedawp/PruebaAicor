import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../contexts/AuthContext";

export default function Product() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const { user } = useAuth();
  const navigate = useNavigate();

  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    api.get(`productos/${id}/`)
        .then(res => setProduct(res.data))
        .catch(console.error);
  }, [id]);

  if (!product) return <p className="text-center mt-10">Cargando producto...</p>;

  const increase = () => {
    if (quantity < product.stock) {
        setQuantity(q => q + 1);
    }
  };

  const decrease = () => setQuantity(q => (q > 1 ? q - 1 : 1));

  const handleAddToCart = async () => {
    try {
        await api.post("cart/", { product_id: product.id, quantity });
        const res = await api.get(`productos/${id}/`);
        setProduct(res.data);
        setQuantity(1); 
    } catch (err) {
        console.error("Error al añadir al carrito:", err);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-10 bg-white shadow-lg rounded-lg grid grid-cols-1 md:grid-cols-2 gap-12">
      {/* Imagen a la izquierda */}
      <div>
        <img
          src={product.image_url || "https://via.placeholder.com/600"}
          alt={product.name}
          className="w-full h-[500px] object-cover rounded"
        />
      </div>

      {/* Info a la derecha */}
      <div className="flex flex-col justify-between">
        <div>
          <h1 className="text-4xl font-bold mb-6">{product.name}</h1>
          <p className="text-gray-700 text-lg mb-8">{product.description}</p>
          <p className="text-3xl font-semibold text-blue-600 mb-4">{product.price} €</p>
          <p className="text-gray-500 mb-8">Stock disponible: {product.stock}</p>
        </div>

        <div className="flex gap-6 items-center">
          {user && (
            <>
              <div className="flex items-center gap-2">
                <button
                  onClick={decrease}
                  className="px-3 py-1 bg-gray-200 rounded text-lg"
                >
                  -
                </button>
                <span className="text-xl">{quantity}</span>
                <button
                  onClick={increase}
                  disabled={quantity >= product.stock}
                  className={`px-3 py-1 rounded text-lg ${
                    quantity >= product.stock
                      ? "bg-gray-300 cursor-not-allowed"
                      : "bg-gray-200"
                  }`}
                >
                  +
                </button>
              </div>
              <button
                onClick={handleAddToCart}
                disabled={product.stock === 0}
                className={`px-6 py-2 rounded text-lg text-white ${
                  product.stock === 0
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-blue-500 hover:bg-blue-600"
                }`}
              >
                {product.stock === 0 ? "Sin stock" : "Añadir al carrito"}
              </button>
            </>
          )}
          <button
            onClick={() => navigate(-1)}
            className="bg-gray-300 text-gray-800 px-8 py-3 rounded hover:bg-gray-400 transition text-lg"
          >
            Volver
          </button>
        </div>
      </div>
    </div>
  );
}

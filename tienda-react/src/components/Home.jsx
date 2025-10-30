export default function Home() {
  return (
    <div className="text-center py-16 bg-gradient-to-b from-blue-50 to-white min-h-screen">
      <h1 className="text-5xl font-extrabold text-blue-700 mb-6 drop-shadow">
        Bienvenido a <span className="text-indigo-600">AicorShop</span>
      </h1>


      <div className="flex justify-center gap-6 mb-16">
        <a
          href="/productos"
          className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg shadow-lg transition transform hover:scale-105"
        >
          Ver Productos
        </a>
        <a
          href="/login"
          className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-8 py-3 rounded-lg shadow-lg transition transform hover:scale-105"
        >
          Iniciar Sesión
        </a>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 px-6">
        <div className="p-6 border rounded-xl shadow hover:shadow-xl transition bg-white">
          <h2 className="text-xl font-semibold mb-2 text-blue-600">Productos</h2>
          <p className="text-gray-600">Explora lo más popular entre nuestros clientes.</p>
        </div>
        <div className="p-6 border rounded-xl shadow hover:shadow-xl transition bg-white">
          <h2 className="text-xl font-semibold mb-2 text-blue-600">Carrito Inteligente</h2>
          <p className="text-gray-600">Añade productos y gestiona cantidades fácilmente.</p>
        </div>
        <div className="p-6 border rounded-xl shadow hover:shadow-xl transition bg-white">
          <h2 className="text-xl font-semibold mb-2 text-blue-600">Pedidos Rápidos</h2>
          <p className="text-gray-600">Consulta tu historial y haz seguimiento en segundos.</p>
        </div>
      </div>
    </div>
  );
}

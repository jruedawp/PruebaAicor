import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProductList from './components/ProductList';
import CartPage from './components/Cart';
import OrdersPage from './components/Orders';
import Navbar from './components/Navbar';
import Login from './components/Login'; 
import Product from './components/Product';

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="container mx-auto p-4">
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/product/:id" element={<Product />} />   
        <Route path="/cart" element={<CartPage />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      </div>
    </BrowserRouter>
  );
}

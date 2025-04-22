import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';

import Home from './pages/Home';
import Components from './pages/Components';
import Configurator from './pages/Configurator';
import Cart from './pages/Cart';
import PCBuilds from './pages/PCBuilds';
import PCBuildDetail from './pages/PCBuildDetail';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import Checkout from './pages/Checkout';
import NotFound from './pages/NotFound';

function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/components" element={<Components />} />
        <Route path="/configurator" element={<Configurator />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/pcbuilds" element={<PCBuilds />} />
        <Route path="/pcbuilds/:id" element={<PCBuildDetail />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

export default App;
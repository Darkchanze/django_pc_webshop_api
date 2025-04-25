import { useEffect, useState } from 'react';
import { useCart } from '../context/CartContext';
import { Link } from 'react-router-dom';

const componentTypes = [
  'CPU', 'GPU', 'Motherboard', 'RAM', 'Storage', 'Power Supply', 'Case', 'Cooler'
];

const manufacturers = [
  'AMD', 'Intel', 'NVIDIA', 'Gigabyte', 'MSI', 'ASUS', 'Corsair', 'Samsung',
  'Crucial', 'Seagate', 'Western Digital', 'ZEBRONICS', 'Ant Esports',
  'Cooler Master', 'Deepcool', 'Frontech', 'Artis', 'ARS Infotech', 'Matrix',
  'Rubaintech', 'WEFLY', 'TECHON', 'Betaohm', 'GIGASTAR', 'ASRock'
];

function Components() {
  const [view, setView] = useState('components');
  const [components, setComponents] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [builds, setBuilds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [selectedManufacturers, setSelectedManufacturers] = useState([]);

  const { addToCart, cartItems } = useCart();

  const isInCart = (id, type = null) =>
    cartItems.some((item) => item.id === id && (!type || item.type === type));

  useEffect(() => {
    const fetchComponents = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/components/');
        if (!res.ok) throw new Error('Failed to fetch components');
        const data = await res.json();
        setComponents(data);
        setFiltered(data);
      } catch (err) {
        console.error(err);
        setError('Could not load components.');
      } finally {
        setLoading(false);
      }
    };

    const loadBuildsUnfiltered = async () => {
      const buildRes = await fetch('http://127.0.0.1:8000/pcs/');
      const buildData = await buildRes.json();
      const compRes = await fetch('http://127.0.0.1:8000/components/');
      const compData = await compRes.json();

      const getComponentPrice = (id) => {
        const comp = compData.find((c) => c.id === id);
        return comp ? parseFloat(comp.price) : 0;
      };

      const enriched = buildData.map((pc) => {
        const total = pc.components.reduce((sum, id) => sum + getComponentPrice(id), 0);
        return { ...pc, total };
      });

      setBuilds(enriched);
    };

    fetchComponents();
    loadBuildsUnfiltered();
  }, []);

  const toggleSelection = (value, list, setList) => {
    if (list.includes(value)) {
      setList(list.filter((item) => item !== value));
    } else {
      setList([...list, value]);
    }
  };

  const handleFilter = () => {
    let result = [...components];

    if (minPrice) {
      result = result.filter(comp => parseFloat(comp.price) >= parseFloat(minPrice));
    }

    if (maxPrice) {
      result = result.filter(comp => parseFloat(comp.price) <= parseFloat(maxPrice));
    }

    if (selectedTypes.length > 0) {
      result = result.filter(comp => selectedTypes.includes(comp.type));
    }

    if (selectedManufacturers.length > 0) {
      result = result.filter(comp => selectedManufacturers.includes(comp.manufacturer));
    }

    setFiltered(result);
  };

  const handleBuildFilter = async () => {
    const buildRes = await fetch('http://127.0.0.1:8000/pcs/');
    const buildData = await buildRes.json();
    const compRes = await fetch('http://127.0.0.1:8000/components/');
    const compData = await compRes.json();

    const getComponentPrice = (id) => {
      const comp = compData.find((c) => c.id === id);
      return comp ? parseFloat(comp.price) : 0;
    };

    const enriched = buildData.map((pc) => {
      const total = pc.components.reduce((sum, id) => sum + getComponentPrice(id), 0);
      return { ...pc, total };
    });

    const filteredBuilds = enriched.filter((build) => {
      if (minPrice && build.total < parseFloat(minPrice)) return false;
      if (maxPrice && build.total > parseFloat(maxPrice)) return false;
      return true;
    });

    setBuilds(filteredBuilds);
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-white px-4 py-12">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">Products</h1>

        <div className="flex justify-center mb-10 space-x-4">
          <button
            onClick={() => setView('components')}
            className={`px-4 py-2 rounded font-medium ${
              view === 'components'
                ? 'bg-cyan-500 text-black'
                : 'bg-[#1e293b] text-white hover:bg-[#2c3e50]'
            }`}
          >
            Components
          </button>
          <button
            onClick={() => setView('builds')}
            className={`px-4 py-2 rounded font-medium ${
              view === 'builds'
                ? 'bg-cyan-500 text-black'
                : 'bg-[#1e293b] text-white hover:bg-[#2c3e50]'
            }`}
          >
            PC Builds
          </button>
        </div>

        {view === 'builds' && (
          <>
            <div className="bg-[#1e293b] p-6 mb-10 rounded-xl shadow-xl">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="text-sm text-gray-400 block mb-1">Min Total Price (€)</label>
                  <input
                    type="number"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                    className="w-full p-2 bg-[#0f172a] border border-gray-700 rounded focus:ring-2 focus:ring-cyan-500"
                  />
                </div>
                <div>
                  <label className="text-sm text-gray-400 block mb-1">Max Total Price (€)</label>
                  <input
                    type="number"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                    className="w-full p-2 bg-[#0f172a] border border-gray-700 rounded focus:ring-2 focus:ring-cyan-500"
                  />
                </div>
                <div className="flex justify-end items-end">
                  <button
                    onClick={handleBuildFilter}
                    className="bg-cyan-500 hover:bg-cyan-400 text-black font-semibold px-6 py-2 rounded w-full md:w-auto"
                  >
                    Apply Filter
                  </button>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {builds.map((build) => {
                const inCart = isInCart(build.id, 'build');
                const buildCartItem = {
                  id: build.id,
                  name: build.name,
                  price: build.total,
                  quantity: 1,
                  type: 'build',
                };

                return (
                  <div
                    key={build.id}
                    className="bg-[#1e293b] p-6 rounded-xl shadow-md hover:shadow-lg transition flex flex-col justify-between"
                  >
                    <div>
                      <Link to={`/pcbuilds/${build.id}`}>
                        <h2 className="text-xl font-bold text-cyan-400 hover:underline mb-2">
                          {build.name}
                        </h2>
                      </Link>
                      <p className="text-gray-300 mb-1">ID: {build.id}</p>
                      <p className="text-white font-semibold mb-2">
                        Total: € {build.total.toFixed(2)}
                      </p>
                    </div>

                    <button
                      onClick={() => addToCart(buildCartItem)}
                      disabled={inCart}
                      className={`mt-4 py-2 px-4 rounded font-semibold transition ${
                        inCart
                          ? 'bg-green-600 text-white cursor-default'
                          : 'bg-cyan-500 hover:bg-cyan-400 text-black'
                      }`}
                    >
                      {inCart ? '✅ Added' : 'Add to Cart'}
                    </button>
                  </div>
                );
              })}
            </div>
          </>
        )}

        {view === 'components' && (
          <>
            <div className="bg-[#1e293b] p-6 mb-10 rounded-xl shadow-xl">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="text-sm text-gray-400 block mb-1">Min Price (€)</label>
                  <input
                    type="number"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                    className="w-full p-2 bg-[#0f172a] border border-gray-700 rounded focus:ring-2 focus:ring-cyan-500"
                  />
                </div>
                <div>
                  <label className="text-sm text-gray-400 block mb-1">Max Price (€)</label>
                  <input
                    type="number"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                    className="w-full p-2 bg-[#0f172a] border border-gray-700 rounded focus:ring-2 focus:ring-cyan-500"
                  />
                </div>
                <div className="flex justify-end items-end">
                  <button
                    onClick={handleFilter}
                    className="bg-cyan-500 hover:bg-cyan-400 text-black font-semibold px-6 py-2 rounded w-full md:w-auto"
                  >
                    Apply Filters
                  </button>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-cyan-400 font-semibold mb-2">Component Type</h3>
                  <div className="flex flex-wrap gap-3">
                    {componentTypes.map((type) => (
                      <label key={type} className="text-sm flex items-center gap-1">
                        <input
                          type="checkbox"
                          checked={selectedTypes.includes(type)}
                          onChange={() => toggleSelection(type, selectedTypes, setSelectedTypes)}
                          className="accent-cyan-500"
                        />
                        {type}
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-cyan-400 font-semibold mb-2">Manufacturer</h3>
                  <div className="flex flex-wrap gap-3">
                    {manufacturers.map((m) => (
                      <label key={m} className="text-sm flex items-center gap-1">
                        <input
                          type="checkbox"
                          checked={selectedManufacturers.includes(m)}
                          onChange={() =>
                            toggleSelection(m, selectedManufacturers, setSelectedManufacturers)
                          }
                          className="accent-cyan-500"
                        />
                        {m}
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {loading && <p className="text-center text-gray-300">Loading components...</p>}
            {error && <p className="text-center text-red-400">{error}</p>}

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {filtered.map((comp) => (
                <div
                  key={comp.id}
                  className="bg-[#1e293b] rounded-xl p-6 shadow-md hover:shadow-lg transition duration-300 flex flex-col justify-between"
                >
                  <div>
                    <h2 className="text-lg font-semibold text-cyan-400 mb-2">{comp.name}</h2>
                    <p className="text-sm text-gray-400 mb-1">
                      <strong>Type:</strong> {comp.type}
                    </p>
                    <p className="text-sm text-gray-400 mb-1">
                      <strong>Manufacturer:</strong> {comp.manufacturer}
                    </p>
                    <p className="text-lg text-cyan-300 font-bold mt-3">
                      € {parseFloat(comp.price).toFixed(2)}
                    </p>
                  </div>

                  <button
                    onClick={() => addToCart(comp)}
                    disabled={isInCart(comp.id)}
                    className={`mt-4 py-2 px-4 rounded font-semibold transition ${
                      isInCart(comp.id)
                        ? 'bg-green-600 text-white cursor-default'
                        : 'bg-cyan-500 hover:bg-cyan-400 text-black'
                    }`}
                  >
                    {isInCart(comp.id) ? '✅ Added' : 'Add to Cart'}
                  </button>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Components;
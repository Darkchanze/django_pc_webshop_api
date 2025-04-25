import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

function PCBuildDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [build, setBuild] = useState(null);
  const [components, setComponents] = useState([]);
  const [error, setError] = useState('');
  const { addToCart } = useCart();

  useEffect(() => {
    const fetchBuild = async () => {
      try {
        const pcRes = await fetch(`http://127.0.0.1:8000/pcs/${id}/`);
        const pcData = await pcRes.json();

        const compRes = await fetch(`http://127.0.0.1:8000/components/`);
        const compData = await compRes.json();

        const buildComponents = pcData.components.map((compId) =>
          compData.find((c) => c.id === compId)
        );

        const total = buildComponents.reduce((sum, c) => sum + parseFloat(c.price), 0);

        setBuild({ ...pcData, total });
        setComponents(buildComponents);
      } catch (err) {
        console.error(err);
        setError('Failed to load build.');
      }
    };

    fetchBuild();
  }, [id]);

  const handleAddToCart = () => {
    if (!build) return;
    addToCart({
      id: build.id,
      name: build.name,
      price: build.total,
      quantity: 1,
      type: 'build',
    });
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-white px-4 py-12">
      <div className="max-w-4xl mx-auto">

        <button
          onClick={() => navigate(-1)}
          className="text-cyan-400 hover:underline mb-6 text-sm"
        >
          ← Back to PC Builds
        </button>

        {error && <p className="text-red-400 text-center">{error}</p>}

        {build && (
          <div className="bg-[#1e293b] p-8 rounded-xl shadow-xl space-y-6">
            <h1 className="text-3xl font-bold text-cyan-400 text-center mb-6">
              {build.name}
            </h1>

            <ul className="space-y-4">
              {components.map((comp) => (
                <li
                  key={comp.id}
                  className="flex justify-between border-b border-gray-700 pb-3 text-sm sm:text-base"
                >
                  <span>{comp.name}</span>
                  <span className="text-cyan-300 whitespace-nowrap">€ {parseFloat(comp.price).toFixed(2)}</span>
                </li>
              ))}
            </ul>

            <div className="flex justify-between text-lg font-semibold border-t border-gray-700 pt-4">
              <span>Total Cost:</span>
              <span className="text-cyan-400">€ {build.total.toFixed(2)}</span>
            </div>

            <div className="pt-4">
              <button
                onClick={handleAddToCart}
                className="w-full py-3 bg-green-500 hover:bg-green-400 text-black font-semibold rounded transition"
              >
                Add PC to Cart
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PCBuildDetail;
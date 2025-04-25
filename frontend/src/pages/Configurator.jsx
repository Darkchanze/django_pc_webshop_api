import { useState } from 'react';
import { useCart } from '../context/CartContext';

function Configurator() {
  const [budget, setBudget] = useState('');
  const [requirements, setRequirements] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const { addToCart } = useCart(); // ✅ Zugriff auf globalen Warenkorb

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/recommend/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ budget, requirements }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(`Server Error: ${response.status}`);
      }

      try {
        const parsed = JSON.parse(data.recommendation);
        setResult(parsed);
      } catch (parseError) {
        console.error('Error parsing recommendation:', parseError);
        throw new Error('Invalid recommendation format from server.');
      }

    } catch (err) {
      console.error(err);
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = () => {
    if (!result) return;
    const cartItem = {
      id: result.name, // kann auch UUID oder result.id sein, wenn vorhanden
      name: result.name,
      price: result.total_cost,
      quantity: 1,
      type: 'build',
    };
    addToCart(cartItem);
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-white px-4 py-12">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">PC Configurator</h1>

        <form onSubmit={handleSubmit} className="bg-[#1e293b] p-8 rounded-xl shadow-xl space-y-6">
          <div>
            <label className="block text-sm text-gray-300 mb-1">Budget (EUR)</label>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-full p-4 rounded bg-[#0f172a] border border-gray-700 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              placeholder="Enter your budget"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-1">Requirements</label>
            <textarea
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
              className="w-full p-4 rounded bg-[#0f172a] border border-gray-700 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              rows={4}
              placeholder="e.g. Make me pc for working and video cutting."
              required
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 bg-cyan-500 hover:bg-cyan-400 text-black font-semibold rounded transition"
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate Recommendation'}
          </button>
        </form>

        {error && <p className="text-red-400 text-center mt-6">{error}</p>}

        {result && (
          <div className="mt-16 bg-[#1e293b] p-8 rounded-xl shadow-xl space-y-6">
            <h2 className="text-3xl font-bold text-cyan-400">{result.name}</h2>

            <ul className="space-y-4">
              {result.components.map((comp, index) => (
                <li
                  key={index}
                  className="flex justify-between gap-6 border-b border-gray-700 pb-3 text-sm sm:text-base"
                >
                  <span className="w-4/5">{comp.name}</span>
                  <span className="text-cyan-300 text-right min-w-[90px] whitespace-nowrap">
                    € {comp.price.toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>

            <div className="flex justify-between text-lg font-semibold border-t border-gray-700 pt-4">
              <span>Total Cost:</span>
              <span className="text-cyan-400">€ {result.total_cost.toFixed(2)}</span>
            </div>

            <div>
              <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-1">Justification</h3>
              <p className="text-gray-300">{result.justification}</p>
            </div>

            {/* Add to Cart Button */}
            <div className="pt-6">
              <button
                onClick={handleAddToCart}
                className="w-full py-3 bg-green-500 hover:bg-green-400 text-black font-semibold rounded transition"
              >
                Add this PC to Cart
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Configurator;
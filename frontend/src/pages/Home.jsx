import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="min-h-screen bg-[#0f172a] text-white flex flex-col items-center justify-center px-6">
      {/* Headline */}
      <h1 className="text-5xl font-bold mb-6 text-center">
        Welcome to Nico's PC Webshop
      </h1>

      {/* Description */}
      <p className="text-lg text-gray-300 mb-8 max-w-xl text-center">
        Build your dream PC with high-quality components – perfect for gaming, work, or both. Start now with our intelligent configurator!
      </p>

      {/* Call-to-Action */}
      <Link
        to="/configurator"
        className="bg-cyan-500 hover:bg-cyan-400 text-black font-bold py-3 px-6 rounded-lg shadow-lg transition"
      >
        Start Configuring
      </Link>

      {/* Feature Section */}
      <div className="mt-20 max-w-5xl w-full grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
        {[
          {
            icon: '🛠️',
            title: 'Fully customizable',
            text: 'Build your ideal PC from a wide range of premium parts.',
          },
          {
            icon: '⚡',
            title: 'Power you can trust',
            text: 'Our systems are optimized for performance and reliability.',
          },
          {
            icon: '🤖',
            title: 'AI-powered configuration',
            text: 'Our AI suggests a perfectly matched PC within seconds – tailored to your needs and budget.',
          },
        ].map((feature, idx) => (
          <div
            key={idx}
            className="bg-[#1e293b] p-6 rounded-xl shadow-md hover:shadow-lg transition-all"
          >
            <div className="text-4xl mb-4">{feature.icon}</div>
            <h3 className="text-xl font-semibold mb-2 text-cyan-400">
              {feature.title}
            </h3>
            <p className="text-gray-300 text-sm">{feature.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
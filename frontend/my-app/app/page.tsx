import Link from 'next/link';

export default function Home() {
  return (
    <div className="bg-gray-900 text-white">
      <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold">
          AI-preneur-in-a-box
        </div>
        <div className="flex items-center space-x-4">
          <Link href="/login">
            <span className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Login</span>
          </Link>
          <Link href="/register">
            <span className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Register</span>
          </Link>
        </div>
      </nav>

      <main className="container mx-auto px-6 py-16 text-center">
        <h1 className="text-5xl font-extrabold leading-tight mb-4">
          Your AI-First Co-pilot for Consulting
        </h1>
        <p className="text-xl text-gray-400 mb-8">
          AI-preneur-in-a-box helps independent consultants and boutique consulting firms win more business and deliver amazing results.
        </p>
        <div className="flex justify-center space-x-4">
          <Link href="/register">
            <span className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg text-lg">Get Started for Free</span>
          </Link>
        </div>
      </main>

      <section className="bg-gray-800 py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-12">Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gray-700 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-4">Automated Research Briefings</h3>
              <p className="text-gray-400">
                Generate comprehensive research briefings for your meetings in minutes, not hours.
              </p>
            </div>
            <div className="bg-gray-700 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-4">Lightweight CRM</h3>
              <p className="text-gray-400">
                Keep track of your clients and meetings with our simple and intuitive CRM.
              </p>
            </div>
            <div className="bg-gray-700 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-4">Integrations</h3>
              <p className="text-gray-400">
                Connect your calendar, notes, and other tools to streamline your workflow.
              </p>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-gray-900 py-8">
        <div className="container mx-auto px-6 text-center text-gray-500">
          &copy; 2025 AI-preneur-in-a-box. All rights reserved.
        </div>
      </footer>
    </div>
  );
}

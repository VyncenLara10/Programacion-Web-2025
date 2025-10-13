import { useState } from 'react';
import HideTab from './components/HideTab';
import RevealTab from './components/RevealTab';

function App() {
  const [activeTab, setActiveTab] = useState('hide');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              Mensajes secretos
            </h1>
          </div>

          <div className="bg-white rounded-lg shadow-xl overflow-hidden">
            <div className="flex border-b">
              <button
                onClick={() => setActiveTab('hide')}
                className={`flex-1 py-4 px-6 font-semibold transition-colors ${
                  activeTab === 'hide'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Escribe un mensaje secreto
              </button>
              <button
                onClick={() => setActiveTab('reveal')}
                className={`flex-1 py-4 px-6 font-semibold transition-colors ${
                  activeTab === 'reveal'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Revela un secreto
              </button>
            </div>

            <div className="p-8">
              {activeTab === 'hide' ? <HideTab /> : <RevealTab />}
            </div>
          </div>

          <div className="mt-8 text-center text-sm text-gray-600">
            <p>Todos los mensajes son cifrados y solo se pueden ver una vez</p>
            <p className="mt-2">Built with React + Vite</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
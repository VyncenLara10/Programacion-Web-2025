import { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

function RevealTab() {
  const [key, setKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [secret, setSecret] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const urlKey = params.get('key');
    if (urlKey) {
      setKey(urlKey);
    }
  }, []);

  const handleRevealSecret = async () => {
    if (!key.trim()) {
      setError('Introduzca su clave');
      return;
    }

    setLoading(true);
    setError(null);
    setSecret(null);

    try {
      const response = await fetch(`${API_URL}/api/reveal/${key}/`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error al revelar secreto');
      }

      setSecret(data.secret);
      setKey('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Introduzca clave secreta
        </label>
        <input
          type="text"
          value={key}
          onChange={(e) => setKey(e.target.value)}
          placeholder="Pegue su clave aca..."
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          disabled={loading}
        />
      </div>

      <button
        onClick={handleRevealSecret}
        disabled={loading || !key.trim()}
        className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Mostrando...' : 'Secreto revelado'}
      </button>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p className="font-semibold">Error</p>
          <p className="text-sm mt-1">{error}</p>
          <p className="text-xs mt-2 text-red-600">
            Clave inexistente o ya se uso
          </p>
        </div>
      )}

      {secret && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-3">
          <p className="text-blue-800 font-semibold"> Mensaje oculto:</p>
          <div className="bg-white border border-blue-300 rounded p-4">
            <p className="whitespace-pre-wrap break-words">{secret}</p>
          </div>
          <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
            <p className="text-yellow-800 text-sm">
               <strong>atencion:</strong> El mensaje sera borrado y no puede ser visto de nuevo
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default RevealTab;
import { useState } from 'react';
import axios from 'axios';

export default function WellnessBooster() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleBoost = async () => {
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const res = await axios.post('/api/v1/wellness/recommendations', {
        recommendation: {
          message: message || 'Take a short break and celebrate your progress!'
        }
      });
      setResult(res.data.message || 'Wellness boost sent!');
      setMessage('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send wellness boost.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-6 max-w-md mx-auto mt-8 text-center">
      <h2 className="text-xl font-bold mb-2">Wellness Booster 🚀</h2>
      <p className="mb-4 text-gray-600">Send a positive boost to your team or agents!</p>
      <textarea
        className="input w-full mb-4"
        rows={3}
        placeholder="Type a custom wellness message (optional)"
        value={message}
        onChange={e => setMessage(e.target.value)}
        disabled={loading}
      />
      <button
        className="btn btn-primary w-full mb-2"
        onClick={handleBoost}
        disabled={loading}
      >
        {loading ? 'Sending...' : 'Boost Wellness!'}
      </button>
      {result && <div className="text-green-600 mt-2">{result}</div>}
      {error && <div className="text-red-600 mt-2">{error}</div>}
    </div>
  );
} 
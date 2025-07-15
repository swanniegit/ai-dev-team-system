import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = '';

interface AgentWellnessResponse {
  agent_id: string;
  agent_name: string;
  mood_level: number;
  energy_level: number;
  stress_level: number;
  satisfaction_level: number;
  engagement_level: number;
  workload_level: number;
  notes?: string;
  response_time: string;
}

interface PollResults {
  total_agents: number;
  responses_received: number;
  average_mood: number;
  average_energy: number;
  average_stress: number;
  average_satisfaction: number;
  average_engagement: number;
  average_workload: number;
  agent_responses: AgentWellnessResponse[];
}

export default function WellnessPoll() {
  const [polling, setPolling] = useState(false);
  const [results, setResults] = useState<PollResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  const sendWellnessPoll = async () => {
    setPolling(true);
    setError(null);
    setResults(null);
    
    try {
      // Send poll to all agents
      const response = await axios.post(`${API_BASE_URL}/api/v1/wellness/poll`, {
        message: "Quick wellness check! How are you feeling right now?",
        timeout_seconds: 30
      });
      
      setResults(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send wellness poll.');
    } finally {
      setPolling(false);
    }
  };

  const getMoodColor = (level: number) => {
    if (level >= 8) return 'text-green-600';
    if (level >= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStressColor = (level: number) => {
    if (level <= 3) return 'text-green-600';
    if (level <= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="card p-6">
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold mb-2">Quick Wellness Poll 📊</h2>
        <p className="text-gray-600 mb-4">
          Send a quick wellness check to all agents and get real-time responses
        </p>
        
        <button
          onClick={sendWellnessPoll}
          disabled={polling}
          className="btn btn-primary"
        >
          {polling ? 'Polling Agents...' : 'Send Wellness Poll'}
        </button>
      </div>

      {error && (
        <div className="text-red-600 text-center mb-4">{error}</div>
      )}

      {polling && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Collecting responses from agents...</p>
        </div>
      )}

      {results && (
        <div className="space-y-6">
          {/* Poll Summary */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-semibold mb-2">Poll Results</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-500">Responses:</span>
                <span className="ml-1 font-medium">
                  {results.responses_received}/{results.total_agents}
                </span>
              </div>
              <div>
                <span className="text-gray-500">Avg Mood:</span>
                <span className={`ml-1 font-medium ${getMoodColor(results.average_mood)}`}>
                  {results.average_mood.toFixed(1)}/10
                </span>
              </div>
              <div>
                <span className="text-gray-500">Avg Energy:</span>
                <span className="ml-1 font-medium">
                  {results.average_energy.toFixed(1)}/10
                </span>
              </div>
              <div>
                <span className="text-gray-500">Avg Stress:</span>
                <span className={`ml-1 font-medium ${getStressColor(results.average_stress)}`}>
                  {results.average_stress.toFixed(1)}/10
                </span>
              </div>
            </div>
          </div>

          {/* Individual Agent Responses */}
          <div>
            <h3 className="font-semibold mb-4">Agent Responses</h3>
            <div className="grid gap-4">
              {results.agent_responses.map((agent) => (
                <div key={agent.agent_id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="font-medium">{agent.agent_name}</h4>
                      <p className="text-sm text-gray-500">
                        Responded at {new Date(agent.response_time).toLocaleTimeString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className={`font-medium ${getMoodColor(agent.mood_level)}`}>
                        Mood: {agent.mood_level}/10
                      </p>
                      <p className="text-sm text-gray-500">
                        Energy: {agent.energy_level}/10
                      </p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-3">
                    <div>
                      <span className="text-gray-500">Stress:</span>
                      <span className={`ml-1 font-medium ${getStressColor(agent.stress_level)}`}>
                        {agent.stress_level}/10
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Satisfaction:</span>
                      <span className="ml-1 font-medium">{agent.satisfaction_level}/10</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Engagement:</span>
                      <span className="ml-1 font-medium">{agent.engagement_level}/10</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Workload:</span>
                      <span className="ml-1 font-medium">{agent.workload_level}/10</span>
                    </div>
                  </div>

                  {agent.notes && (
                    <div className="bg-blue-50 rounded p-3">
                      <p className="text-sm text-blue-800">{agent.notes}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 
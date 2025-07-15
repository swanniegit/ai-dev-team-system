import { useState, useEffect } from 'react'
import { 
  HeartIcon,
  PlusIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/react/24/outline'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import WellnessBooster from '../components/WellnessBooster'
import WellnessPoll from '../components/WellnessPoll'

interface WellnessCheckin {
  id: string
  user_id: string
  agent_id: string
  mood_level: number
  energy_level: number
  stress_level: number
  satisfaction_level: number
  engagement_level: number
  workload_level: number
  notes?: string
  created_at: string
}

const mockCheckins: WellnessCheckin[] = [
  {
    id: '1',
    user_id: 'user-1',
    agent_id: 'dev-001',
    mood_level: 8,
    energy_level: 7,
    stress_level: 4,
    satisfaction_level: 8,
    engagement_level: 9,
    workload_level: 6,
    notes: 'Feeling good about the current sprint progress',
    created_at: '2024-01-15T10:00:00Z'
  },
  {
    id: '2',
    user_id: 'user-2',
    agent_id: 'qa-001',
    mood_level: 6,
    energy_level: 5,
    stress_level: 7,
    satisfaction_level: 6,
    engagement_level: 7,
    workload_level: 8,
    notes: 'A bit overwhelmed with the testing backlog',
    created_at: '2024-01-15T09:30:00Z'
  },
  {
    id: '3',
    user_id: 'user-3',
    agent_id: 'pm-001',
    mood_level: 9,
    energy_level: 8,
    stress_level: 3,
    satisfaction_level: 9,
    engagement_level: 8,
    workload_level: 5,
    created_at: '2024-01-15T09:00:00Z'
  }
]

const mockWellnessData = [
  { date: '2024-01-10', mood: 7.2, energy: 6.8, stress: 4.5 },
  { date: '2024-01-11', mood: 7.5, energy: 7.0, stress: 4.2 },
  { date: '2024-01-12', mood: 7.8, energy: 7.2, stress: 4.0 },
  { date: '2024-01-13', mood: 7.6, energy: 6.9, stress: 4.1 },
  { date: '2024-01-14', mood: 7.9, energy: 7.1, stress: 3.8 },
  { date: '2024-01-15', mood: 7.7, energy: 6.7, stress: 4.7 }
]

export default function Wellness() {
  const [checkins, setCheckins] = useState<WellnessCheckin[]>([])
  const [loading, setLoading] = useState(true)
  const [showCheckinForm, setShowCheckinForm] = useState(false)

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setCheckins(mockCheckins)
      setLoading(false)
    }, 1000)
  }, [])

  const averageMetrics = {
    mood: checkins.reduce((sum, c) => sum + c.mood_level, 0) / checkins.length || 0,
    energy: checkins.reduce((sum, c) => sum + c.energy_level, 0) / checkins.length || 0,
    stress: checkins.reduce((sum, c) => sum + c.stress_level, 0) / checkins.length || 0,
    satisfaction: checkins.reduce((sum, c) => sum + c.satisfaction_level, 0) / checkins.length || 0,
    engagement: checkins.reduce((sum, c) => sum + c.engagement_level, 0) / checkins.length || 0,
    workload: checkins.reduce((sum, c) => sum + c.workload_level, 0) / checkins.length || 0
  }

  const getMoodColor = (level: number) => {
    if (level >= 8) return 'text-green-600'
    if (level >= 6) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getStressColor = (level: number) => {
    if (level <= 3) return 'text-green-600'
    if (level <= 6) return 'text-yellow-600'
    return 'text-red-600'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Team Wellness</h1>
          <p className="text-gray-600">Monitor and improve team health and morale</p>
        </div>
        <button 
          onClick={() => setShowCheckinForm(true)}
          className="btn btn-primary"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          New Check-in
        </button>
      </div>

      {/* Wellness Booster */}
      <WellnessBooster />

      {/* Wellness Poll */}
      <WellnessPoll />

      {/* Wellness Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <HeartIcon className="h-8 w-8 text-pink-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Average Mood</p>
              <p className={`text-2xl font-bold ${getMoodColor(averageMetrics.mood)}`}>
                {averageMetrics.mood.toFixed(1)}/10
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <ArrowTrendingUpIcon className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Energy Level</p>
              <p className="text-2xl font-bold text-gray-900">
                {averageMetrics.energy.toFixed(1)}/10
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <ArrowTrendingDownIcon className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Stress Level</p>
              <p className={`text-2xl font-bold ${getStressColor(averageMetrics.stress)}`}>
                {averageMetrics.stress.toFixed(1)}/10
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Wellness Trends Chart */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Wellness Trends</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={mockWellnessData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="mood" stroke="#ec4899" strokeWidth={2} name="Mood" />
            <Line type="monotone" dataKey="energy" stroke="#10b981" strokeWidth={2} name="Energy" />
            <Line type="monotone" dataKey="stress" stroke="#ef4444" strokeWidth={2} name="Stress" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Check-ins */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Check-ins</h3>
        <div className="space-y-4">
          {checkins.map((checkin) => (
            <div key={checkin.id} className="border-b border-gray-200 pb-4 last:border-b-0">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="font-medium text-gray-900">Agent {checkin.agent_id}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(checkin.created_at).toLocaleString()}
                  </p>
                </div>
                <div className="text-right">
                  <p className={`font-medium ${getMoodColor(checkin.mood_level)}`}>
                    Mood: {checkin.mood_level}/10
                  </p>
                  <p className="text-sm text-gray-500">
                    Energy: {checkin.energy_level}/10
                  </p>
                </div>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Stress:</span>
                  <span className={`ml-1 font-medium ${getStressColor(checkin.stress_level)}`}>
                    {checkin.stress_level}/10
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">Satisfaction:</span>
                  <span className="ml-1 font-medium">{checkin.satisfaction_level}/10</span>
                </div>
                <div>
                  <span className="text-gray-500">Engagement:</span>
                  <span className="ml-1 font-medium">{checkin.engagement_level}/10</span>
                </div>
                <div>
                  <span className="text-gray-500">Workload:</span>
                  <span className="ml-1 font-medium">{checkin.workload_level}/10</span>
                </div>
              </div>

              {checkin.notes && (
                <div className="mt-2 p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-700">{checkin.notes}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Check-in Form Modal */}
      {showCheckinForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">New Wellness Check-in</h3>
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Mood Level (1-10)
                </label>
                <input type="range" min="1" max="10" className="w-full" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Energy Level (1-10)
                </label>
                <input type="range" min="1" max="10" className="w-full" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Stress Level (1-10)
                </label>
                <input type="range" min="1" max="10" className="w-full" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notes (optional)
                </label>
                <textarea className="input" rows={3} placeholder="How are you feeling today?"></textarea>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="btn btn-primary flex-1">
                  Submit Check-in
                </button>
                <button 
                  type="button" 
                  onClick={() => setShowCheckinForm(false)}
                  className="btn btn-secondary flex-1"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
} 
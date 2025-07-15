import { useState, useEffect } from 'react'
import { 
  UserGroupIcon, 
  ExclamationTriangleIcon, 
  CheckCircleIcon,
  HeartIcon
} from '@heroicons/react/24/outline'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

interface DashboardMetrics {
  totalAgents: number
  activeAgents: number
  totalIssues: number
  openIssues: number
  completedIssues: number
  averageWellness: number
  eventsToday: number
}

const mockMetrics: DashboardMetrics = {
  totalAgents: 8,
  activeAgents: 6,
  totalIssues: 45,
  openIssues: 12,
  completedIssues: 33,
  averageWellness: 7.8,
  eventsToday: 156
}

const mockWellnessData = [
  { name: 'Excellent', value: 15, color: '#22c55e' },
  { name: 'Good', value: 20, color: '#3b82f6' },
  { name: 'Neutral', value: 5, color: '#f59e0b' },
  { name: 'Poor', value: 2, color: '#ef4444' },
  { name: 'Terrible', value: 0, color: '#7f1d1d' }
]

const mockEventData = [
  { time: '00:00', events: 5 },
  { time: '04:00', events: 3 },
  { time: '08:00', events: 12 },
  { time: '12:00', events: 18 },
  { time: '16:00', events: 15 },
  { time: '20:00', events: 8 }
]

export default function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics>(mockMetrics)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setMetrics(mockMetrics)
      setLoading(false)
    }, 1000)
  }, [])

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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of your Agentic Agile System</p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <UserGroupIcon className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Active Agents</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.activeAgents}/{metrics.totalAgents}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <ExclamationTriangleIcon className="h-8 w-8 text-warning-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Open Issues</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.openIssues}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircleIcon className="h-8 w-8 text-success-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Completed</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.completedIssues}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <HeartIcon className="h-8 w-8 text-pink-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Team Wellness</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.averageWellness}/10</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Events Timeline */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Events Today</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockEventData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="events" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Wellness Distribution */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Wellness Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={mockWellnessData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {mockWellnessData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-4">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <div className="h-2 w-2 bg-success-500 rounded-full"></div>
            </div>
            <div className="flex-1">
              <p className="text-sm text-gray-900">PM Agent completed issue triage for #123</p>
              <p className="text-xs text-gray-500">2 minutes ago</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <div className="h-2 w-2 bg-primary-500 rounded-full"></div>
            </div>
            <div className="flex-1">
              <p className="text-sm text-gray-900">QA Agent started testing for PR #45</p>
              <p className="text-xs text-gray-500">5 minutes ago</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <div className="h-2 w-2 bg-warning-500 rounded-full"></div>
            </div>
            <div className="flex-1">
              <p className="text-sm text-gray-900">New issue created: "Fix login bug"</p>
              <p className="text-xs text-gray-500">10 minutes ago</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 
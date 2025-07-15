import { useState, useEffect } from 'react'
import { 
  PlayIcon, 
  PauseIcon, 
  Cog6ToothIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface Agent {
  id: string
  name: string
  type: string
  status: 'active' | 'inactive' | 'error'
  lastActivity: string
  tasksCompleted: number
  currentTask?: string
  health: number
}

const mockAgents: Agent[] = [
  {
    id: 'pm-001',
    name: 'Project Manager Agent',
    type: 'PM',
    status: 'active',
    lastActivity: '2 minutes ago',
    tasksCompleted: 45,
    currentTask: 'Triage new issues',
    health: 95
  },
  {
    id: 'po-001',
    name: 'Product Owner Agent',
    type: 'PO',
    status: 'active',
    lastActivity: '5 minutes ago',
    tasksCompleted: 32,
    currentTask: 'Review backlog',
    health: 88
  },
  {
    id: 'sm-001',
    name: 'Scrum Master Agent',
    type: 'SM',
    status: 'active',
    lastActivity: '1 minute ago',
    tasksCompleted: 28,
    currentTask: 'Facilitate daily standup',
    health: 92
  },
  {
    id: 'dev-001',
    name: 'Developer Agent',
    type: 'DEV',
    status: 'active',
    lastActivity: '30 seconds ago',
    tasksCompleted: 67,
    currentTask: 'Code review PR #123',
    health: 85
  },
  {
    id: 'qa-001',
    name: 'QA Agent',
    type: 'QA',
    status: 'active',
    lastActivity: '3 minutes ago',
    tasksCompleted: 41,
    currentTask: 'Run test suite',
    health: 90
  },
  {
    id: 'ar-001',
    name: 'Architect Agent',
    type: 'AR',
    status: 'inactive',
    lastActivity: '1 hour ago',
    tasksCompleted: 23,
    health: 78
  },
  {
    id: 'ad-001',
    name: 'Admin Agent',
    type: 'AD',
    status: 'error',
    lastActivity: '10 minutes ago',
    tasksCompleted: 15,
    health: 45
  },
  {
    id: 'mb-001',
    name: 'Morale Booster Agent',
    type: 'MB',
    status: 'active',
    lastActivity: '15 minutes ago',
    tasksCompleted: 12,
    currentTask: 'Send team encouragement',
    health: 96
  }
]

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null)

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setAgents(mockAgents)
      setLoading(false)
    }, 1000)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-success-100 text-success-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      case 'error':
        return 'bg-danger-100 text-danger-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getHealthColor = (health: number) => {
    if (health >= 90) return 'text-success-600'
    if (health >= 70) return 'text-warning-600'
    return 'text-danger-600'
  }

  const toggleAgentStatus = (agentId: string) => {
    setAgents(agents.map(agent => 
      agent.id === agentId 
        ? { ...agent, status: agent.status === 'active' ? 'inactive' : 'active' }
        : agent
    ))
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
          <h1 className="text-2xl font-bold text-gray-900">Agents</h1>
          <p className="text-gray-600">Manage your autonomous agents</p>
        </div>
        <button className="btn btn-primary">
          Add New Agent
        </button>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <div key={agent.id} className="card hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-medium text-gray-900">{agent.name}</h3>
                <p className="text-sm text-gray-500">Type: {agent.type}</p>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => toggleAgentStatus(agent.id)}
                  className="p-1 rounded-md hover:bg-gray-100"
                >
                  {agent.status === 'active' ? (
                    <PauseIcon className="h-4 w-4 text-gray-600" />
                  ) : (
                    <PlayIcon className="h-4 w-4 text-gray-600" />
                  )}
                </button>
                <button className="p-1 rounded-md hover:bg-gray-100">
                  <Cog6ToothIcon className="h-4 w-4 text-gray-600" />
                </button>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">Status</span>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(agent.status)}`}>
                  {agent.status}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">Health</span>
                <span className={`text-sm font-medium ${getHealthColor(agent.health)}`}>
                  {agent.health}%
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">Tasks Completed</span>
                <span className="text-sm font-medium text-gray-900">{agent.tasksCompleted}</span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">Last Activity</span>
                <span className="text-sm text-gray-900">{agent.lastActivity}</span>
              </div>

              {agent.currentTask && (
                <div className="pt-2 border-t border-gray-200">
                  <span className="text-sm text-gray-500">Current Task</span>
                  <p className="text-sm text-gray-900 mt-1">{agent.currentTask}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Agent Details Modal */}
      {selectedAgent && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">{selectedAgent.name}</h3>
            {/* Add detailed agent information here */}
            <button
              onClick={() => setSelectedAgent(null)}
              className="btn btn-secondary w-full"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
} 
import { useState, useEffect } from 'react'
import { 
  PlusIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  UserIcon
} from '@heroicons/react/24/outline'

interface Issue {
  id: string
  title: string
  description: string
  status: 'open' | 'in_progress' | 'review' | 'closed'
  priority: 'low' | 'medium' | 'high' | 'critical'
  assignee?: string
  created_at: string
  updated_at: string
  labels: string[]
}

const mockIssues: Issue[] = [
  {
    id: '123',
    title: 'Fix login authentication bug',
    description: 'Users are unable to log in with valid credentials',
    status: 'in_progress',
    priority: 'high',
    assignee: 'dev-001',
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-01-15T14:20:00Z',
    labels: ['bug', 'authentication', 'frontend']
  },
  {
    id: '124',
    title: 'Add user profile page',
    description: 'Create a new page for users to view and edit their profile information',
    status: 'open',
    priority: 'medium',
    created_at: '2024-01-15T11:00:00Z',
    updated_at: '2024-01-15T11:00:00Z',
    labels: ['feature', 'frontend', 'user-management']
  },
  {
    id: '125',
    title: 'Database connection timeout',
    description: 'Database connections are timing out under high load',
    status: 'review',
    priority: 'critical',
    assignee: 'ar-001',
    created_at: '2024-01-14T16:45:00Z',
    updated_at: '2024-01-15T09:15:00Z',
    labels: ['bug', 'database', 'performance']
  },
  {
    id: '126',
    title: 'Update API documentation',
    description: 'Documentation is outdated and needs to be updated with new endpoints',
    status: 'open',
    priority: 'low',
    created_at: '2024-01-14T14:20:00Z',
    updated_at: '2024-01-14T14:20:00Z',
    labels: ['documentation', 'api']
  },
  {
    id: '127',
    title: 'Implement search functionality',
    description: 'Add search capability to the main application',
    status: 'closed',
    priority: 'medium',
    assignee: 'dev-001',
    created_at: '2024-01-10T09:00:00Z',
    updated_at: '2024-01-15T12:30:00Z',
    labels: ['feature', 'search', 'frontend']
  }
]

export default function Issues() {
  const [issues, setIssues] = useState<Issue[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [priorityFilter, setPriorityFilter] = useState<string>('all')

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setIssues(mockIssues)
      setLoading(false)
    }, 1000)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open':
        return 'bg-blue-100 text-blue-800'
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800'
      case 'review':
        return 'bg-purple-100 text-purple-800'
      case 'closed':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'bg-red-100 text-red-800'
      case 'high':
        return 'bg-orange-100 text-orange-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredIssues = issues.filter(issue => {
    const matchesSearch = issue.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         issue.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || issue.status === statusFilter
    const matchesPriority = priorityFilter === 'all' || issue.priority === priorityFilter
    
    return matchesSearch && matchesStatus && matchesPriority
  })

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
          <h1 className="text-2xl font-bold text-gray-900">Issues</h1>
          <p className="text-gray-600">Manage project issues and tasks</p>
        </div>
        <button className="btn btn-primary">
          <PlusIcon className="h-4 w-4 mr-2" />
          New Issue
        </button>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search issues..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input"
            >
              <option value="all">All Status</option>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="review">Review</option>
              <option value="closed">Closed</option>
            </select>
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="input"
            >
              <option value="all">All Priority</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>
      </div>

      {/* Issues List */}
      <div className="space-y-4">
        {filteredIssues.map((issue) => (
          <div key={issue.id} className="card hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h3 className="text-lg font-medium text-gray-900">
                    #{issue.id} {issue.title}
                  </h3>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(issue.status)}`}>
                    {issue.status.replace('_', ' ')}
                  </span>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(issue.priority)}`}>
                    {issue.priority}
                  </span>
                </div>
                <p className="text-gray-600 mb-3">{issue.description}</p>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>Created: {new Date(issue.created_at).toLocaleDateString()}</span>
                  <span>Updated: {new Date(issue.updated_at).toLocaleDateString()}</span>
                  {issue.assignee && (
                    <span className="flex items-center">
                      <UserIcon className="h-4 w-4 mr-1" />
                      {issue.assignee}
                    </span>
                  )}
                </div>
                <div className="flex flex-wrap gap-1 mt-3">
                  {issue.labels.map((label) => (
                    <span
                      key={label}
                      className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full"
                    >
                      {label}
                    </span>
                  ))}
                </div>
              </div>
              <div className="flex space-x-2">
                <button className="p-2 text-gray-400 hover:text-gray-600">
                  <ExclamationTriangleIcon className="h-4 w-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-gray-600">
                  <CheckCircleIcon className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredIssues.length === 0 && (
        <div className="text-center py-12">
          <ExclamationTriangleIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No issues found</h3>
          <p className="text-gray-600">Try adjusting your search or filters</p>
        </div>
      )}
    </div>
  )
} 
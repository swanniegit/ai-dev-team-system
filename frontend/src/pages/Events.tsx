import { useState, useEffect } from 'react'
import { 
  BoltIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  ClockIcon,
  UserIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline'

interface Event {
  id: string
  event_type: string
  source: string
  target?: string
  data: any
  timestamp: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  priority: 'low' | 'medium' | 'high' | 'critical'
}

const mockEvents: Event[] = [
  {
    id: '1',
    event_type: 'issue_created',
    source: 'pm-001',
    data: { issue_id: '123', title: 'Fix login bug' },
    timestamp: '2024-01-15T14:30:00Z',
    status: 'completed',
    priority: 'high'
  },
  {
    id: '2',
    event_type: 'agent_status_changed',
    source: 'dev-001',
    target: 'api-hub',
    data: { status: 'active', health: 95 },
    timestamp: '2024-01-15T14:25:00Z',
    status: 'completed',
    priority: 'medium'
  },
  {
    id: '3',
    event_type: 'wellness_checkin',
    source: 'qa-001',
    data: { mood: 7, energy: 6, stress: 5 },
    timestamp: '2024-01-15T14:20:00Z',
    status: 'completed',
    priority: 'low'
  },
  {
    id: '4',
    event_type: 'code_review_requested',
    source: 'dev-001',
    target: 'qa-001',
    data: { pr_id: '45', files_changed: 12 },
    timestamp: '2024-01-15T14:15:00Z',
    status: 'processing',
    priority: 'medium'
  },
  {
    id: '5',
    event_type: 'sprint_planning_started',
    source: 'sm-001',
    data: { sprint_id: 'S24-01', participants: ['pm-001', 'po-001', 'dev-001'] },
    timestamp: '2024-01-15T14:10:00Z',
    status: 'completed',
    priority: 'high'
  },
  {
    id: '6',
    event_type: 'database_error',
    source: 'ar-001',
    data: { error: 'Connection timeout', retry_count: 3 },
    timestamp: '2024-01-15T14:05:00Z',
    status: 'failed',
    priority: 'critical'
  }
]

export default function Events() {
  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [typeFilter, setTypeFilter] = useState<string>('all')

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setEvents(mockEvents)
      setLoading(false)
    }, 1000)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'processing':
        return 'bg-blue-100 text-blue-800'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
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

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'issue_created':
      case 'issue_updated':
        return <ExclamationTriangleIcon className="h-4 w-4" />
      case 'agent_status_changed':
        return <UserIcon className="h-4 w-4" />
      case 'wellness_checkin':
        return <InformationCircleIcon className="h-4 w-4" />
      case 'code_review_requested':
      case 'code_review_completed':
        return <CheckCircleIcon className="h-4 w-4" />
      case 'database_error':
        return <ExclamationTriangleIcon className="h-4 w-4" />
      default:
        return <BoltIcon className="h-4 w-4" />
    }
  }

  const filteredEvents = events.filter(event => {
    const matchesSearch = event.event_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         event.source.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         JSON.stringify(event.data).toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || event.status === statusFilter
    const matchesType = typeFilter === 'all' || event.event_type === typeFilter
    
    return matchesSearch && matchesStatus && matchesType
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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Events</h1>
        <p className="text-gray-600">Monitor system events and agent communications</p>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search events..."
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
              <option value="pending">Pending</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
            </select>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="input"
            >
              <option value="all">All Types</option>
              <option value="issue_created">Issue Created</option>
              <option value="agent_status_changed">Agent Status</option>
              <option value="wellness_checkin">Wellness Check-in</option>
              <option value="code_review_requested">Code Review</option>
              <option value="database_error">Database Error</option>
            </select>
          </div>
        </div>
      </div>

      {/* Events List */}
      <div className="space-y-4">
        {filteredEvents.map((event) => (
          <div key={event.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 mt-1">
                <div className="p-2 bg-gray-100 rounded-lg">
                  {getEventIcon(event.event_type)}
                </div>
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <h3 className="text-lg font-medium text-gray-900">
                      {event.event_type.replace(/_/g, ' ')}
                    </h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(event.status)}`}>
                      {event.status}
                    </span>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(event.priority)}`}>
                      {event.priority}
                    </span>
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <ClockIcon className="h-4 w-4 mr-1" />
                    {new Date(event.timestamp).toLocaleString()}
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center space-x-4 text-sm">
                    <span className="text-gray-500">
                      <UserIcon className="h-4 w-4 inline mr-1" />
                      Source: {event.source}
                    </span>
                    {event.target && (
                      <span className="text-gray-500">
                        Target: {event.target}
                      </span>
                    )}
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-3">
                    <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                      {JSON.stringify(event.data, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredEvents.length === 0 && (
        <div className="text-center py-12">
          <BoltIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No events found</h3>
          <p className="text-gray-600">Try adjusting your search or filters</p>
        </div>
      )}

      {/* Event Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <BoltIcon className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Events</p>
              <p className="text-2xl font-bold text-gray-900">{events.length}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <CheckCircleIcon className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Completed</p>
              <p className="text-2xl font-bold text-gray-900">
                {events.filter(e => e.status === 'completed').length}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Failed</p>
              <p className="text-2xl font-bold text-gray-900">
                {events.filter(e => e.status === 'failed').length}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <ClockIcon className="h-8 w-8 text-yellow-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Processing</p>
              <p className="text-2xl font-bold text-gray-900">
                {events.filter(e => e.status === 'processing').length}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 
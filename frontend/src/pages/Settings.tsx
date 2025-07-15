import { useState } from 'react'
import { 
  Cog6ToothIcon,
  BellIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline'

interface Setting {
  id: string
  name: string
  description: string
  type: 'toggle' | 'input' | 'select'
  value: any
  category: string
}

const mockSettings: Setting[] = [
  {
    id: 'notifications_enabled',
    name: 'Enable Notifications',
    description: 'Receive notifications for important events',
    type: 'toggle',
    value: true,
    category: 'notifications'
  },
  {
    id: 'slack_integration',
    name: 'Slack Integration',
    description: 'Send notifications to Slack channels',
    type: 'toggle',
    value: true,
    category: 'notifications'
  },
  {
    id: 'auto_backup',
    name: 'Automatic Backups',
    description: 'Automatically backup system data',
    type: 'toggle',
    value: true,
    category: 'system'
  },
  {
    id: 'backup_frequency',
    name: 'Backup Frequency',
    description: 'How often to perform backups',
    type: 'select',
    value: 'daily',
    category: 'system'
  },
  {
    id: 'api_rate_limit',
    name: 'API Rate Limit',
    description: 'Maximum requests per minute',
    type: 'input',
    value: '1000',
    category: 'security'
  },
  {
    id: 'session_timeout',
    name: 'Session Timeout',
    description: 'Session timeout in minutes',
    type: 'input',
    value: '30',
    category: 'security'
  },
  {
    id: 'timezone',
    name: 'Timezone',
    description: 'System timezone',
    type: 'select',
    value: 'UTC',
    category: 'general'
  },
  {
    id: 'language',
    name: 'Language',
    description: 'Interface language',
    type: 'select',
    value: 'en',
    category: 'general'
  }
]

export default function Settings() {
  const [settings, setSettings] = useState<Setting[]>(mockSettings)
  const [activeTab, setActiveTab] = useState('general')

  const categories = [
    { id: 'general', name: 'General', icon: Cog6ToothIcon },
    { id: 'notifications', name: 'Notifications', icon: BellIcon },
    { id: 'security', name: 'Security', icon: ShieldCheckIcon },
    { id: 'system', name: 'System', icon: Cog6ToothIcon }
  ]

  const handleSettingChange = (settingId: string, value: any) => {
    setSettings(settings.map(setting => 
      setting.id === settingId ? { ...setting, value } : setting
    ))
  }

  const filteredSettings = settings.filter(setting => setting.category === activeTab)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Configure your Agentic Agile System</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar */}
        <div className="lg:w-64">
          <nav className="space-y-1">
            {categories.map((category) => {
              const Icon = category.icon
              return (
                <button
                  key={category.id}
                  onClick={() => setActiveTab(category.id)}
                  className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    activeTab === category.id
                      ? 'bg-primary-100 text-primary-900'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {category.name}
                </button>
              )
            })}
          </nav>
        </div>

        {/* Settings Content */}
        <div className="flex-1">
          <div className="card">
            <h2 className="text-lg font-medium text-gray-900 mb-6">
              {categories.find(c => c.id === activeTab)?.name} Settings
            </h2>
            
            <div className="space-y-6">
              {filteredSettings.map((setting) => (
                <div key={setting.id} className="border-b border-gray-200 pb-6 last:border-b-0">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-sm font-medium text-gray-900">{setting.name}</h3>
                      <p className="text-sm text-gray-500 mt-1">{setting.description}</p>
                    </div>
                    
                    <div className="ml-6">
                      {setting.type === 'toggle' && (
                        <button
                          onClick={() => handleSettingChange(setting.id, !setting.value)}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            setting.value ? 'bg-primary-600' : 'bg-gray-200'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              setting.value ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      )}
                      
                      {setting.type === 'input' && (
                        <input
                          type="text"
                          value={setting.value}
                          onChange={(e) => handleSettingChange(setting.id, e.target.value)}
                          className="input w-32"
                        />
                      )}
                      
                      {setting.type === 'select' && (
                        <select
                          value={setting.value}
                          onChange={(e) => handleSettingChange(setting.id, e.target.value)}
                          className="input w-32"
                        >
                          {setting.id === 'backup_frequency' && (
                            <>
                              <option value="hourly">Hourly</option>
                              <option value="daily">Daily</option>
                              <option value="weekly">Weekly</option>
                            </>
                          )}
                          {setting.id === 'timezone' && (
                            <>
                              <option value="UTC">UTC</option>
                              <option value="EST">EST</option>
                              <option value="PST">PST</option>
                              <option value="GMT">GMT</option>
                            </>
                          )}
                          {setting.id === 'language' && (
                            <>
                              <option value="en">English</option>
                              <option value="es">Spanish</option>
                              <option value="fr">French</option>
                              <option value="de">German</option>
                            </>
                          )}
                        </select>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Save Button */}
          <div className="mt-6 flex justify-end">
            <button className="btn btn-primary">
              Save Changes
            </button>
          </div>
        </div>
      </div>

      {/* System Information */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">System Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Version</p>
            <p className="text-sm font-medium text-gray-900">1.0.0</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Last Updated</p>
            <p className="text-sm font-medium text-gray-900">2024-01-15</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Database Status</p>
            <p className="text-sm font-medium text-green-600">Connected</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Redis Status</p>
            <p className="text-sm font-medium text-green-600">Connected</p>
          </div>
        </div>
      </div>
    </div>
  )
} 
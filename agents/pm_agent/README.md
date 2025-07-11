# 🤖 PM Agent (Project Manager Agent)

The PM Agent is an autonomous agent that manages project workflows in the Agentic Agile System. It automatically triages issues, assigns them to appropriate agents, and monitors project progress.

## 🚀 Features

- **Automatic Issue Triage**: Analyzes issues and determines priority, type, and assignment
- **Smart Assignment**: Routes issues to appropriate agent types based on content
- **Real-time Monitoring**: Continuously monitors for new issues and project status
- **Heartbeat System**: Maintains connection with the API hub
- **Configurable Rules**: Customizable triage rules and assignment logic

## 📋 Capabilities

- Issue triage and categorization
- Sprint planning assistance
- Project monitoring and reporting
- Stakeholder communication coordination

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   cd agents/pm_agent
   pip install -r requirements.txt
   ```

2. **Configure Environment** (optional):
   ```bash
   # Copy and edit environment variables
   cp ../../env.example .env
   ```

## 🚀 Usage

### Quick Start

1. **Ensure API Hub is Running**:
   ```bash
   # From the root directory
   docker-compose up -d
   ```

2. **Test the Agent**:
   ```bash
   python test_agent.py
   ```

3. **Run the Agent**:
   ```bash
   python run.py
   ```

### Configuration

The agent can be configured via environment variables:

```bash
# Agent Identity
PM_AGENT_NAME=PM Agent Alpha
API_BASE_URL=http://localhost:8000

# Behavior Settings
HEARTBEAT_INTERVAL=60
ISSUE_CHECK_INTERVAL=300
```

## 🔧 Architecture

```
pm_agent/
├── __init__.py          # Package initialization
├── config.py           # Configuration management
├── api_client.py       # API communication client
├── issue_triage.py     # Issue analysis and triage logic
├── main.py            # Main agent application
├── run.py             # Entry point script
├── test_agent.py      # Test suite
├── requirements.txt   # Dependencies
└── README.md         # This file
```

## 📊 Issue Triage Logic

The PM Agent uses intelligent analysis to categorize issues:

### Priority Detection
- **Critical**: Contains keywords like "urgent", "blocker", "production", "security"
- **High**: Contains keywords like "important", "deadline", "customer", "feature"
- **Medium**: Default priority for most issues
- **Low**: Contains keywords like "documentation", "cleanup", "refactor"

### Issue Type Detection
- **Bug**: Contains "bug", "error", "crash", "broken", "fails"
- **Feature**: Contains "feature", "new", "add", "implement"
- **Story**: Contains "story", "user story", "as a user"
- **Epic**: Contains "epic", "large", "major"
- **Task**: Default type for general work

### Assignment Logic
- **Bugs** → QA Engineer
- **Features** → Product Owner
- **Stories** → Product Owner
- **Tasks** → Developer
- **Epics** → Product Owner

## 🔄 Workflow

1. **Registration**: Agent registers with the API hub
2. **Monitoring**: Continuously checks for new issues
3. **Triage**: Analyzes each issue and determines properties
4. **Update**: Updates issues with triage results
5. **Assignment**: Triggers appropriate agents (future feature)
6. **Heartbeat**: Maintains connection status

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_agent.py
```

This will test:
- API connection
- Agent registration
- Issue triage logic
- Issue creation
- Heartbeat functionality

## 📈 Monitoring

The agent provides real-time statistics:

- Issues processed
- Heartbeats sent
- Uptime
- Current status

## 🔗 Integration

The PM Agent integrates with:

- **API Hub**: Main communication point
- **Other Agents**: Can trigger and coordinate with other agent types
- **Issue Management**: Creates and updates issues
- **Project Tracking**: Monitors project progress

## 🚧 Future Enhancements

- [ ] Agent triggering and coordination
- [ ] Sprint planning automation
- [ ] Stakeholder communication
- [ ] Advanced analytics and reporting
- [ ] Machine learning for better triage
- [ ] Integration with external tools (Jira, GitHub, etc.)

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**:
   - Ensure the API hub is running: `docker-compose up -d`
   - Check the API URL in configuration

2. **Agent Registration Failed**:
   - Verify API hub health: `curl http://localhost:8000/health`
   - Check network connectivity

3. **Issues Not Processing**:
   - Verify agent is running and sending heartbeats
   - Check issue status in the API

### Logs

The agent provides detailed logging. Check the console output for:
- Connection status
- Issue processing details
- Error messages
- Performance metrics

## 📞 Support

For issues and questions:
1. Check the main project README
2. Review the API documentation
3. Check agent logs for error details
4. Verify configuration settings 
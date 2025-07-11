# 🎯 Product Owner (PO) Agent

A Product Owner agent for the Agentic Agile System that automates story creation, backlog management, and sprint planning using Claude 3.7 Sonnet for intelligent decision-making.

## 🚀 Features

### **20-Behavior Checklist Implementation**
The PO agent implements a configurable 20-behavior checklist that companies can enable/disable:

#### **Core Story Management** ✅
- [x] **Story Creation**: Generate user stories from feature requests using Claude 3.7 Sonnet
- [x] **Acceptance Criteria**: Write detailed acceptance criteria with AI assistance
- [x] **Story Pointing**: Estimate story points using Fibonacci sequence
- [x] **Priority Ranking**: Rank stories by business value and impact
- [x] **Dependency Mapping**: Identify and track story dependencies

#### **Planning & Strategy** ✅
- [x] **Sprint Planning**: Suggest optimal stories for next sprint
- [x] **Backlog Grooming**: Keep backlog clean, prioritized, and up-to-date
- [ ] **Release Planning**: Plan feature releases and milestones
- [ ] **Roadmap Creation**: Generate product roadmap with AI insights
- [ ] **Capacity Planning**: Estimate team capacity for sprints

#### **Business Intelligence** ✅
- [x] **Business Value Scoring**: Score stories 1-10 on business impact
- [ ] **ROI Calculation**: Estimate return on investment for features
- [ ] **Market Analysis**: Consider market timing and trends
- [ ] **Competitive Analysis**: Analyze competitor features and positioning
- [ ] **Customer Feedback Integration**: Link stories to customer insights

#### **Quality & Compliance** ✅
- [x] **Definition of Ready**: Ensure stories meet DoR criteria
- [x] **Definition of Done**: Track DoD completion and quality gates
- [x] **Risk Assessment**: Flag high-risk stories and dependencies
- [ ] **Technical Debt Tracking**: Identify and prioritize tech debt
- [ ] **Compliance Checking**: Ensure regulatory and security compliance

## 🤖 Claude 3.7 Sonnet Integration

The PO agent integrates with Claude 3.7 Sonnet for intelligent decision-making:

- **Story Creation**: AI-powered user story generation from feature requests
- **Acceptance Criteria**: Intelligent acceptance criteria writing
- **Story Pointing**: AI-based story point estimation using Fibonacci
- **Priority Ranking**: Smart backlog prioritization
- **Fallback Logic**: Works without Claude API key (graceful degradation)

## 🐳 Docker Deployment

### **Quick Start**
```bash
# Navigate to PO agent directory
cd agents/po

# Build and run the agent
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f po-agent
```

### **Environment Variables**
```bash
# Required
API_BASE_URL=http://host.docker.internal:8000

# Optional (for Claude integration)
CLAUDE_API_KEY=your_claude_api_key_here

# Agent Configuration
PO_AGENT_NAME=Product Owner Agent
HEARTBEAT_INTERVAL=60
STORY_CHECK_INTERVAL=300
```

### **Testing**
```bash
# Run test container
docker-compose run --rm po-agent-test

# Or test with Python directly
python main.py
```

## ⚙️ Configuration

### **Behavior Configuration**
Edit `config.py` to enable/disable behaviors:

```python
enabled_behaviors = {
    "story_creation": True,
    "acceptance_criteria": True,
    "story_pointing": True,
    "priority_ranking": True,
    "dependency_mapping": True,
    "sprint_planning": True,
    "backlog_grooming": True,
    # ... more behaviors
}
```

### **Claude Integration Settings**
```python
claude_model = "claude-3-5-sonnet-20241022"
claude_max_tokens = 4000
claude_temperature = 0.7
```

## 📊 Metrics & Monitoring

The PO agent tracks detailed metrics:

- **Stories Created**: Number of user stories generated
- **Acceptance Criteria Written**: Number of acceptance criteria sets created
- **Story Points Estimated**: Total story points estimated
- **Stories Prioritized**: Number of stories prioritized
- **Backlog Items Processed**: Number of backlog items groomed
- **Behaviors Enabled**: Number of active behaviors
- **Claude Integration**: Whether Claude API is configured

## 🔧 Development

### **Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export API_BASE_URL=http://localhost:8000
export CLAUDE_API_KEY=your_key_here

# Run agent
python main.py
```

### **File Structure**
```
agents/po/
├── main.py              # Main agent application
├── config.py            # Configuration and behavior settings
├── claude_client.py     # Claude 3.7 Sonnet integration
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker container definition
├── docker-compose.yml  # Docker Compose configuration
└── README.md           # This file
```

## 🔗 Integration

The PO agent integrates with:

- **API Hub**: Registers, sends heartbeats, creates/updates issues
- **PM Agent**: Receives triaged issues for story creation
- **Claude 3.7 Sonnet**: AI-powered decision making
- **External Systems**: Feature request sources (configurable)

## 🚀 Next Steps

1. **Enable More Behaviors**: Configure additional behaviors from the 20-behavior checklist
2. **Customize Prompts**: Modify Claude prompts for your organization's needs
3. **Add External Integrations**: Connect to Jira, GitHub Issues, or customer feedback systems
4. **Scale**: Deploy multiple PO agents for different products/teams

## 📝 License

Part of the Agentic Agile System - MIT License 
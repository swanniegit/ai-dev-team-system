# 🏅 Scrum Master (SM) Agent

A Scrum Master agent for the Agentic Agile System that automates ceremony facilitation, impediment removal, and team coaching using Claude 3.7 Sonnet for intelligent decision-making.

## 🚀 Features

### **20-Behavior Checklist Implementation**
The SM agent implements a configurable 20-behavior checklist that companies can enable/disable:

#### **Ceremony Management** ✅
- [x] **Sprint Planning Facilitation**
- [x] **Daily Standup Coordination**
- [x] **Sprint Review Organization**
- [x] **Retrospective Facilitation**
- [x] **Backlog Refinement**

#### **Team Coaching** ✅
- [x] **Agile Coaching**
- [x] **Team Building**
- [x] **Conflict Resolution**
- [ ] **Skill Development**
- [ ] **Mentoring**

#### **Process Optimization** ✅
- [x] **Velocity Tracking**
- [x] **Burndown Monitoring**
- [x] **Impediment Removal**
- [x] **Process Improvement**
- [x] **Metrics Analysis**

#### **Communication & Coordination** ✅
- [x] **Stakeholder Communication**
- [ ] **Cross-team Coordination**
- [ ] **Escalation Management**
- [x] **Documentation**
- [ ] **Training Coordination**

## 🤖 Claude 3.7 Sonnet Integration

The SM agent integrates with Claude 3.7 Sonnet for intelligent ceremony facilitation and team coaching.

## 🐳 Docker Deployment

### **Quick Start**
```bash
cd agents/sm
docker-compose up -d
docker-compose ps
docker-compose logs -f sm-agent
```

### **Environment Variables**
```bash
API_BASE_URL=http://host.docker.internal:8000
CLAUDE_API_KEY=your_claude_api_key_here
SM_AGENT_NAME=Scrum Master Agent
HEARTBEAT_INTERVAL=60
CEREMONY_CHECK_INTERVAL=300
```

## ⚙️ Configuration

Edit `config.py` to enable/disable behaviors and set Claude integration settings.

## 📊 Metrics & Monitoring

The SM agent tracks:
- Ceremonies facilitated
- Impediments removed
- Velocity tracked
- Retrospectives led
- Behaviors enabled
- Claude integration status

## 🔧 Development

```bash
pip install -r requirements.txt
python main.py
```

## 🔗 Integration

- **API Hub**: Registers, sends heartbeats, updates ceremonies/impediments
- **Claude 3.7 Sonnet**: AI-powered facilitation and coaching

## 🚀 Next Steps

- Enable more behaviors from the checklist
- Customize Claude prompts
- Integrate with team calendars or chat tools

## 📝 License

Part of the Agentic Agile System - MIT License 
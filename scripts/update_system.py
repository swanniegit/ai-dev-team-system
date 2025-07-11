#!/usr/bin/env python3
"""
Agentic Agile System Update Script
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import requests

class SystemUpdater:
    """Agentic Agile System updater"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "recommendations": []
        }
    
    def check_agents(self):
        """Check all agent implementations"""
        print("🔍 Checking agent implementations...")
        
        expected_agents = [
            "pm_agent", "po", "sm", "dev", "qa", "ar", "ad", "mb"
        ]
        
        agent_status = {}
        for agent in expected_agents:
            agent_path = self.project_root / "agents" / agent
            if agent_path.exists():
                # Check for required files
                required_files = ["main.py", "config.py", "requirements.txt"]
                missing_files = []
                
                for file in required_files:
                    if not (agent_path / file).exists():
                        missing_files.append(file)
                
                if missing_files:
                    agent_status[agent] = {
                        "status": "incomplete",
                        "missing_files": missing_files
                    }
                else:
                    agent_status[agent] = {
                        "status": "complete",
                        "missing_files": []
                    }
            else:
                agent_status[agent] = {
                    "status": "missing",
                    "missing_files": ["entire_agent"]
                }
        
        self.report["checks"]["agents"] = agent_status
        
        # Count status
        complete = sum(1 for status in agent_status.values() if status["status"] == "complete")
        incomplete = sum(1 for status in agent_status.values() if status["status"] == "incomplete")
        missing = sum(1 for status in agent_status.values() if status["status"] == "missing")
        
        print(f"✅ Complete: {complete}/8 agents")
        print(f"⚠️  Incomplete: {incomplete}/8 agents")
        print(f"❌ Missing: {missing}/8 agents")
        
        if incomplete > 0 or missing > 0:
            self.report["recommendations"].append("Complete missing agent implementations")
    
    def check_documentation(self):
        """Check documentation completeness"""
        print("📚 Checking documentation...")
        
        required_docs = [
            "README.md",
            "SETUP.md", 
            "DEPLOYMENT_SUMMARY.md",
            "AGENT_COMPLETION_SUMMARY.md",
            "MEMORY_SYSTEM_SUMMARY.md",
            "FUNCTIONAL_TECHNICAL_SPEC.md"
        ]
        
        doc_status = {}
        for doc in required_docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                size = doc_path.stat().st_size
                doc_status[doc] = {
                    "status": "present",
                    "size_bytes": size,
                    "size_kb": round(size / 1024, 2)
                }
            else:
                doc_status[doc] = {
                    "status": "missing",
                    "size_bytes": 0,
                    "size_kb": 0
                }
        
        self.report["checks"]["documentation"] = doc_status
        
        present = sum(1 for status in doc_status.values() if status["status"] == "present")
        missing = sum(1 for status in doc_status.values() if status["status"] == "missing")
        
        print(f"✅ Present: {present}/{len(required_docs)} documents")
        print(f"❌ Missing: {missing}/{len(required_docs)} documents")
        
        if missing > 0:
            self.report["recommendations"].append("Create missing documentation")
    
    def check_infrastructure(self):
        """Check infrastructure files"""
        print("🏗️ Checking infrastructure...")
        
        infra_files = {
            "docker-compose.yml": "Docker Compose",
            "Dockerfile": "Docker",
            "k8s/": "Kubernetes",
            ".github/workflows/": "GitHub Actions"
        }
        
        infra_status = {}
        for file_path, description in infra_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                if full_path.is_dir():
                    # Count files in directory
                    file_count = len(list(full_path.rglob("*")))
                    infra_status[file_path] = {
                        "status": "present",
                        "type": "directory",
                        "file_count": file_count
                    }
                else:
                    size = full_path.stat().st_size
                    infra_status[file_path] = {
                        "status": "present",
                        "type": "file",
                        "size_bytes": size
                    }
            else:
                infra_status[file_path] = {
                    "status": "missing",
                    "type": "unknown"
                }
        
        self.report["checks"]["infrastructure"] = infra_status
        
        present = sum(1 for status in infra_status.values() if status["status"] == "present")
        missing = sum(1 for status in infra_status.values() if status["status"] == "missing")
        
        print(f"✅ Present: {present}/{len(infra_files)} infrastructure components")
        print(f"❌ Missing: {missing}/{len(infra_files)} infrastructure components")
        
        if missing > 0:
            self.report["recommendations"].append("Set up missing infrastructure")
    
    def check_dependencies(self):
        """Check for dependency updates"""
        print("📦 Checking dependencies...")
        
        try:
            # Check pip for outdated packages
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                outdated = json.loads(result.stdout)
                self.report["checks"]["dependencies"] = {
                    "status": "checked",
                    "outdated_count": len(outdated),
                    "outdated_packages": outdated
                }
                
                print(f"📦 Outdated packages: {len(outdated)}")
                
                if len(outdated) > 0:
                    self.report["recommendations"].append(f"Update {len(outdated)} outdated dependencies")
                    
                    # Show top 5 outdated packages
                    for pkg in outdated[:5]:
                        print(f"  - {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
            else:
                self.report["checks"]["dependencies"] = {
                    "status": "error",
                    "error": result.stderr
                }
                print("❌ Error checking dependencies")
                
        except Exception as e:
            self.report["checks"]["dependencies"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Error checking dependencies: {e}")
    
    def check_security(self):
        """Run security checks"""
        print("🔒 Running security checks...")
        
        try:
            # Try to run bandit if available
            result = subprocess.run(
                [sys.executable, "-m", "bandit", "-r", ".", "-f", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                security_issues = json.loads(result.stdout)
                issue_count = len(security_issues.get("results", []))
                
                self.report["checks"]["security"] = {
                    "status": "checked",
                    "issues_count": issue_count,
                    "issues": security_issues.get("results", [])
                }
                
                print(f"🔒 Security issues found: {issue_count}")
                
                if issue_count > 0:
                    self.report["recommendations"].append(f"Fix {issue_count} security issues")
            else:
                self.report["checks"]["security"] = {
                    "status": "bandit_not_available",
                    "message": "Install bandit: pip install bandit"
                }
                print("⚠️  Bandit not available (install with: pip install bandit)")
                
        except Exception as e:
            self.report["checks"]["security"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Error running security checks: {e}")
    
    def generate_report(self):
        """Generate and save report"""
        print("\n📊 Generating system report...")
        
        # Save JSON report
        report_file = self.project_root / "system_health_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        
        # Generate markdown report
        md_report = self.generate_markdown_report()
        md_file = self.project_root / "SYSTEM_HEALTH_REPORT.md"
        with open(md_file, 'w') as f:
            f.write(md_report)
        
        print(f"✅ Report saved to: {report_file}")
        print(f"✅ Markdown report saved to: {md_file}")
        
        return md_report
    
    def generate_markdown_report(self):
        """Generate markdown report"""
        md = f"""# 🔍 Agentic Agile System Health Report

**Generated:** {self.report['timestamp']}
**Repository:** {self.project_root.name}

## 📊 Summary

"""
        
        # Agents summary
        if "agents" in self.report["checks"]:
            agents = self.report["checks"]["agents"]
            complete = sum(1 for status in agents.values() if status["status"] == "complete")
            incomplete = sum(1 for status in agents.values() if status["status"] == "incomplete")
            missing = sum(1 for status in agents.values() if status["status"] == "missing")
            
            md += f"""### 🤖 Agents Status: {complete}/8 Complete

- ✅ **Complete:** {complete} agents
- ⚠️ **Incomplete:** {incomplete} agents  
- ❌ **Missing:** {missing} agents

"""
        
        # Documentation summary
        if "documentation" in self.report["checks"]:
            docs = self.report["checks"]["documentation"]
            present = sum(1 for status in docs.values() if status["status"] == "present")
            missing = sum(1 for status in docs.values() if status["status"] == "missing")
            
            md += f"""### 📚 Documentation Status: {present}/{len(docs)} Present

- ✅ **Present:** {present} documents
- ❌ **Missing:** {missing} documents

"""
        
        # Infrastructure summary
        if "infrastructure" in self.report["checks"]:
            infra = self.report["checks"]["infrastructure"]
            present = sum(1 for status in infra.values() if status["status"] == "present")
            missing = sum(1 for status in infra.values() if status["status"] == "missing")
            
            md += f"""### 🏗️ Infrastructure Status: {present}/{len(infra)} Present

- ✅ **Present:** {present} components
- ❌ **Missing:** {missing} components

"""
        
        # Dependencies
        if "dependencies" in self.report["checks"]:
            deps = self.report["checks"]["dependencies"]
            if deps["status"] == "checked":
                md += f"""### 📦 Dependencies: {deps['outdated_count']} Outdated

"""
                if deps["outdated_count"] > 0:
                    for pkg in deps["outdated_packages"][:5]:
                        md += f"- {pkg['name']}: {pkg['version']} → {pkg['latest_version']}\n"
        
        # Security
        if "security" in self.report["checks"]:
            security = self.report["checks"]["security"]
            if security["status"] == "checked":
                md += f"""### 🔒 Security: {security['issues_count']} Issues Found

"""
        
        # Recommendations
        if self.report["recommendations"]:
            md += """## 🎯 Recommendations

"""
            for rec in self.report["recommendations"]:
                md += f"- {rec}\n"
        
        md += """
## 📝 Next Steps

1. Review the detailed JSON report: `system_health_report.json`
2. Address high-priority recommendations
3. Run tests to ensure system stability
4. Update documentation as needed
5. Consider creating a new release

---
*Report generated by Agentic Agile System Updater*
"""
        
        return md
    
    def run_all_checks(self):
        """Run all system checks"""
        print("🚀 Starting Agentic Agile System health check...\n")
        
        self.check_agents()
        print()
        
        self.check_documentation()
        print()
        
        self.check_infrastructure()
        print()
        
        self.check_dependencies()
        print()
        
        self.check_security()
        print()
        
        report = self.generate_report()
        
        print("\n" + "="*50)
        print("🎉 System health check complete!")
        print("="*50)
        
        return report


def main():
    """Main function"""
    updater = SystemUpdater()
    report = updater.run_all_checks()
    
    # Print summary
    print("\n📋 Quick Summary:")
    print(report.split("## 📊 Summary")[1].split("## 📝 Next Steps")[0])


if __name__ == "__main__":
    main() 
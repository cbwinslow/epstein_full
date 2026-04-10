#!/usr/bin/env python3
"""
Epstein Project — AI Agent Data Quality Monitor

Integration script for AI agents to run automated data quality checks
and report findings. Can be triggered by:
- Scheduled cron jobs
- GitHub Actions workflows
- Manual execution
- AI agent commands

Usage:
  python ai_quality_agent.py --run-check        # Run check and report
  python ai_quality_agent.py --analyze          # Generate AI analysis
  python ai_quality_agent.py --monitor          # Continuous monitoring mode
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = os.environ.get("EPSTEIN_PROJECT_ROOT", "/home/cbwinslow/workspace/epstein")
REPORT_DIR = f"{PROJECT_ROOT}/data_quality_reports"


def run_data_quality_check() -> dict:
    """Run the data quality validator and return results."""
    validator_path = f"{PROJECT_ROOT}/scripts/data_quality_validator.py"
    
    if not os.path.exists(validator_path):
        return {"error": "Data quality validator not found"}
    
    try:
        result = subprocess.run(
            ["python3", validator_path, "--ai-report"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Find the latest report
        reports = sorted(Path(REPORT_DIR).glob("data_quality_report_*.json"))
        if reports:
            with open(reports[-1]) as f:
                return json.load(f)
        else:
            return {"error": "No report generated"}
            
    except subprocess.TimeoutExpired:
        return {"error": "Quality check timed out"}
    except Exception as e:
        return {"error": str(e)}


def generate_ai_summary(report: dict) -> str:
    """Generate a human-readable summary for AI agents."""
    summary = f"""## Data Quality Report Summary

**Generated:** {report.get('timestamp', 'N/A')}
**Overall Status:** {report.get('summary', {}).get('status', 'UNKNOWN')}

### Statistics
- Critical Issues: {report.get('summary', {}).get('critical_count', 0)}
- Total Issues: {report.get('summary', {}).get('total_issues', 0)}
- Total Warnings: {report.get('summary', {}).get('total_warnings', 0)}

"""
    
    # Add issues section
    issues = report.get('issues', [])
    if issues:
        summary += "### Critical Issues\n\n"
        for i, issue in enumerate(issues[:5], 1):
            summary += f"{i}. **[{issue.get('severity')}]** {issue.get('type')} in `{issue.get('table')}`\n"
            summary += f"   - {issue.get('details')}\n\n"
        
        if len(issues) > 5:
            summary += f"_... and {len(issues) - 5} more issues_\n\n"
    
    # Add warnings section
    warnings = report.get('warnings', [])
    if warnings:
        summary += "### Warnings\n\n"
        for i, warning in enumerate(warnings[:3], 1):
            summary += f"{i}. {warning.get('type')} in `{warning.get('table')}`: {warning.get('details')}\n"
        
        if len(warnings) > 3:
            summary += f"_... and {len(warnings) - 3} more warnings_\n\n"
    
    # Add recommendations
    summary += """### Recommendations

1. **Immediate Action Required:** Address all HIGH severity issues
2. **Data Quality Improvement:** Review MEDIUM severity warnings
3. **Monitoring:** Schedule regular data quality checks

"""
    
    # Add next steps for AI agent
    if issues:
        summary += """### Next Steps for AI Agent

1. Investigate root cause of critical issues
2. Generate SQL fix scripts
3. Validate fixes after application
4. Document data quality standards

"""
    else:
        summary += "### Status\n✓ Data quality checks passed. No immediate action required.\n"
    
    return summary


def save_memory_to_letta(report: dict, summary: str):
    """Save data quality report to Letta memory system."""
    try:
        sys.path.insert(0, '/home/cbwinslow/dotfiles/ai/packages/letta_integration')
        from letta_integration import LettaIntegration
        
        letta = LettaIntegration(
            server_url='http://localhost:8283',
            agent_name='windsurf'
        )
        
        # Create memory content
        memory_content = f"""Data Quality Check Run - {datetime.now().isoformat()}

Status: {report.get('summary', {}).get('status', 'UNKNOWN')}
Critical Issues: {report.get('summary', {}).get('critical_count', 0)}
Total Issues: {report.get('summary', {}).get('total_issues', 0)}

{summary}
"""
        
        # Save to archival memory
        agent_id = letta.get_or_create_agent('windsurf')
        if agent_id:
            letta.save_to_archival(
                text=memory_content,
                tags=['data-quality', 'validation', 'epstein-project']
            )
            print("✓ Saved to Letta memory")
        
    except Exception as e:
        print(f"⚠ Could not save to Letta: {e}")


def create_github_issue(report: dict) -> str:
    """Create a GitHub issue for critical data quality issues."""
    if report.get('summary', {}).get('critical_count', 0) == 0:
        return None
    
    title = f"[Data Quality] {report['summary']['critical_count']} critical issues found"
    
    body = f"""## Data Quality Alert

**Generated:** {report['timestamp']}
**Status:** {report['summary']['status']}

### Critical Issues Found

"""
    
    for issue in report.get('issues', []):
        if issue.get('severity') == 'HIGH':
            body += f"- [{issue['type']}] {issue['table']}: {issue['details']}\n"
    
    body += f"""

### Action Required

1. Run data quality validation: `python scripts/data_quality_validator.py`
2. Review generated report in `data_quality_reports/`
3. Apply fixes using SQL scripts
4. Re-run validation to confirm resolution

### Files

- Validator: `scripts/data_quality_validator.py`
- SQL Views: `migrations/004_data_quality_views.sql`
"""
    
    # Save issue template
    issue_path = f"{REPORT_DIR}/github_issue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(issue_path, 'w') as f:
        f.write(f"# {title}\n\n{body}")
    
    return issue_path


def continuous_monitor_mode(interval_minutes: int = 60, max_retries: int = 10):
    """Run continuous monitoring with periodic checks."""
    import time
    
    print(f"Starting continuous monitoring (interval: {interval_minutes} minutes)")
    print("Press Ctrl+C to stop")
    
    consecutive_errors = 0
    
    while True:
        try:
            print(f"\n[{datetime.now().isoformat()}] Running data quality check...")
            report = run_data_quality_check()
            
            # Reset error counter on success
            consecutive_errors = 0
            
            if report.get('summary', {}).get('status') == 'FAIL':
                print("⚠ CRITICAL ISSUES DETECTED")
                summary = generate_ai_summary(report)
                print(summary)
                
                # Create GitHub issue for critical issues
                issue_path = create_github_issue(report)
                if issue_path:
                    print(f"✓ GitHub issue template created: {issue_path}")
                
                # Save to memory
                save_memory_to_letta(report, summary)
            else:
                print("✓ Data quality check passed")
            
            time.sleep(interval_minutes * 60)
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break
        except Exception as e:
            consecutive_errors += 1
            print(f"Error during monitoring (attempt {consecutive_errors}/{max_retries}): {e}")
            if consecutive_errors >= max_retries:
                print(f"Max retries ({max_retries}) reached. Stopping monitoring.")
                break
            time.sleep(60)  # Wait 1 minute before retry


def main():
    parser = argparse.ArgumentParser(
        description="AI Agent Data Quality Monitor"
    )
    parser.add_argument(
        "--run-check", action="store_true",
        help="Run data quality check and report"
    )
    parser.add_argument(
        "--analyze", action="store_true",
        help="Generate AI analysis summary"
    )
    parser.add_argument(
        "--monitor", action="store_true",
        help="Run continuous monitoring"
    )
    parser.add_argument(
        "--interval", type=int, default=60,
        help="Monitoring interval in minutes (default: 60)"
    )
    parser.add_argument(
        "--save-memory", action="store_true",
        help="Save results to Letta memory"
    )
    
    args = parser.parse_args()
    
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    if args.monitor:
        continuous_monitor_mode(args.interval)
    elif args.run_check:
        report = run_data_quality_check()
        summary = generate_ai_summary(report)
        print(summary)
        
        if args.save_memory:
            save_memory_to_letta(report, summary)
        
        # Return exit code based on status
        if report.get('summary', {}).get('status') == 'FAIL':
            return 1
    elif args.analyze:
        # Find latest report and analyze
        reports = sorted(Path(REPORT_DIR).glob("data_quality_report_*.json"))
        if reports:
            with open(reports[-1]) as f:
                report = json.load(f)
            summary = generate_ai_summary(report)
            print(summary)
        else:
            print("No data quality reports found. Run with --run-check first.")
            return 1
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

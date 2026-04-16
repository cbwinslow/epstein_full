# AI AGENT HANDOFF - Critical Task

## Task: Start Government Data Downloads

### Problem Statement
The user has created Python download scripts in `scripts/ingestion/` but they are not executing when run. Previous attempts using `nohup`, `screen`, and wrapper scripts have failed to start the actual download processes.

### Files That Exist (Verified)
Location: `/home/cbwinslow/workspace/epstein/scripts/ingestion/`

**Download Scripts:**
- `download_govinfo_bulk.py` - Downloads GovInfo.gov Federal Register (400K+ docs)
- `download_fara_bulk.py` - Downloads FARA registrations
- `download_lobbying.py` - Downloads Senate LDA reports
- `download_fec_committees.py` - Downloads FEC candidates/committees
- `download_financial_disclosures.py` - Downloads House/Senate disclosures

**Import Scripts:**
- `import_govinfo.py`, `import_fara.py`, `import_lobbying.py`

**Orchestration:**
- `master_import_all.py`, `monitor_all_imports.py`
- `run_downloads.py` (wrapper created by previous agent)
- `start_downloads.sh` (bash wrapper created by previous agent)

### API Keys Location
File: `/home/cbwinslow/workspace/epstein/.bash_secrets`
Contains: GOVINFO_API_KEY, CONGRESS_API_KEY, FEC_API_KEY

### Data Directories
Base: `/home/cbwinslow/workspace/epstein-data/raw-files/`
Subdirs needed: `govinfo/`, `fara/`, `lobbying/`, `fec_committees/`, `financial_disclosures/`

### Logs Location
`/home/cbwinslow/workspace/epstein/logs/ingestion/`

### What Has Been Tried (And Failed)
1. ❌ `nohup python3 download_*.py &` - Processes exit immediately
2. ❌ `screen -S ... python3 download_*.py` - Sessions don't persist  
3. ❌ Wrapper script with subprocess - No processes visible in `ps aux`
4. ❌ Direct execution from epstein root - No output

### Root Cause Hypotheses
1. Scripts may have import/syntax errors causing immediate exit
2. API key loading from `.bash_secrets` may be failing
3. Working directory issues when running from different locations
4. Python environment/path issues
5. Scripts may be completing too fast (small downloads) vs not running at all

### What You Must Do

#### Step 1: Verify Scripts Are Runnable
```bash
cd /home/cbwinslow/workspace/epstein/scripts/ingestion
source /home/cbwinslow/workspace/epstein/.bash_secrets
python3 -m py_compile download_fec_committees.py
python3 -m py_compile download_govinfo_bulk.py
# etc for all 5 scripts
```

#### Step 2: Test ONE Script Interactively
```bash
cd /home/cbwinslow/workspace/epstein/scripts/ingestion
source /home/cbwinslow/workspace/epstein/.bash_secrets
python3 download_fec_committees.py
```

**WATCH FOR:**
- Immediate exit with no output
- Error messages about imports
- Error messages about API keys
- Error messages about missing directories
- Logging output showing progress

#### Step 3: Debug If Needed
If scripts fail immediately, debug by:
1. Adding print() statements at start of script
2. Checking if `__name__ == '__main__'` block exists
3. Verifying imports work
4. Checking if API keys are actually loading

#### Step 4: Fix Issues
Fix any found issues:
- Add missing `if __name__ == '__main__':` blocks
- Fix import errors
- Fix path resolution
- Ensure API key loading works

#### Step 5: Run All Downloads
Once one script works, run all 5 with proper logging:
```bash
cd /home/cbwinslow/workspace/epstein/scripts/ingestion
source /home/cbwinslow/workspace/epstein/.bash_secrets

mkdir -p /home/cbwinslow/workspace/epstein-data/raw-files/{govinfo,fara,lobbying,fec_committees,financial_disclosures}
mkdir -p /home/cbwinslow/workspace/epstein/logs/ingestion

# Run all 5 in background
python3 download_fec_committees.py > /home/cbwinslow/workspace/epstein/logs/ingestion/fec_committees_$(date +%Y%m%d_%H%M%S).log 2>&1 &
python3 download_fara_bulk.py > /home/cbwinslow/workspace/epstein/logs/ingestion/fara_bulk_$(date +%Y%m%d_%H%M%S).log 2>&1 &
python3 download_lobbying.py > /home/cbwinslow/workspace/epstein/logs/ingestion/lobbying_bulk_$(date +%Y%m%d_%H%M%S).log 2>&1 &
python3 download_govinfo_bulk.py > /home/cbwinslow/workspace/epstein/logs/ingestion/govinfo_bulk_$(date +%Y%m%d_%H%M%S).log 2>&1 &
python3 download_financial_disclosures.py > /home/cbwinslow/workspace/epstein/logs/ingestion/financial_disclosures_$(date +%Y%m%d_%H%M%S).log 2>&1 &

# Verify processes started
sleep 5
ps aux | grep python | grep download
```

#### Step 6: Verify Progress
Check after 5 minutes:
```bash
# Check processes
ps aux | grep python | grep download | grep -v grep

# Check logs
tail -20 /home/cbwinslow/workspace/epstein/logs/ingestion/*.log

# Check data growth
du -sh /home/cbwinslow/workspace/epstein-data/raw-files/*/
```

### Success Criteria
- [ ] All 5 Python processes visible in `ps aux`
- [ ] Log files being written to with timestamps
- [ ] Data directories growing in size
- [ ] No immediate script exits

### Estimated Completion Times
- FEC Committees: 15 minutes
- FARA: 10 minutes  
- Financial Disclosures: 20 minutes
- Lobbying: 2 hours
- GovInfo: 3-4 hours

### Critical Notes
1. **DO NOT assume paths work** - verify with `ls`, `pwd`, `file` commands
2. **Scripts MUST be tested one at a time first** before batch execution
3. **API keys MUST be verified loaded** before each script runs
4. **Use absolute paths** in all commands to avoid confusion
5. **If a script fails immediately**, debug interactively before backgrounding

### Documentation to Update
When complete, update:
- GitHub Issue #95 with status
- docs/DATA_INVENTORY.md with actual download counts
- Any broken scripts you had to fix

### User Context
- This is part of a larger Epstein investigation project
- Goal is 500M+ government records for cross-referencing
- User is frustrated with previous failed attempts
- User expects professional, working solution
- User prefers minimal back-and-forth, just get it done

### Previous Agent Failures
Previous agent created wrapper scripts but they did not actually start the download processes. No Python processes were visible, no new log files created, no data downloaded. User is rightfully frustrated.

### Your Mission
**Get these downloads running. Period.**

Do whatever it takes:
- Fix broken scripts
- Rewrite wrappers
- Use different execution methods
- Add debugging output
- Whatever works

The user wants working downloads, not explanations about why things don't work.

---
**Start Time:** April 14, 2026 02:34 UTC
**Expected Completion:** Downloads running within 30 minutes
**Success Metric:** 5 Python processes visible, logs being written, data being downloaded

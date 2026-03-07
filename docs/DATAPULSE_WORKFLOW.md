# DataPulse Team 9 - Scrum Workflow

## Team Structure

### Product Owner: Kevin
- Defines DataPulse vision and priorities
- Creates user stories for MVP features
- Accepts/rejects completed work
- Available for clarifications

### Scrum Master: TBD (Selected by Kevin)
- Facilitates daily standups
- Removes blockers
- Ensures 4-day sprint timeline adherence
- Coordinates between team members

### Development Team

| Role | Name | Responsibilities |
|------|------|-----------------|
| Backend Dev 1 | Joseph Lubandi | File Upload & Validation Engine |
| Backend Dev 2 | Diane Ishimwe | API & Reporting |
| Backend Dev 3 | Bright Kirenga | Scheduling & Notifications |
| QA Engineer | Bernice Mawuena | Testing & Quality Assurance |
| DevOps | Yram Asher | Infrastructure & CI/CD |
| Data Engineer | Zainab Abdullai | Schema & Data Pipeline |

---

## 4-Day Sprint Structure

### Day 1: Setup & Sprint Planning (Monday)

**Morning: Sprint Planning (2 hours)**
- Kevin presents prioritized user stories
- Team estimates story points
- Team commits to sprint goal
- Break stories into tasks

**Afternoon: Setup & Foundation**
- Clone repository and review starter code
- Set up development environment
- Database schema finalized
- Auth system implementation starts
- CI/CD pipeline setup begins

**Deliverables:**
- Sprint backlog finalized
- Tasks assigned on GitHub Project board
- Development environments ready
- Initial branches created

---

### Day 2: Core Development (Tuesday)

**Morning: Daily Standup (15 min)**
- Automated standup issue created at 7 AM UTC
- Each member posts: yesterday's work, today's plan, blockers

**All Day: Core Features**
- Primary CRUD operations
- Core business logic implementation
- Frontend/UI connected to backend APIs
- Initial test suite running
- Sample data loaded

**End of Day:**
- PRs created for completed tasks
- Code reviews assigned
- Update project board

---

### Day 3: Integration & Testing (Wednesday)

**Morning: Daily Standup (15 min)**

**Mid-Morning: Backlog Refinement (1 hour)**
- Review progress
- Adjust priorities if needed
- Identify risks

**All Day: Integration**
- All MVP features implemented
- End-to-end integration testing
- Analytics/dashboard pipeline working
- Bug fixes from testing
- Docker containers running together

**End of Day:**
- Integration testing complete
- Critical bugs identified and fixed
- Stretch goals assessment

---

### Day 4: Polish & Demo (Thursday)

**Morning: Daily Standup (15 min)**

**Morning-Afternoon: Final Polish**
- All critical bugs fixed
- Final testing and QA
- Documentation complete
- Stretch goals (if time permits)

**Afternoon: Sprint Review (1 hour)**
- Demo completed user stories to Kevin
- Kevin accepts/rejects based on acceptance criteria
- Gather feedback

**Late Afternoon: Sprint Retrospective (45 min)**
- What went well?
- What didn't go well?
- What can we improve next sprint?

**Deliverables:**
- Working MVP demo
- All documentation complete
- Retrospective action items

---

## DataPulse User Stories & Task Breakdown

### Epic 1: File Upload & Validation

**User Story #1: File Upload (8 points)**
```
As a Data Analyst,
I want to upload CSV and JSON files,
So that I can validate my data quality.
```

**Tasks:**
- #1.1 [Backend-Joseph] Create file upload API endpoint
- #1.2 [Backend-Joseph] Implement CSV parser with error handling
- #1.3 [Backend-Joseph] Implement JSON parser with error handling
- #1.4 [DevOps-Yram] Configure file storage volume in Docker
- #1.5 [QA-Bernice] Test file upload with various formats

**User Story #2: Validation Rules (13 points)**
```
As a Data Engineer,
I want to define validation rules for my datasets,
So that I can check data quality automatically.
```

**Tasks:**
- #2.1 [Backend-Joseph] Create validation rules CRUD API
- #2.2 [Backend-Joseph] Implement null check rule
- #2.3 [Backend-Joseph] Implement data type check rule
- #2.4 [Backend-Joseph] Implement range check rule
- #2.5 [Backend-Joseph] Implement uniqueness check rule
- #2.6 [Data-Zainab] Design rules table schema
- #2.7 [QA-Bernice] Test each rule type with edge cases

**User Story #3: Quality Score Calculation (5 points)**
```
As a Data Analyst,
I want to see a quality score (0-100) for my dataset,
So that I can quickly assess data quality.
```

**Tasks:**
- #3.1 [Backend-Joseph] Implement quality score calculator
- #3.2 [Backend-Joseph] Calculate percentage of rows passing rules
- #3.3 [QA-Bernice] Test score calculation accuracy

---

### Epic 2: Reporting & Dashboard

**User Story #4: Quality Reports (8 points)**
```
As a Data Analyst,
I want detailed quality reports,
So that I can see which rules failed and why.
```

**Tasks:**
- #4.1 [Backend-Diane] Create quality report generation API
- #4.2 [Backend-Diane] Generate per-rule findings
- #4.3 [Data-Zainab] Design reports table schema
- #4.4 [QA-Bernice] Test report generation

**User Story #5: Trend Dashboard (8 points)**
```
As a Data Manager,
I want to see quality trends over time,
So that I can track data quality improvements.
```

**Tasks:**
- #5.1 [Backend-Diane] Create trend API endpoint
- #5.2 [Backend-Diane] Aggregate historical quality scores
- #5.3 [Data-Zainab] Create data pipeline for metrics
- #5.4 [Data-Zainab] Optimize queries with indexes
- #5.5 [QA-Bernice] Test trend calculations

---

### Epic 3: Authentication & Security

**User Story #6: User Authentication (5 points)**
```
As a user,
I want to log in securely,
So that my data is protected.
```

**Tasks:**
- #6.1 [Backend-Diane] Implement JWT authentication
- #6.2 [Backend-Diane] Create registration endpoint
- #6.3 [Backend-Diane] Create login endpoint
- #6.4 [Backend-Diane] Add authorization middleware
- #6.5 [QA-Bernice] Test auth flows

---

### Epic 4: Scheduling & Notifications (Stretch)

**User Story #7: Scheduled Checks (8 points)**
```
As a Data Engineer,
I want to schedule automatic quality checks,
So that I don't have to run them manually.
```

**Tasks:**
- #7.1 [Backend-Bright] Implement cron-based scheduler
- #7.2 [Backend-Bright] Create schedule configuration API
- #7.3 [Backend-Bright] Add batch processing for multiple datasets
- #7.4 [QA-Bernice] Test scheduled execution

**User Story #8: Quality Alerts (5 points)**
```
As a Data Manager,
I want email alerts when quality drops,
So that I can respond quickly to issues.
```

**Tasks:**
- #8.1 [Backend-Bright] Implement notification system
- #8.2 [Backend-Bright] Create alert threshold configuration
- #8.3 [Backend-Bright] Add email sending functionality
- #8.4 [QA-Bernice] Test alert triggers

---

## Daily Workflow

### Morning Routine (Every Day)

1. **Check automated standup issue (7 AM UTC)**
2. **Post your update:**
   ```
   Yesterday: Completed task #1.1 - file upload endpoint
   Today: Working on task #1.2 - CSV parser
   Blockers: None
   ```
3. **Review team updates**
4. **Check assigned PRs for review**

### Development Workflow

1. **Pick task from Sprint Backlog**
   - Assign yourself on GitHub
   - Move to "In Progress"

2. **Create feature branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/file-upload-api
   ```

3. **Implement with TDD**
   ```bash
   # Write test first
   pytest tests/test_upload.py -v

   # Implement feature
   # Run tests again
   pytest tests/test_upload.py -v
   ```

4. **Commit with convention**
   ```bash
   git add .
   git commit -m "feat(upload): add CSV file upload endpoint"
   git push origin feature/file-upload-api
   ```

5. **Create Pull Request**
   - Use PR template
   - Link to task: "Closes #1.1"
   - Reviewer auto-assigned
   - Wait for CI to pass

6. **Address review feedback**
   - Make requested changes
   - Push updates
   - Re-request review

7. **Merge when approved**
   - Squash and merge
   - Delete branch
   - Task moves to "Done"

---

## Role-Specific Workflows

### Backend Developers (Joseph, Diane, Bright)

**Daily Tasks:**
1. Implement assigned API endpoints
2. Write unit tests (pytest)
3. Update API documentation
4. Review other backend PRs
5. Coordinate on shared models

**Code Standards:**
- Follow FastAPI best practices
- Use Pydantic for validation
- SQLAlchemy for database
- Type hints required
- Docstrings for all functions

### QA Engineer (Bernice)

**Daily Tasks:**
1. Write test cases for new features
2. Execute manual testing
3. Report bugs with severity
4. Verify bug fixes
5. Update test documentation

**Testing Checklist:**
- [ ] API endpoint tests
- [ ] Validation rule tests
- [ ] Integration tests
- [ ] Edge case tests
- [ ] Performance tests

### DevOps (Yram)

**Daily Tasks:**
1. Monitor CI/CD pipeline
2. Fix build issues
3. Update Docker configurations
4. Manage environments
5. Review infrastructure PRs

**Responsibilities:**
- Dockerfile optimization
- Docker Compose setup
- GitHub Actions workflows
- Environment variables
- Deployment documentation

### Data Engineer (Zainab)

**Daily Tasks:**
1. Design database schemas
2. Write migration scripts
3. Optimize queries
4. Create data pipelines
5. Document data models

**Deliverables:**
- Database schema diagrams
- Migration scripts
- Index optimization
- Data dictionary
- ETL pipeline code

---

## GitHub Project Board Setup

### Columns:
1. **Product Backlog** - All user stories (Kevin prioritizes)
2. **Sprint Backlog** - Current sprint tasks
3. **In Progress** - Actively being worked on
4. **In Review** - PR submitted
5. **Done** - Merged and deployed

### Labels:
- `type: story` - User story
- `type: task` - Technical task
- `type: bug` - Defect
- `role: backend` - Backend work
- `role: qa` - QA work
- `role: devops` - DevOps work
- `role: data` - Data engineering work
- `priority: high` - Must have for MVP
- `priority: medium` - Should have
- `priority: low` - Nice to have
- `status: blocked` - Waiting on dependency

---

## Communication Channels

### Daily Standup
- Automated GitHub issue at 7 AM UTC
- Post updates in issue comments
- Tag @Scrum-Master for blockers

### Code Reviews
- Auto-assigned by workflow
- Review within 4 hours
- Use PR comments for feedback

### Blockers
- Post in standup issue immediately
- Tag relevant team member
- Scrum Master escalates if needed

### Questions
- Technical: Ask in PR or issue
- Process: Ask Scrum Master
- Requirements: Ask Kevin (PO)

---

## Definition of Done

### For Tasks:
- [ ] Code implemented
- [ ] Unit tests written and passing
- [ ] Code reviewed and approved
- [ ] PR merged to develop
- [ ] Documentation updated

### For User Stories:
- [ ] All tasks completed
- [ ] Integration tests passing
- [ ] QA approval obtained
- [ ] Deployed to staging
- [ ] Kevin (PO) acceptance
- [ ] No critical bugs

---

## Example: Day 1 Sprint Planning

**Kevin (PO) presents:**
```
Priority 1: User Story #1 - File Upload (8 pts)
Priority 2: User Story #2 - Validation Rules (13 pts)
Priority 3: User Story #6 - Authentication (5 pts)
Priority 4: User Story #3 - Quality Score (5 pts)
Priority 5: User Story #4 - Quality Reports (8 pts)

Sprint Goal: Users can upload files, define rules, and see quality scores
Total: 39 story points
```

**Team breaks down stories:**
```
Joseph takes: Story #1, #2, #3 (File upload & validation)
Diane takes: Story #6, #4 (Auth & reporting)
Bright takes: Story #5 (Trends - if time permits)
Bernice: Tests for all stories
Yram: Docker setup, CI/CD
Zainab: Database schema for all features
```

**Tasks created and assigned:**
- 25 tasks created from 5 user stories
- Each task assigned to specific person
- All tasks moved to Sprint Backlog
- Team commits to sprint goal

---

## Success Metrics

### Velocity
- Target: 35-40 story points per 4-day sprint
- Track actual vs. planned

### Quality
- Code coverage: >80%
- All tests passing
- Zero critical bugs at demo

### Collaboration
- All PRs reviewed within 4 hours
- Daily standup participation: 100%
- No blockers lasting >1 day

---

## Quick Reference Commands

```bash
# Start work on task
git checkout develop
git pull origin develop
git checkout -b feature/task-name

# Run tests
cd backend
pytest tests/ -v --cov=.

# Commit
git add .
git commit -m "feat(scope): description"

# Push and create PR
git push origin feature/task-name
gh pr create --title "feat(scope): description" --body "Closes #123"

# Run locally
docker-compose up --build

# Check CI status
gh pr checks
```

---

## Emergency Procedures

### Critical Bug Found
1. Create bug issue immediately
2. Label `priority: high` + `type: bug`
3. Notify Scrum Master
4. Scrum Master decides: fix now or defer
5. If urgent, pull from sprint backlog

### Team Member Blocked
1. Post in standup issue with `@Scrum-Master`
2. Scrum Master investigates within 1 hour
3. If external blocker, escalate to Kevin
4. Team member picks different task meanwhile

### Behind Schedule
1. Scrum Master assesses at Day 2 standup
2. Options: reduce scope, pair programming, defer stretch goals
3. Communicate with Kevin
4. Focus on MVP features only

---

**Remember:** This is a 4-day sprint. Move fast, communicate often, and focus on delivering working software!

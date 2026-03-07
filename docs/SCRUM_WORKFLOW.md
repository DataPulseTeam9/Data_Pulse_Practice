# Scrum Workflow Guide

## Overview
This document outlines the complete Scrum workflow for the DataPulse project, from Product Owner requirements to Developer implementation.

---

## Roles & Responsibilities

### Product Owner (PO)
- Defines product vision and priorities
- Creates and maintains product backlog
- Writes user stories with business value
- Accepts/rejects completed work
- Available for clarifications

### Scrum Master
- Facilitates Scrum ceremonies
- Removes blockers
- Ensures process adherence
- Coaches team on Agile practices
- Shields team from distractions

### Development Team
- Self-organizing and cross-functional
- Estimates story points
- Breaks stories into tasks
- Implements, tests, and delivers features
- Participates in all ceremonies

---

## Scrum Artifacts

### 0. Epic
**Created by:** Product Owner
**Template:** `.github/ISSUE_TEMPLATE/epic.md`

**Purpose:** Group related user stories into a larger feature or initiative

**Example:**
```
Epic #10: File Upload & Validation System
├── User Story #11: CSV File Upload
├── User Story #12: JSON File Upload
├── User Story #13: Validation Rules Engine
└── User Story #14: Quality Score Calculation
```

**Contains:**
- Epic overview and business value
- List of user stories (linked)
- Total story points
- Target sprint(s)
- Dependencies

**When to use:**
- Feature spans multiple sprints
- Multiple related user stories
- Large initiative (>21 story points)

### 1. User Story
**Created by:** Product Owner
**Template:** `.github/ISSUE_TEMPLATE/user_story.md`

**Format:**
```
As a [role],
I want [feature],
So that [benefit].
```

**Example:**
```
As a Data Analyst,
I want to upload CSV files through the web interface,
So that I can validate data quality without using the API.
```

**Contains:**
- User story statement
- Acceptance criteria (Given/When/Then)
- Story points (estimated by team)
- Sprint assignment
- Definition of Done

### 2. Task
**Created by:** Developers (from user stories)
**Template:** `.github/ISSUE_TEMPLATE/task.md`

**Purpose:** Break down user stories into implementable technical work

**Example:**
```
[Backend] Create CSV upload endpoint
[Frontend] Build file upload component
[DevOps] Configure file storage volume
```

### 3. Bug
**Created by:** Anyone
**Template:** `.github/ISSUE_TEMPLATE/bug_report.md`

**Purpose:** Report defects found during development or testing

---

## Workflow: From Story to Deployment

### Phase 1: Product Backlog Refinement
**When:** Ongoing, formal session mid-sprint
**Who:** PO + Scrum Master + Dev Team

1. **PO creates User Story**
   - Opens issue using User Story template
   - Fills in role, feature, benefit
   - Adds acceptance criteria
   - Labels: `type: story`

2. **Team refines story**
   - Discusses requirements
   - Clarifies acceptance criteria
   - Identifies dependencies
   - Estimates story points (Planning Poker)
   - PO prioritizes in backlog

### Phase 2: Sprint Planning
**When:** Start of sprint (every 2 weeks)
**Who:** Entire Scrum team

1. **PO presents top priority stories**
2. **Team commits to sprint goal**
3. **Developers break stories into tasks**
   - Create Task issues from User Story
   - Link tasks: "Part of #[story-number]"
   - Assign to developers
   - Move to "Sprint Backlog" on project board

**Example breakdown:**
```
User Story #45: CSV Upload Feature (8 points)
├── Task #46: [Backend] Create upload endpoint
├── Task #47: [Backend] Add file validation
├── Task #48: [Frontend] Build upload UI
└── Task #49: [Test] Write integration tests
```

### Phase 3: Development
**When:** During sprint
**Who:** Developers

1. **Pick task from Sprint Backlog**
   - Move card to "In Progress" on board
   - Assign yourself

2. **Create feature branch**
   ```bash
   git checkout -b feature/csv-upload-endpoint
   ```

3. **Implement & commit**
   - Write code
   - Write tests
   - Run pre-commit hooks
   - Commit with conventional format:
     ```bash
     git commit -m "feat(upload): add CSV upload endpoint"
     ```

4. **Create Pull Request**
   - Use PR template
   - Link to task: "Closes #46"
   - Request review (auto-assigned by workflow)
   - PR moves to "In Review" automatically

### Phase 4: Code Review
**When:** After PR creation
**Who:** Assigned reviewer

1. **Reviewer checks:**
   - Code quality and standards
   - Tests coverage
   - Acceptance criteria met
   - No security issues

2. **Review outcomes:**
   - **Approve:** PR labeled "status: approved"
   - **Request changes:** PR labeled "status: needs-work"
   - Developer addresses feedback and re-requests review

3. **Merge PR**
   - Squash and merge
   - Delete branch
   - Task automatically moves to "Done"

### Phase 5: Daily Standup
**When:** Every weekday 7 AM UTC (automated)
**Who:** Dev team + Scrum Master

**Automated standup issue created with:**
1. What did I complete yesterday?
2. What am I working on today?
3. Any blockers?

**Team responds in issue comments**

### Phase 6: Sprint Review
**When:** End of sprint
**Who:** Scrum team + stakeholders

1. **Demo completed user stories**
2. **PO accepts/rejects based on acceptance criteria**
3. **Gather feedback**
4. **Update product backlog**

### Phase 7: Sprint Retrospective
**When:** After sprint review
**Who:** Scrum team only

**Discuss:**
- What went well?
- What didn't go well?
- What can we improve?

**Action items become tasks for next sprint**

---

## GitHub Project Board Columns

```
📋 Product Backlog    → All user stories (prioritized by PO)
🎯 Sprint Backlog     → Stories/tasks for current sprint
🚧 In Progress        → Actively being worked on
👀 In Review          → PR submitted, awaiting review
✅ Done               → Merged and deployed
```

---

## Story Points Guide

| Points | Complexity | Time Estimate |
|--------|-----------|---------------|
| 1      | Trivial   | < 2 hours     |
| 2      | Simple    | 2-4 hours     |
| 3      | Easy      | 4-8 hours     |
| 5      | Medium    | 1-2 days      |
| 8      | Complex   | 2-3 days      |
| 13     | Very complex | 3-5 days   |
| 21     | Too large | Split story   |

**Rule:** If story > 13 points, break it down into smaller stories

---

## Definition of Done (DoD)

A user story is "Done" when:
- [ ] All tasks completed
- [ ] Code reviewed and approved
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] CI/CD pipeline passes
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] PO acceptance obtained
- [ ] No known bugs

---

## Labels & Automation

### Issue Labels
- `type: epic` - Large feature spanning multiple stories
- `type: story` - User story
- `type: task` - Technical task
- `type: bug` - Defect
- `status: in-review` - PR under review
- `status: needs-work` - Changes requested
- `status: approved` - Ready to merge
- `priority: high` - Must have this sprint
- `priority: medium` - Should have
- `priority: low` - Nice to have

### Automated Workflows
1. **PR opened** → Auto-assign reviewer → Label "in-review"
2. **Review approved** → Label "approved" → Notify team
3. **Changes requested** → Label "needs-work" → Notify author
4. **PR merged** → Close linked issues → Move to Done
5. **Daily standup** → Create issue → Assign team

---

## Example: Complete Flow

### Week 1: Sprint Planning

**Monday - PO creates story:**
```
Issue #100: User Story
As a Data Engineer,
I want to schedule data quality checks,
So that I can automate validation workflows.

Story Points: 8
Sprint: Sprint 5
```

**Team breaks into tasks:**
```
Issue #101: [Backend] Create scheduling API
Issue #102: [Backend] Add cron job processor
Issue #103: [Frontend] Build schedule UI
Issue #104: [Test] Write E2E tests
```

### Week 1-2: Development

**Developer 1:**
```bash
git checkout -b feature/scheduling-api
# ... implement ...
git commit -m "feat(scheduler): add scheduling API endpoint"
# Create PR → Closes #101
```

**Developer 2:**
```bash
git checkout -b feature/schedule-ui
# ... implement ...
git commit -m "feat(scheduler): add schedule management UI"
# Create PR → Closes #103
```

### Week 2: Review & Merge

- PRs reviewed and approved
- Merged to main
- CI/CD deploys to staging
- Tasks #101, #103 → Done

### Week 2: Sprint Review

- PO tests scheduling feature
- Verifies acceptance criteria
- Approves story #100
- Story moved to Done

---

## Best Practices

### For Product Owners
- Write stories from user perspective
- Include clear acceptance criteria
- Prioritize ruthlessly
- Be available for questions
- Accept/reject work promptly

### For Developers
- Break large stories into tasks
- Update task status daily
- Write meaningful commit messages
- Request review when ready
- Respond to review feedback quickly

### For Scrum Masters
- Keep ceremonies timeboxed
- Remove blockers immediately
- Ensure board is up-to-date
- Coach team on process
- Protect team from scope creep

---

## Common Scenarios

### Scenario 1: Story too large
**Problem:** Story estimated at 21 points
**Solution:** Split into multiple smaller stories
```
Original: "Build complete reporting system" (21 pts)
Split into:
- "Create report data API" (5 pts)
- "Build report UI components" (5 pts)
- "Add export functionality" (3 pts)
```

### Scenario 2: Bug found in sprint
**Problem:** Critical bug discovered
**Solution:**
1. Create bug issue immediately
2. Label `priority: high`
3. Scrum Master decides: fix now or next sprint
4. If urgent, pull from sprint backlog

### Scenario 3: Story not done by sprint end
**Problem:** Story incomplete at sprint review
**Solution:**
1. Do NOT mark as done
2. Move back to product backlog
3. Re-estimate if needed
4. Prioritize for next sprint

### Scenario 4: Scope creep during sprint
**Problem:** PO wants to add features mid-sprint
**Solution:**
1. Scrum Master protects sprint commitment
2. New requests go to product backlog
3. Discuss in next sprint planning
4. Emergency changes require team agreement

---

## Tools & Commands

### Create user story
```bash
# On GitHub: Issues → New Issue → User Story template
```

### Create task from story
```bash
# On GitHub: Issues → New Issue → Task template
# Add: "Part of #[story-number]"
```

### Create feature branch
```bash
git checkout -b feature/short-description
```

### Commit with convention
```bash
git commit -m "type(scope): description"
# Types: feat, fix, docs, test, refactor, devops, chore
```

### Create PR
```bash
gh pr create --title "feat(scope): description" --body "Closes #123"
```

---

## Sprint Cadence (2-week sprints)

| Day | Activity | Duration |
|-----|----------|----------|
| Mon Week 1 | Sprint Planning | 2 hours |
| Daily | Standup (automated) | 15 min |
| Wed Week 1 | Backlog Refinement | 1 hour |
| Fri Week 2 | Sprint Review | 1 hour |
| Fri Week 2 | Sprint Retrospective | 45 min |

---

## Metrics to Track

- **Velocity:** Story points completed per sprint
- **Burndown:** Work remaining vs. time
- **Cycle Time:** Time from "In Progress" to "Done"
- **Code Coverage:** % of code tested
- **Bug Rate:** Bugs per story point
- **Review Time:** Time from PR to merge

---

## Questions?

- **Product questions:** Ask Product Owner
- **Process questions:** Ask Scrum Master
- **Technical questions:** Ask in team channel
- **Blockers:** Report in daily standup

---

**Remember:** Scrum is about continuous improvement. Adapt this process to what works best for your team!

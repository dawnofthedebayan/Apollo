---
title: Apollo Knowledge Base
type: project
project-id: "#project/apollo"
status: planning
priority: medium
start-date: 23.05.2026
target-date: ""
completed-date: ""
tags:
  - project
  - horizon/mid-term
---

# Project Name

> [!NOTE] Project Control Tower
> This is the single source of truth for this project. Change the `project-id` in the properties above to automatically pull in related notes.

---

## 🎯 Goal & Success Criteria

**What does done look like?**

**Why does this matter?**

**Success looks like:**
- [ ] Agent can generate quiz for me where it just looks at 05-idea
- [ ] 
- [ ] 

---

## 🗺️ Scope

**In scope:**
- 

**Out of scope:**
- 

---

## 📋 Task Board

### 🔥 Active
- [ ] 

### ⏳ Up Next
- [ ] 

### ✅ Done
- [ ] 

---

## 🔁 Progress Log

| Date | Update |
|------|--------|
|  | Project initialized |

---

## 🧱 Blockers

- 

---

## 💡 Ideas & Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
|  |  |  |

---

## 👥 Stakeholders & Resources

| Name | Role | Notes |
|------|------|-------|
|  |  |  |

---

## 🔗 Linked Notes

*(These tables automatically update when you tag other notes with this project's unique `project-id`)*

### 📓 Journals
```dataview
TABLE week AS Week, area AS Area
FROM "01-journals"
WHERE contains(file.tags, this.project-id) OR contains(tags, this.project-id)
SORT file.name DESC
```

### 📚 References
```dataview
TABLE type AS Type, status AS Status, rating AS Rating
FROM "03-references"
WHERE contains(file.tags, this.project-id) OR contains(tags, this.project-id)
SORT file.name ASC
```

### 🧑 People
```dataview
TABLE role AS Role, company AS Company, last-contact AS "Last Contact"
FROM "04-people"
WHERE contains(file.tags, this.project-id) OR contains(tags, this.project-id)
SORT last-contact DESC
```

### 🌳 Evergreen Ideas
```dataview
TABLE maturity AS Maturity, certainty AS Certainty
FROM "05-evergreen"
WHERE contains(file.tags, this.project-id) OR contains(tags, this.project-id)
SORT file.mtime DESC
```

### 📥 Inbox Captures
```dataview
TABLE priority AS Priority, created AS Date
FROM "00-inbox"
WHERE (contains(file.tags, this.project-id) OR contains(tags, this.project-id)) AND processed = false
SORT priority DESC
```

### 📁 Files & External Links
```dataview
TABLE Date
FROM ""
WHERE (contains(file.tags, this.project-id) OR contains(tags, this.project-id)) AND (type = "file" OR type = null)
SORT file.mtime DESC
```

---

## 🤖 LLM Prompt Seed

> Summarise the current state of this project, identify blockers, and suggest the next 3 actions.
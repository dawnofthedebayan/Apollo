---
title: "<% tp.config.target_file.basename %>"
type: "person"
relationship: "<%* tR += await tp.system.suggester(['colleague','collaborator','mentor','contact','friend','lead','investor','founder','creator','researcher'], ['colleague','collaborator','mentor','contact','friend','lead','investor','founder','creator','researcher'], false, 'Relationship type?'); %>"
context: "<%* const areas = ['finance','coding','ai-ml','real-estate','music','content','personal','research','reading']; tR += await tp.system.suggester(areas, areas, false, 'How do you know them?'); %>"
status: "<%* tR += await tp.system.suggester(['active','dormant','to-contact','met-once','following'], ['active','dormant','to-contact','met-once','following'], false, 'Relationship status?'); %>"
company: ""
role: ""
location: ""
email: ""
linkedin: ""
twitter: ""
website: ""
first-met: ""
last-contact: <% tp.date.now("YYYY-MM-DD") %>
tags: [people]
related-projects: []
llm-summary: ""
created: <% tp.date.now("YYYY-MM-DD") %>
---

# <% tp.config.target_file.basename %>

> [!INFO] Person Dossier · Added <% tp.date.now("YYYY-MM-DD") %>

---

## 🧑 Who Are They?

**Role / Title:**
**Company / Org:**
**Location:**

<!-- 2–3 sentences on who this person is and why they're in your vault -->

---

## 🔗 How We're Connected

- **Met via:**
- **Context:**
- **Mutual contacts:** 

---

## 💡 What They're Working On

<!-- Their current projects, interests, focus areas -->
- 

---

## 🗣️ Key Conversations

| Date | Medium | Summary |
|------|--------|---------|
| <% tp.date.now("YYYY-MM-DD") %> |  |  |

---

## 🧠 Their Ideas & Perspectives

<!-- Notable opinions, frameworks, or insights they've shared -->
- 

---

## ❓ Ask Them About

<!-- Things to bring up next time you interact -->
- [ ] 
- [ ] 

---

## 📎 Their Work & Resources

<!-- Links to their articles, tools, repos, videos -->
- 

---

## 🤝 How I Can Help Them

<!-- Reciprocity — what value can you offer? -->
- 

---

## 🔁 Follow-Up

- [ ] 
- **Next contact date:**

---

## 🤖 LLM Prompt Seed

> Summarise this person's background and suggest talking points based on their work in: 

---
*Created <% tp.date.now("YYYY-MM-DD") %> · [[04-people]]*
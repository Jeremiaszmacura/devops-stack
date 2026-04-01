---
name: debuging-errors
description: While debugging errors, spawn new Claude SubAgent with own context to resolve the issue.
---

When you face an issue:
* prepare all context data needed to resolve the issue in separate Claude Code context/subagent
* spawn new Claude SubAgent with the prepared context to resolve the issue
* When subagent finish the debuging, it should fix the issue and provide a detailed report of the changes made to resolve the issue, including any code changes, configuration updates, or other modifications. The report should also include an explanation of the root cause of the issue and how it was resolved.
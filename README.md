# TriageAssist

An LLM agent for clinical-intake triage: it takes a description of symptoms, asks
clarifying follow-up questions, and returns a triage recommendation (self-care,
see a doctor, urgent, or emergency) behind explicit safety guardrails.

> **This is a portfolio project, not a medical device.** It does not diagnose and
> is not a substitute for professional medical advice. See the safety section of
> this README (written at the end of the build) for what the guardrails do and
> do not guarantee.

Built incrementally — the commit history walks through each layer, from the
FastAPI skeleton to the agent loop, RAG retrieval, safety evals, React frontend,
and deployment.

**Full README, architecture diagram, and live demo link land at the end of the build.**

# 🧭 LLM‑Assisted Project Kickoff Checklist

A minimal, repeatable workflow for starting new software projects with the help of a Large Language Model (LLM).  
The goal is to keep projects structured, modular, and easy to reason about from day one.

---

## 1. Define the Problem
- Write 1–2 sentences describing what you want to build.
- Ask the LLM to restate the problem clearly and surface hidden assumptions or constraints.

---

## 2. Map the Domain
- Ask the LLM: **"What are the key entities, relationships, and invariants in this domain?"**
- Review and confirm the domain model until it matches your understanding.

---

## 3. Define the Architecture
- Ask the LLM: **"Given this domain model, propose a minimal modular architecture."**
- Keep only the modules that are essential.
- Ensure each module has a single responsibility.

---

## 4. Implement Modules One by One
- Ask the LLM: **"Implement module X based on the architecture and domain model."**
- Keep modules pure, testable, and independent.
- Avoid premature integration.

---

## 5. Test Each Module
- Ask the LLM: **"Give me minimal tests or synthetic examples for this module."**
- Validate correctness before moving on.

---

## 6. Integrate Into a Small End‑to‑End Flow
- Ask the LLM: **"Show a minimal script that runs the main workflow using these modules."**
- Run the system with real data.
- Confirm the architecture holds under real‑world conditions.

---

## 📝 Notes
- This workflow keeps the LLM focused on **structure first**, **code second**.
- It prevents premature coding and avoids architectural drift.
- It works for small utilities, large systems, and everything in between.
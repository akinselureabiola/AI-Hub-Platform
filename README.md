# AI Hub Platform

## Overview

AI Hub Platform is a modular AI platform that brings together multiple AI-powered applications into a single workspace.

Instead of building standalone AI tools that solve one problem at a time, the goal of this project is to create a central platform where users can access different AI assistants from one dashboard. Each assistant is designed to solve practical business and IT problems while sharing the same authentication, infrastructure, and backend services.

This project is being built incrementally, with each module representing a real-world use case and an opportunity to explore modern software engineering practices, cloud infrastructure, and AI integration.

---

## Why I Started This Project

Over the last couple of years, I've built several independent AI applications, including an ATS Resume Assistant and an AI IT Support Copilot. As those projects grew, I realised maintaining separate applications wasn't scalable.

Rather than continuing to build isolated tools, I decided to create a single platform where multiple AI applications can live under one architecture while sharing authentication, database services, and a consistent user experience.

The project is also helping me strengthen my understanding of modern web development, cloud technologies, software architecture, and enterprise application design.

---

## Current Features

Current progress includes:

* Modern Next.js application structure
* Supabase integration
* Backend architecture
* Shared authentication foundation
* Centralised project structure
* Documentation and system design
* Responsive landing page
* Vercel deployment
* ATS Resume Assistant API Integration (MVP)

---

## Planned AI Modules

The platform is designed to support multiple AI applications, including:

### ATS Resume Assistant

* ATS resume analysis
* Resume tailoring
* Cover letter generation
* Job description matching
* DOCX export

### AI IT Support Copilot

* Incident classification
* Guided troubleshooting
* Root Cause Analysis
* Ticket escalation recommendations
* Knowledge base integration

### Software Testing Assistant

* AI-generated Pytest test cases
* Test coverage suggestions
* Unit testing assistance
* Mock generation
* Testing documentation

Additional AI modules will be added as the platform evolves.

---

## Technology Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Backend

* Supabase
* PostgreSQL
* Server Actions
* Authentication Middleware

### AI

* OpenAI
* LangGraph

### Deployment

* Vercel
* Cloudflare
* GitHub

---

## Project Structure

```text
AI-Hub-Platform/

app/
components/
lib/
public/
docs/

README.md
package.json
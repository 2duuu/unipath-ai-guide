## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>

# Checkout the landing_page branch
git checkout landing_page
```

---

# 🎓 UniHub - AI-Powered Academic Guidance Platform

![UniHub](https://img.shields.io/badge/Status-Active%20Development-green)
![License](https://img.shields.io/badge/License-Proprietary-red)
![Tech Stack](https://img.shields.io/badge/Stack-React%20%7C%20FastAPI%20%7C%20SQLite-blue)

> **Empowering Romanian students to make informed university choices through AI-driven insights and personalized guidance.**

---

## 📖 Table of Contents

- [Overview](#overview)
- [What We've Built](#what-weve-built)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Current Status](#current-status)
- [Future Roadmap](#future-roadmap)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**UniHub** is an innovative web platform designed to help Romanian high school students navigate the complex landscape of university admissions. By combining AI-powered recommendations, comprehensive university data, and an intuitive user experience, we make the process of choosing the right academic path accessible and stress-free.

### The Problem We're Solving

Romanian students face numerous challenges when selecting universities:
- **Information overload**: 150+ universities with thousands of programs
- **Unclear fit**: Difficulty matching personal interests with program requirements
- **Limited guidance**: Lack of personalized counseling and insights
- **Admission complexity**: Confusing requirements, deadlines, and procedures

### Our Solution

UniHub provides:
- 🤖 **AI-driven matching** based on student profiles, interests, and academic performance
- 📊 **Comprehensive data** on 150+ universities and programs across Romania
- 🎯 **Personalized recommendations** with compatibility scoring
- 📝 **Application support** including motivation letters, CV prep, and deadline tracking
- 💬 **Expert guidance** through AI chat and 1-on-1 counseling (premium tiers)

---

## 🏆 What We've Built

### Current Implementation (v1.0)

#### Frontend (React + TypeScript)
- ✅ **Modern, responsive UI** with Tailwind CSS and shadcn/ui components
- ✅ **Complete page structure**:
  - Landing page with hero, features, testimonials, pricing
  - Interactive career quiz (initial + extended)
  - University/program browse & search with filters
  - User authentication (login/signup)
  - Account dashboard with quiz results and package management
  - Package system with 3 tiers (Free, Decision & Clarity, Application Prep, Guided Support)
  - Contact page
- ✅ **Multi-language support** (fully translated from Romanian to English)
- ✅ **Package/subscription system** with feature gating
- ✅ **PDF report generation** for quiz results
- ✅ **Smooth animations** with Framer Motion

#### Backend (FastAPI + Python)
- ✅ **RESTful API** with FastAPI
- ✅ **Authentication system** (JWT-based)
- ✅ **SQLite database** with SQLAlchemy ORM
- ✅ **Quiz system**:
  - Initial quiz (7 core variables)
  - Extended interview (45+ questions)
- ✅ **Deterministic matching engine** (100-point scoring)
- ✅ **Package management API** with tier-based features
- ✅ **Database seeding scripts** for Romanian universities

#### Data Infrastructure
- ✅ **11 major Romanian universities** (UB, UPB, ASE, UTCN, UBB, etc.)
- ✅ **36+ academic programs** across multiple fields
- ✅ **Admission criteria** (cutoff scores, requirements)
- ✅ **University metadata** (location, ranking, facilities)

---

## 🎯 Key Features

### For Students

| Feature | Free | Decision & Clarity | Application Prep | Guided Support |
|---------|------|-------------------|------------------|----------------|
| Core Academic Quiz | ✅ | ✅ | ✅ | ✅ |
| University Recommendations | ✅ | ✅ | ✅ | ✅ |
| Advanced AI Comparisons | ❌ | ✅ | ✅ | ✅ |
| Ranked Recommendations | ❌ | ✅ | ✅ | ✅ |
| Trade-off Analysis | ❌ | ✅ | ✅ | ✅ |
| Admission Probability | ❌ | ✅ | ✅ | ✅ |
| PDF Summary Download | ❌ | ✅ | ✅ | ✅ |
| Unlimited AI Chat | ❌ | ✅ | ✅ | ✅ |
| Application Strategy | ❌ | ❌ | ✅ | ✅ |
| Deadline Timeline | ❌ | ❌ | ✅ | ✅ |
| Motivation Letter Training | ❌ | ❌ | ✅ | ✅ |
| CV Training | ❌ | ❌ | ✅ | ✅ |
| AI Document Feedback | ❌ | ❌ | ✅ | ✅ |
| 1-on-1 Video Counseling | ❌ | ❌ | ❌ | ✅ |
| Human Expert Guidance | ❌ | ❌ | ❌ | ✅ |
| Document Verification | ❌ | ❌ | ❌ | ✅ |
| Submission Prep Support | ❌ | ❌ | ❌ | ✅ |
| Deadline Tracking & Reminders | ❌ | ❌ | ❌ | ✅ |
| Peer Insight Sessions | ❌ | ❌ | ❌ | ✅ (Bonus) |

### Pricing
- **Free**: €0 - Basic quiz and recommendations
- **Decision & Clarity**: €36.30 - AI-powered decision support
- **Application Prep**: €121 - Full application guidance
- **Guided Support**: €484 - Premium human-assisted support

---

## 🛠 Technology Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **UI Library**: shadcn/ui (Radix UI primitives)
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: Axios
- **State Management**: React Context + TanStack Query
- **PDF Generation**: jsPDF

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLite + SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Data Validation**: Pydantic v2
- **Testing**: pytest + pytest-cov
- **PDF Generation**: ReportLab

### Future AI/LLM Integration
- **Planned**: OpenAI GPT-4, Anthropic Claude, or Langchain
- **Use Cases**: Advanced matching, personalized explanations, chat support

### DevOps & Tools
- **Version Control**: Git
- **Package Manager**: npm (frontend), pip (backend)
- **Development**: Hot reload (Vite + Uvicorn)
- **Code Quality**: ESLint, TypeScript strict mode

---

## 🏗 Project Architecture

```
unipath-ai-guide/
├── frontend (React app)
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Route pages (Account, Quiz, etc.)
│   │   ├── contexts/       # React contexts (Auth)
│   │   ├── services/       # API clients
│   │   ├── lib/            # Utilities (packages, utils)
│   │   ├── hooks/          # Custom React hooks
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Helper functions
│   ├── public/             # Static assets
│   ├── index.html          # Entry HTML
│   ├── package.json        # Node dependencies
│   └── vite.config.ts      # Vite config
│
├── backend/ (FastAPI API)
│   ├── src/
│   │   ├── database.py     # SQLAlchemy models
│   │   ├── api.py          # FastAPI routes
│   │   ├── auth.py         # Authentication logic
│   │   ├── models.py       # Pydantic models
│   │   ├── packages.py     # Package/tier management
│   │   ├── interview_system.py  # Quiz logic
│   │   ├── matching_engine.py   # Matching algorithm
│   │   └── db_query.py     # Database queries
│   ├── scripts/            # Database seeding
│   ├── tests/              # Backend tests
│   ├── docs/               # Backend documentation
│   ├── data/               # SQLite database
│   ├── requirements.txt    # Python dependencies (core)
│   └── api_requirements.txt # Python dependencies (API)
│
├── README.md               # This file
├── INSTRUCTIONS.md         # Setup & run guide
└── package.json            # Root workspace config
```

---

## 📊 Current Status

### ✅ Completed Features
- Frontend UI/UX (100%)
- Authentication system (100%)
- Quiz system (initial + extended, 100%)
- Package/subscription system (100%)
- University database (11 universities, 36 programs)
- Basic matching algorithm (100%)
- PDF export (100%)
- Multi-language support (English, 100%)
- Responsive design (mobile/tablet/desktop, 100%)

### 🚧 In Progress
- Payment gateway integration (Stripe/PayPal)
- Email notifications (welcome, reminders)
- Admin dashboard for content management

### ⏳ Planned (See Roadmap)
- AI/LLM integration for advanced matching
- Real-time chat support
- Application document templates
- Video counseling scheduling system
- Peer review forum

---

## 🚀 Future Roadmap

### Phase 1: AI/LLM Integration (Q2 2026)
**Goal**: Replace deterministic matching with LLM-powered semantic analysis

#### Key Objectives
1. **LLM-Based Matching Engine**
   - Train/fine-tune model on student-university fit data
   - Semantic analysis of student profiles vs. program descriptions
   - Generate natural language explanations for recommendations
   - Predict admission probability using historical data

2. **Conversational AI Chat**
   - Unlimited chat for premium users
   - Answer questions about universities, programs, admissions
   - Provide personalized advice and clarifications
   - Context-aware responses based on user profile

3. **Document Review AI**
   - Analyze motivation letters and CVs
   - Provide specific feedback and improvement suggestions
   - Check for common mistakes and formatting issues
   - Score documents based on admission criteria

#### Technical Implementation
- **Framework**: Langchain + OpenAI GPT-4 or Anthropic Claude
- **Vector Database**: Pinecone or Chroma for university/program embeddings
- **Fine-tuning**: Collect user feedback to improve recommendations
- **RAG (Retrieval-Augmented Generation)**: Combine database queries with LLM reasoning

### Phase 2: Enhanced Data & Expansion (Q3 2026)
- Expand to 150+ universities (complete Romanian coverage)
- Add 500+ programs across all fields
- Integrate real-time admission statistics
- Alumni success stories and career outcomes
- Scholarship and financial aid information

### Phase 3: Application Platform (Q4 2026)
- Integrated application submission (where supported)
- Document upload and verification
- Application status tracking
- Deadline calendar with reminders
- Video counseling platform with booking system

### Phase 4: Community & Social (Q1 2027)
- Student forum and peer discussions
- University student ambassadors
- Q&A with current students
- Success stories and testimonials
- Study group formation

### Phase 5: Analytics & Insights (Q2 2027)
- Admin analytics dashboard
- University ranking algorithm
- Trend analysis (popular programs, admission rates)
- Predictive modeling for admission outcomes
- ROI analysis for different programs

---

## 🎯 Getting Started

For detailed setup instructions, see **[INSTRUCTIONS.md](./INSTRUCTIONS.md)**.

Quick start:
```bash
# Install dependencies
npm install

# Start frontend (development)
npm run dev

# Start backend API
cd backend
python -m uvicorn src.api:app --reload
```

Visit: http://localhost:3001 (frontend) and http://localhost:8000 (API)

---

## 📚 Documentation

- **[INSTRUCTIONS.md](./INSTRUCTIONS.md)** - Setup and run guide
- **[backend/docs/README.md](./backend/docs/README.md)** - Backend documentation
- **[backend/docs/MVP_README.md](./backend/docs/MVP_README.md)** - MVP user guide
- **[backend/docs/DATABASE_README.md](./backend/docs/DATABASE_README.md)** - Database schema
- **[PACKAGE_QUICK_REFERENCE.md](./PACKAGE_QUICK_REFERENCE.md)** - Package system reference

---

## 🤝 Contributing

This is a private project currently in active development. Contributions are limited to the core team.

### Development Workflow
1. Create a feature branch from `main`
2. Make changes and test thoroughly
3. Submit a pull request with clear description
4. Code review and merge

### Code Standards
- TypeScript strict mode enabled
- ESLint for code quality
- Consistent formatting with Prettier
- Component-driven architecture
- Test coverage for critical paths

---

## 📄 License

**Proprietary** - All rights reserved. This project is not open source and may not be reproduced, distributed, or used without explicit permission.

---

## 📞 Contact

For questions, feedback, or support:
- **Email**: contact@unihub.ro
- **Phone**: +40 721 234 567
- **Location**: Bucharest, Romania

---

## 🎉 Acknowledgments

Built with ❤️ by the UniHub team to empower Romanian students in their academic journey.

**Powered by:**
- React + TypeScript
- FastAPI + Python
- shadcn/ui + Tailwind CSS
- OpenAI / Anthropic (coming soon)

---

**Last Updated**: January 23, 2026  
**Version**: 1.0.0

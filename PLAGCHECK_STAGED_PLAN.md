# PlagCheck-Django Staged Product Plan

## Current Product Status

The current repository is a prototype for a plagiarism-checking web app built around three working flows:

- User registration and login with OTP email verification.
- Folder and file management for authenticated users, including PDF-to-text extraction.
- Folder-based text similarity analysis with downloadable CSV reports.

What is already present in code:

- User signup, OTP verification, login, logout, and a landing page.
- File upload into folders, including multiple file upload support.
- Basic PDF OCR/text extraction into stored text files.
- Similarity report generation using TF-IDF and cosine similarity.
- Report viewing, deletion, and CSV export.

What is still missing for a robust academic plagiarism platform:

- Clear professor/TA/admin role separation.
- Assignment, course, submission, and review workflows.
- Batch review queues, prioritization, and triage.
- Human-in-the-loop feedback, override, and decision tracking.
- Audit logs, case notes, and evidence management.
- Scalable similarity pipeline, plagiarism explanation, and review assistance.
- Rich UX for progress, pausing, partial completion, and fast-track review.

---

## Stage 1: Business Analyst Feature Blueprint

### Product Intent

Build a plagiarism and similarity review platform that helps professors and teaching assistants move from raw submissions to fair, documented decisions with less manual effort and more confidence.

### Core Personas

#### Professor

- Wants quick visibility into suspicious submissions across one or more assignments.
- Needs confidence that the system is fair, explainable, and easy to defend.
- Wants to reduce repetitive manual comparison work.
- Needs summary-level control with the ability to drill down only when necessary.

#### Teaching Assistant

- Needs a fast triage workflow for many submissions.
- Wants to review flagged cases, annotate findings, and pass edge cases upward.
- Needs a queue that supports urgency, severity, and due-date based prioritization.

#### Student, indirectly

- Needs a predictable, transparent process.
- Benefits from clear submission expectations and evidence-based outcomes.

#### Department or Program Admin

- Needs governance, reporting, and policy consistency across courses.
- Wants archival, search, and auditability.

### Business Outcomes

- Reduce time spent on manual comparison.
- Increase consistency in plagiarism review decisions.
- Provide evidence-rich, defensible review outcomes.
- Make the workflow understandable to non-technical faculty staff.
- Support reuse across courses and semesters.

### Complete Feature Catalog

#### A. Identity, Access, and Roles

- Email and OTP-based onboarding.
- Role-based access control for professor, TA, admin, and optional student view.
- Department or course-scoped permissions.
- Account verification status and recovery paths.
- Profile settings for contact information and notification preferences.

#### B. Course and Assignment Management

- Create courses, terms, and sections.
- Create assignments with due dates, submission rules, and policy thresholds.
- Attach rubrics, policy notes, and instructor guidance.
- Reuse templates across semesters.
- Archive old courses while preserving reports and evidence.

#### C. Submission Intake

- Upload single or multiple files.
- Bulk upload by folder, assignment, or course.
- Drag-and-drop upload with progress tracking.
- Accepted file types: PDF, DOCX, TXT, and optionally images with OCR.
- Auto-parse metadata such as filename, uploader, timestamp, and source assignment.
- Detect duplicate uploads and versioned resubmissions.

#### D. Text Extraction and Normalization

- OCR for scanned PDFs.
- Text extraction from digital PDFs and documents.
- Normalize whitespace, hyphenation, punctuation, and encoding.
- Language detection and optional multilingual handling.
- Store extracted text separately from original uploads.
- Preserve extraction quality indicators and failure reasons.

#### E. Similarity and Plagiarism Detection

- Compare submission against all files in an assignment, course, or selected folder.
- Pairwise similarity scoring.
- Threshold-based flagging.
- Multiple detection modes:
  - exact match detection
  - near-duplicate detection
  - paraphrase or semantic similarity detection
  - code similarity detection if needed later
- Highlight matching segments and overlap regions.
- Explain why a pair is flagged, not just the score.
- Support comparison with internal corpus, previous semesters, and optional external sources.

#### F. Review Queue and Triage

- Queue flagged submissions by score, assignment, due date, or course.
- Sort by highest risk, most urgent, or least reviewed.
- Mark items as new, in review, needs escalation, cleared, or confirmed.
- Assign cases to a TA or professor.
- Pause and resume review work without losing state.
- Fast-track low-risk items and hold suspicious ones for deeper review.

#### G. Human-in-the-Loop Decisioning

- Add comments, notes, and rationale on each case.
- Recommend an action: clear, warn, escalate, or investigate further.
- Allow override of system recommendations.
- Capture reviewer identity and timestamps.
- Add second-review approval for severe cases.
- Maintain a decision history for accountability.

#### H. Evidence and Case Management

- Show side-by-side file comparison.
- Sentence-level or paragraph-level evidence markers.
- Evidence snapshots and exported case packets.
- Case status timeline.
- Attach internal notes and external references.
- Export report as PDF, CSV, or shareable review summary.

#### I. Reporting and Analytics

- Course-level summary dashboard.
- Assignment-level risk heatmap.
- Trend analysis across semesters.
- Reviewer workload and throughput analytics.
- False positive review metrics and threshold tuning insights.
- Exportable compliance and audit reports.

#### J. Collaboration and Communication

- Reviewer assignment and handoff.
- Internal comments and mention-based collaboration.
- Optional student notification workflow.
- Escalation requests and professor sign-off.
- Templated communications for consistent messaging.

#### K. Search and Discovery

- Search by student, filename, assignment, course, similarity score, or status.
- Filter by reviewer, date range, flag severity, and decision outcome.
- Save common views.
- Quick access to recent and high-priority cases.

#### L. Security, Compliance, and Governance

- Full audit logs.
- Permissioned access to evidence and outcomes.
- Data retention settings.
- Secure file storage and encryption expectations.
- Activity history for every key action.

#### M. Platform and Reliability

- Background processing for OCR and similarity jobs.
- Job progress and retry handling.
- Failure recovery and visible error states.
- Scalable queue-based processing.
- Performance monitoring and alerting.

### Priority Tiers

#### Must Have

- Role-based access.
- Course and assignment structure.
- File upload and text extraction.
- Similarity detection and report generation.
- Review queue with status tracking.
- Evidence view and export.
- Audit trail.

#### Should Have

- Assignment templates.
- Annotated comparison view.
- Reviewer assignment and escalation.
- Dashboards and filters.
- Background job management.

#### Could Have

- Semantic similarity and paraphrase detection.
- External corpus checks.
- Multilingual OCR and translation support.
- Advanced analytics and ML-assisted review cues.

### Non-Functional Requirements

- Fast perceived response time for upload and review.
- Reliable background processing for OCR and comparisons.
- Strong permissioning and data isolation.
- Clear accessibility and keyboard navigation.
- Mobile-friendly review for light tasks.
- Traceable and testable business decisions.

---

## Stage 2: Project Delivery Council Plan

### Current Status Assessment

The app is functionally real but architecturally early-stage. It has working endpoints and models, but the domain is still organized around folders/files rather than academic workflow objects like courses, assignments, submissions, and review cases.

### Key Gaps To Close

- Replace folder-first thinking with course-assignment-submission thinking.
- Introduce background jobs for OCR and similarity scoring.
- Add status-driven review flows.
- Separate data ingestion from review and decision layers.
- Add dashboards and operational visibility.

### Suggested Implementation Architecture

#### Domain Layer

- Users and roles.
- Courses.
- Assignments.
- Submissions.
- Review cases.
- Evidence items.
- Decisions and audit events.

#### Processing Layer

- File ingestion service.
- Text extraction service.
- Similarity engine.
- Report generation service.
- Notification service.

#### Presentation Layer

- Professor dashboard.
- TA review queue.
- Assignment details.
- Submission comparison page.
- Reports and analytics.

### Stage-wise Delivery Roadmap

#### Phase 1: Foundation

- Stabilize authentication and roles.
- Introduce course and assignment data models.
- Refactor uploads to attach to assignments.
- Preserve current file manager features as a transitional layer.

#### Phase 2: Core Review Workflow

- Build submission intake around assignments.
- Move extraction and similarity to background jobs.
- Create review cases from similarity output.
- Add queue, status, and assignment of cases.

#### Phase 3: Reviewer Experience

- Add evidence-rich comparison screens.
- Add notes, decisions, and escalation.
- Introduce filters, saved views, and fast-track actions.

#### Phase 4: Reporting and Governance

- Build dashboards and analytics.
- Add audit logs and export formats.
- Add retention and policy controls.

#### Phase 5: Scale and Intelligence

- Add semantic similarity enhancements.
- Improve performance and job orchestration.
- Add proactive review recommendations.

### Delivery Principles

- Protect the current working prototype while refactoring gradually.
- Add new abstractions without forcing a big-bang rewrite.
- Make every new feature observable, testable, and reviewable.
- Favor workflows over raw technical controls.

---

## Stage 3: UI/UX Design Direction

### Design Goal

Create a review environment that feels calm, guided, and highly efficient for professors and TAs. The interface should reduce cognitive load, reveal the right detail at the right time, and support human judgment rather than replacing it.

### Experience Principles

- Show progress clearly at every stage.
- Keep the primary action visible when users need it.
- Let users pause, save, fast-track, or escalate without losing context.
- Treat review work as a guided flow, not a static page.
- Surface confidence, risk, and evidence together.
- Avoid forcing users into technical jargon.

### Suggested Information Architecture

- Home dashboard.
- Courses.
- Assignments.
- Uploads and submissions.
- Review queue.
- Cases and evidence.
- Reports and analytics.
- Settings and governance.

### Key Screens And Flows

#### 1. Onboarding and Role Setup

- Sign up or invite flow.
- Role selection or assignment.
- Verification and organization setup.
- First-run checklist.

#### 2. Professor Dashboard

- High-priority flagged items.
- Assignment health overview.
- Recent uploads and pending reviews.
- Actions for creating assignments and launching checks.

#### 3. TA Review Queue

- Ordered review cards with severity, score, and status.
- One-click triage actions.
- Filters for course, due date, and risk level.
- Queue progress indicator.

#### 4. Submission Comparison View

- Side-by-side document display.
- Highlighted matches and evidence markers.
- Similarity summary and confidence indicators.
- Reviewer notes panel.
- Actions: clear, escalate, mark for follow-up, save and continue.

#### 5. Case Detail View

- Case timeline.
- Decision history.
- Comments and attachments.
- Export and handoff controls.

#### 6. Reports Dashboard

- Assignment-level and course-level summaries.
- Trends over time.
- Reviewer workload and throughput.
- Export controls.

### Interaction Patterns

- Persistent top-level status chips for case state.
- Progress bars for uploads, extraction, and scoring.
- Step-based review with save-and-resume.
- Inline feedback at every major action.
- Empty states that explain what to do next.
- Confirmations only for destructive actions.

### Human Loop Features

- Pause review and resume later.
- Fast-track low-risk cases.
- Escalate uncertain cases.
- Add reviewer notes at every stage.
- Show what the system saw and why it flagged it.
- Allow override of automated suggestions.

### Visual Direction

- Clear academic, editorial feel rather than a generic admin dashboard.
- Strong typography hierarchy.
- Subtle data emphasis, not visual noise.
- Dense information on desktop, simplified flow on smaller screens.
- Calm, trustworthy color system with strong status semantics.

---

## Stage 4: Delivery Plan For Two Developers

### Team Split

#### Developer A: AI and Backend

- Data models and migrations.
- OCR and extraction pipeline.
- Similarity engine and scoring logic.
- Background jobs and APIs.
- Reports, exports, and audit logging.

#### Developer B: Frontend

- Dashboard and review UI.
- Upload and queue screens.
- Comparison views and interaction states.
- Responsive layout and accessibility.
- Frontend state, loading, empty, and error states.

### Weekly Sprint Plan

#### Sprint 1

- Align domain model for courses, assignments, submissions, and review cases.
- Define API contracts.
- Sketch dashboard and queue layout.
- Preserve the current file-based flow while introducing the new structure.

#### Sprint 2

- Implement course and assignment models.
- Build upload submission endpoints.
- Create the first professor dashboard shell.
- Add authentication and role checks.

#### Sprint 3

- Move text extraction into a background process.
- Build similarity job execution and result persistence.
- Create queue cards and case list UI.
- Add loading and progress feedback.

#### Sprint 4

- Build case detail and evidence comparison screens.
- Add reviewer notes and status transitions.
- Add export and report views.
- Wire frontend actions to backend review state.

#### Sprint 5

- Add analytics and operational reporting.
- Add audit logs and history views.
- Polish empty states, error states, and confirmations.
- Conduct usability review with professor/TA scenarios.

#### Sprint 6

- Harden permissions and edge cases.
- Optimize performance and job reliability.
- Add cleanup and archival flows.
- Prepare release candidate and documentation.

### Coordination Rules

- Backend changes should expose simple, stable contracts early.
- Frontend should be built against mocked data first, then connected.
- Each sprint should end with one complete, reviewable user journey.
- Avoid building advanced intelligence before the core review loop is usable.

---

## Recommended Next Artifact

If this document becomes the working source of truth, the next practical step is to convert the Stage 1 feature catalog into a prioritized backlog and a data model proposal.
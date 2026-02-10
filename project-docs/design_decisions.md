# Project Design Decisions - Athlete Management Application

> [!NOTE]
> This document captures key architectural and design decisions made during the planning phase. It serves as a reference for understanding **why** certain choices were made.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Decisions](#architecture-decisions)
4. [Data Model Design](#data-model-design)
5. [Invoice System](#invoice-system)
6. [Workout Tracking](#workout-tracking)
7. [Authentication & Authorization](#authentication--authorization)
8. [UI/UX Design](#uiux-design)
9. [Deployment Strategy](#deployment-strategy)
10. [Future Considerations](#future-considerations)

---

## Project Overview

**Purpose**: Build a comprehensive athlete management system for running and triathlon coaching with automated billing, workout tracking, and payment management.

**Core Objectives**:
1. Streamline payment tracking and invoice generation
2. Enable athletes to view and track their workouts
3. Provide coaches with efficient athlete management tools
4. Lay foundation for future analytics and insights

**Target Users**:
- **Primary**: Coach (Mehul Ved) - Admin interface
- **Secondary**: Athletes - Custom athlete portal

---

## Technology Stack

### Backend: Django

**Decision**: Use Django as the web framework

**Rationale**:
- ✅ **Batteries included**: Built-in admin interface, ORM, authentication
- ✅ **Rapid development**: Quick to prototype and iterate
- ✅ **Mature ecosystem**: Extensive packages for PDF generation, email, etc.
- ✅ **Python**: Familiar language, easy to maintain
- ✅ **Scalable**: Can handle growth from single coach to multi-coach platform

**Alternatives Considered**:
- Flask: Too minimal, would require more custom code
- FastAPI: Better for APIs, but we need full-stack framework
- Ruby on Rails: Less familiar, smaller ecosystem in India

### Database: PostgreSQL

**Decision**: Use PostgreSQL as the primary database

**Rationale**:
- ✅ **Robust**: ACID compliance, data integrity
- ✅ **JSON support**: Flexible for invoice line items, metadata
- ✅ **Free tier available**: Railway, Render support PostgreSQL
- ✅ **Future-ready**: Can add TimescaleDB extension for time-series analytics
- ✅ **Django compatibility**: Excellent ORM support

**Alternatives Considered**:
- SQLite: Not suitable for production, limited concurrency
- MySQL: Less feature-rich than PostgreSQL
- MongoDB: Overkill for structured data, harder to maintain relationships

### Frontend: Django Templates + Vanilla CSS

**Decision**: Server-side rendering with Django templates, minimal JavaScript

**Rationale**:
- ✅ **Simplicity**: No complex build process, easier to maintain
- ✅ **SEO-friendly**: Server-rendered pages
- ✅ **Fast development**: No separate frontend/backend coordination
- ✅ **Responsive design**: CSS Grid + Flexbox for mobile/desktop
- ✅ **Progressive enhancement**: Add JavaScript only where needed

**Alternatives Considered**:
- React/Next.js: Overkill for this use case, adds complexity
- Vue.js: Still requires build process and API layer
- HTMX: Interesting but less mature, team unfamiliarity

---

## Architecture Decisions

### Monolithic Architecture

**Decision**: Build as a single Django monolith

**Rationale**:
- ✅ **Simplicity**: Single codebase, easier to develop and deploy
- ✅ **Faster development**: No microservices coordination overhead
- ✅ **Sufficient for scale**: Can handle hundreds of athletes easily
- ✅ **Lower costs**: Single server deployment
- ✅ **Easier debugging**: All code in one place

**When to Reconsider**: If scaling to 1000+ athletes or multi-tenant platform

### Responsive Web App (Not Native Mobile)

**Decision**: Build responsive web application, not native mobile apps

**Rationale**:
- ✅ **Single codebase**: Works on all devices via browser
- ✅ **No app store**: Immediate updates, no approval process
- ✅ **Lower development cost**: Don't need iOS + Android developers
- ✅ **Easier maintenance**: One codebase to update
- ✅ **PWA potential**: Can add offline support later if needed

**Trade-offs**:
- ❌ No push notifications (can use web push later)
- ❌ No native integrations (Strava/Garmin require web OAuth)

### Coach-Centric Admin Interface

**Decision**: Use Django admin for coach, custom portal for athletes

**Rationale**:
- ✅ **Time-saving**: Django admin is powerful out-of-the-box
- ✅ **Customizable**: Can extend admin for specific needs
- ✅ **Familiar**: Standard Django pattern
- ✅ **Focus resources**: Spend time on athlete-facing features

**Customizations Needed**:
- Custom admin actions (generate invoice, send email)
- Inline editing for related models
- Filters and search for quick access

---

## Data Model Design

### Separation of Concerns

**Decision**: Separate models for Athlete, Subscription, Payment, Invoice

**Rationale**:
- ✅ **Flexibility**: Athletes can change plans without losing history
- ✅ **Audit trail**: Complete payment and subscription history
- ✅ **Data integrity**: Clear relationships, no data duplication
- ✅ **Reporting**: Easy to query payments, subscriptions separately

### BillingPlan with HSN/SAC Codes

**Decision**: Add `service_level` (FOCUS/PERSONAL) and auto-generate HSN/SAC codes

**Rationale**:
- ✅ **Scalability**: Supports 8 different plan types
- ✅ **Automation**: HSN/SAC auto-generated from plan configuration
- ✅ **Flexibility**: Easy to add new plan types
- ✅ **Invoice accuracy**: Ensures correct HSN/SAC on every invoice

**HSN/SAC Format**: `{PLAN_TYPE}{SERVICE_LEVEL}{PERIOD}`
- Example: RUNFOCUS1MO, TRIPERSONAL1QTR

### Workout Status Tracking

**Decision**: Use `status` field (UPCOMING, COMPLETED, SKIPPED, RESCHEDULED) + `completion_quality` (EXCELLENT, GOOD, SATISFACTORY, STRUGGLED, INCOMPLETE)

**Rationale**:
- ✅ **Rich data**: Captures both completion and quality
- ✅ **Analytics-ready**: Can track adherence and performance trends
- ✅ **Coach insights**: Understand athlete struggles
- ✅ **Visual feedback**: Different colors for different states

**Why Separate Fields**:
- Status = What happened (completed, skipped, etc.)
- Quality = How well it went (only for completed workouts)

### JSONField for Invoice Line Items

**Decision**: Store line items as JSON array instead of separate LineItem model

**Rationale**:
- ✅ **Immutability**: Invoice is a snapshot, shouldn't change
- ✅ **Simplicity**: Easier to generate PDF from single object
- ✅ **Flexibility**: Can add custom fields without migrations
- ✅ **Performance**: Fewer database queries

**Format**:
```json
[{
  "description": "Running Focus - February 2026",
  "hsn_sac": "RUNFOCUS1MO",
  "quantity": 1,
  "rate": 5000,
  "amount": 5000
}]
```

---

## Invoice System

### GST Conditional Logic

**Decision**: Only charge GST if `company_gstin` is present and valid

**Rationale**:
- ✅ **Legal compliance**: Can't charge GST without GSTIN registration
- ✅ **Flexibility**: Supports both registered and unregistered businesses
- ✅ **Accurate invoicing**: Total reflects actual legal obligation
- ✅ **Future-proof**: Easy to add GSTIN later

**Implementation**:
```python
if company_gstin and len(company_gstin) == 15:
    # Calculate CGST + SGST (or IGST for inter-state)
    total = taxable_amount + gst_amount
else:
    # No GST
    total = taxable_amount
```

### Multiple Invoice Templates

**Decision**: Create 4 separate invoice templates (paid, unpaid, overdue, cancelled)

**Rationale**:
- ✅ **Clear communication**: Status immediately visible
- ✅ **Urgency**: Overdue invoices stand out
- ✅ **Professional**: Different messaging for different states
- ✅ **User experience**: Athletes know exactly what action to take

**Visual Differentiation**:
- Color-coded borders (green, yellow, red, gray)
- Status badges with icons
- State-specific messaging

### PDF Generation with ReportLab

**Decision**: Use ReportLab for PDF generation

**Rationale**:
- ✅ **Python-native**: Integrates well with Django
- ✅ **Powerful**: Full control over layout
- ✅ **Reliable**: Mature library, widely used
- ✅ **Customizable**: Can match brand design exactly

**Alternatives Considered**:
- WeasyPrint: HTML to PDF, but less control over layout
- wkhtmltopdf: External dependency, harder to deploy

### UPI Payment Option

**Decision**: Support both bank transfer and UPI ID for payments

**Rationale**:
- ✅ **Convenience**: UPI is fastest payment method in India
- ✅ **Adoption**: Most athletes use UPI daily
- ✅ **Simplicity**: Just share UPI ID (e.g., mved@ybl)
- ✅ **Instant**: Payments reflect immediately

**Implementation**: Add `bank_upi_id` field to InvoiceTemplate model

---

## Workout Tracking

### Calendar-Based View

**Decision**: Display workouts in monthly calendar format

**Rationale**:
- ✅ **Familiar**: Everyone understands calendars
- ✅ **Visual**: Easy to see patterns and gaps
- ✅ **Contextual**: See workouts in relation to dates
- ✅ **Navigation**: Simple month-to-month browsing

**Color Coding**: 7 different states with distinct gradients

### Workout Rescheduling

**Decision**: Allow athletes to reschedule workouts with `original_date` tracking

**Rationale**:
- ✅ **Flexibility**: Life happens, workouts need to move
- ✅ **Data integrity**: Preserve original plan for analytics
- ✅ **Transparency**: Coach can see rescheduling patterns
- ✅ **User experience**: Athletes feel empowered

**Implementation**: Store `original_date` when status changes to RESCHEDULED

### Completion Quality Ratings

**Decision**: Let athletes self-rate workout quality (EXCELLENT to STRUGGLED)

**Rationale**:
- ✅ **Athlete voice**: Captures subjective experience
- ✅ **Coach insights**: Understand when athletes struggle
- ✅ **Trend analysis**: Identify patterns in performance
- ✅ **Motivation**: Celebrate excellent workouts

**Why Self-Rating**: Athletes know their effort better than metrics alone

### Strava/Garmin Link Integration

**Decision**: Store external activity links (URL field) instead of full API integration

**Rationale**:
- ✅ **Simplicity**: No OAuth complexity
- ✅ **Flexibility**: Works with any platform (Strava, Garmin, Coros, etc.)
- ✅ **Privacy**: Athletes control what they share
- ✅ **Faster development**: No API rate limits or authentication

**Future Enhancement**: Full API integration for automatic sync

---

## Authentication & Authorization

### Django Built-in Auth

**Decision**: Use Django's built-in authentication system

**Rationale**:
- ✅ **Secure**: Battle-tested, industry standard
- ✅ **Complete**: User model, sessions, password reset
- ✅ **Extensible**: Easy to add custom fields
- ✅ **No dependencies**: Part of Django core

### Two User Types

**Decision**: Coach uses Django admin, athletes use custom portal

**Rationale**:
- ✅ **Security**: Separate interfaces, different permissions
- ✅ **UX**: Each interface optimized for its user
- ✅ **Simplicity**: No complex role-based access control needed

**Implementation**:
- Coach: `is_staff=True`, accesses `/admin/`
- Athlete: `is_staff=False`, accesses `/athlete/`

### Email-Based Login

**Decision**: Use email as username for athletes

**Rationale**:
- ✅ **Familiar**: Everyone remembers their email
- ✅ **Unique**: Email is already unique identifier
- ✅ **Communication**: Same email for login and invoices

---

## UI/UX Design

### Dark Theme with Glassmorphism

**Decision**: Dark navy background (#0f0f23) with glassmorphism cards

**Rationale**:
- ✅ **Modern**: Trendy, premium feel
- ✅ **Brand alignment**: Matches Tailwind landing page
- ✅ **Readability**: Good contrast for text
- ✅ **Energy saving**: Better for OLED screens

**Glassmorphism**:
```css
background: rgba(255, 255, 255, 0.05);
backdrop-filter: blur(10px);
```

### Blue-Cyan Gradient Branding

**Decision**: Use #4facfe → #00f2fe gradient for TAILWIND logo

**Rationale**:
- ✅ **Distinctive**: Unique brand identity
- ✅ **Energetic**: Conveys movement and speed
- ✅ **Consistency**: Matches landing page
- ✅ **Versatile**: Works on dark and light backgrounds

### Color-Coded Workout States

**Decision**: Use 7 distinct gradient colors for workout states

**Rationale**:
- ✅ **Instant recognition**: No need to read status text
- ✅ **Visual hierarchy**: Important states stand out (overdue = pulsing red)
- ✅ **Accessibility**: Color + text + icons for redundancy
- ✅ **Motivation**: Green gradients for success feel rewarding

### Mobile-First Responsive Design

**Decision**: Design for mobile first, then scale up to desktop

**Rationale**:
- ✅ **Usage patterns**: Athletes likely check on phones
- ✅ **Constraints**: Mobile forces simplicity
- ✅ **Progressive enhancement**: Easy to add desktop features
- ✅ **Performance**: Mobile-optimized is fast everywhere

**Breakpoints**: 768px (tablet), 1024px (desktop), 1280px (large desktop)

### Inter Font

**Decision**: Use Inter font family

**Rationale**:
- ✅ **Readability**: Designed for screens
- ✅ **Professional**: Clean, modern appearance
- ✅ **Free**: Open source, no licensing costs
- ✅ **Variable font**: Single file, multiple weights

---

## Deployment Strategy

### Railway.app (Recommended)

**Decision**: Deploy on Railway.app for initial launch

**Rationale**:
- ✅ **Free tier**: $5 credit/month (sufficient for MVP)
- ✅ **PostgreSQL included**: No separate database setup
- ✅ **Custom domain**: Can use app.tailwindrun.com
- ✅ **Auto-deploy**: GitHub integration
- ✅ **File storage**: Can store invoice PDFs
- ✅ **Easy scaling**: Upgrade as needed

**Alternatives**:
- Render.com: Free tier spins down (bad UX)
- PythonAnywhere: No custom domain on free tier
- Fly.io: More complex setup

### Custom Domain

**Decision**: Use subdomain `app.tailwindrun.com`

**Rationale**:
- ✅ **Professional**: Better than railway.app URL
- ✅ **Branding**: Consistent with main website
- ✅ **Trust**: Athletes feel secure with branded domain
- ✅ **SEO**: Better for search engines

### Environment Variables

**Decision**: Store sensitive config in environment variables

**Rationale**:
- ✅ **Security**: Secrets not in code repository
- ✅ **Flexibility**: Different configs for dev/staging/prod
- ✅ **Best practice**: Industry standard

**Key Variables**:
- `SECRET_KEY`, `DATABASE_URL`, `EMAIL_PASSWORD`, `DEBUG`

### Backup Strategy

**Decision**: Daily automated backups with 30-day retention

**Rationale**:
- ✅ **Data safety**: Protect against accidental deletion
- ✅ **Compliance**: Invoice data is legally important
- ✅ **Recovery**: Can restore to any point in last 30 days
- ✅ **Peace of mind**: Sleep better knowing data is safe

**Implementation**: Use Railway's backup feature + manual exports to S3/Google Drive

---

## Future Considerations

### Analytics Foundation

**Decision**: Design data models with analytics in mind

**Rationale**:
- ✅ **Long-term vision**: Want to build insights engine
- ✅ **Data quality**: Capture quality ratings, completion dates
- ✅ **Flexibility**: JSON fields for extensibility
- ✅ **Timestamps**: Track when things happen

**What We're Capturing**:
- Workout completion patterns
- Payment continuity
- Athlete engagement (login, submissions)
- Quality ratings over time

### Multi-Coach Platform

**Decision**: Design for single coach, but keep multi-coach in mind

**Rationale**:
- ✅ **Current need**: Single coach (Mehul)
- ✅ **Future potential**: Could expand to team/organization
- ✅ **Architecture**: Models support ForeignKey to Coach
- ✅ **Minimal overhead**: Doesn't complicate current implementation

**What to Add Later**:
- Coach model (currently just Django User)
- Coach-athlete relationships
- Coach-specific branding/templates

### API for Mobile App

**Decision**: Not building API now, but structure supports it

**Rationale**:
- ✅ **YAGNI**: Don't need it yet
- ✅ **Django REST Framework**: Easy to add later
- ✅ **Clean models**: Already separated from views
- ✅ **Authentication**: Django auth works with DRF

**When to Build**: If 50+ athletes request mobile app

---

## Key Principles

### 1. Simplicity Over Perfection

**Rationale**: Get MVP working quickly, iterate based on real usage

**Examples**:
- Django admin for coach (not custom interface)
- Manual invoice generation (not fully automated)
- URL field for Strava (not API integration)

### 2. Data Quality First

**Rationale**: Good data enables future analytics

**Examples**:
- Capture completion quality ratings
- Track original dates for rescheduled workouts
- Store athlete comments
- Timestamp everything

### 3. Athlete Experience Matters

**Rationale**: Athletes are paying customers, need good UX

**Examples**:
- Beautiful, modern UI
- Mobile-responsive design
- Clear payment status
- Easy workout submission

### 4. Legal Compliance

**Rationale**: Invoices are legal documents, must be accurate

**Examples**:
- Proper GST handling (only when GSTIN present)
- Indian invoice format (PAN, HSN/SAC)
- PDF generation and storage
- Audit trail for payments

### 5. Future-Proof Architecture

**Rationale**: Build foundation for analytics and insights

**Examples**:
- Rich data models
- Flexible JSON fields
- Timestamp tracking
- Separation of concerns

---

## Success Criteria

**MVP Success** (Phase 1):
- ✅ Coach can manage athletes and payments
- ✅ Automated invoice generation
- ✅ Athletes can view and complete workouts
- ✅ Payment tracking with history
- ✅ Deployed and accessible at app.tailwindrun.com

**Long-term Success** (Phase 2+):
- Analytics dashboard for coach
- Athlete behavior insights
- Churn prediction
- Automated review preparation
- 80%+ athlete retention

---

## Lessons Learned (To Be Updated)

_This section will be updated during and after development to capture lessons learned and decisions that would be made differently in hindsight._

---

## Document Maintenance

**Last Updated**: February 10, 2026

**Update Frequency**: After major decisions or architecture changes

**Owner**: Development team

**Review**: Before starting new features or making significant changes

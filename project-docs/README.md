# Athlete Management Application - Documentation

This directory contains all project documentation for the Tailwind Coaching athlete management application.

## Documents

### Planning & Implementation

- **[implementation_plan.md](implementation_plan.md)** - Complete technical implementation plan with data models, views, features, and deployment strategy
- **[design_decisions.md](design_decisions.md)** - Architectural choices, rationale, and key design decisions
- **[future_roadmap.md](future_roadmap.md)** - Long-term vision with analytics, insights engine, and phased implementation plan

### UI/UX

- **[complete_ui_mockups.md](complete_ui_mockups.md)** - All UI mockups (mobile + desktop) with color specifications and responsive design details
- **[invoice_email_templates.md](invoice_email_templates.md)** - Email templates for invoice delivery with HTML design and Django integration

### Images

- **[images/](images/)** - All UI mockup images (workout calendar, payment history, invoices, etc.)

## Quick Links

### For Developers
1. Start with [implementation_plan.md](implementation_plan.md) for technical specs
2. Review [design_decisions.md](design_decisions.md) to understand why choices were made
3. Check [complete_ui_mockups.md](complete_ui_mockups.md) for UI implementation

### For Product Planning
1. Review [future_roadmap.md](future_roadmap.md) for long-term vision
2. Check [complete_ui_mockups.md](complete_ui_mockups.md) for user experience

## Project Structure

```
tailwind-coaching/
├── docs/                    # Website code (landing page)
├── project-docs/            # This directory - App documentation
│   ├── implementation_plan.md
│   ├── design_decisions.md
│   ├── future_roadmap.md
│   ├── complete_ui_mockups.md
│   ├── invoice_email_templates.md
│   └── images/
│       ├── athlete_dashboard_mockup.png
│       ├── payment_history_mockup.png
│       ├── realistic_workout_calendar.png
│       ├── desktop_workout_calendar.png
│       └── ... (more mockups)
└── (Django app will go here)
```

## Key Features

- **Athlete Management** - Profile, subscription, payment tracking
- **Automated Invoicing** - Indian GST format with conditional GST calculation
- **Workout Tracking** - Calendar view with 7 color-coded states
- **Payment Plans** - 8 HSN/SAC codes (RUNFOCUS1MO, TRIPERSONAL1QTR, etc.)
- **Email Integration** - Automated invoice delivery
- **Responsive Design** - Mobile-first, works on all devices

## Technology Stack

- **Backend**: Django + PostgreSQL
- **Frontend**: Django Templates + Vanilla CSS
- **Deployment**: Railway.app (recommended)
- **Domain**: app.tailwindrun.com

## Getting Started

1. Read [implementation_plan.md](implementation_plan.md) for complete technical overview
2. Review mockups in [complete_ui_mockups.md](complete_ui_mockups.md)
3. Understand design choices in [design_decisions.md](design_decisions.md)
4. Follow implementation plan to build the application

## Contributing

When making changes:
1. Update relevant documentation files
2. Keep mockups in sync with implementation
3. Document design decisions in [design_decisions.md](design_decisions.md)
4. Update [future_roadmap.md](future_roadmap.md) as features are completed

## Questions?

Contact: mehul@mehulved.com

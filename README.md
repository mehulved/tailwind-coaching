# Tailwind - Running & Triathlon Coaching

A minimalist landing page for Tailwind coaching services, focusing on long-term athletic development for runners and triathletes.

## About

Tailwind provides personalized coaching for running and triathlon athletes, with a focus on sustainable practices and long-term goal achievement. With over 17 years of endurance sports experience, we specialize in working with beginners and developing athletes.

## Project Structure

```
tailwind-coaching/
├── docs/                # Website files (GitHub Pages)
│   ├── index.html
│   └── style.css
├── project-docs/        # Athlete management app documentation
│   ├── README.md
│   ├── implementation_plan.md
│   ├── complete_ui_mockups.md
│   ├── design_decisions.md
│   ├── future_roadmap.md
│   ├── invoice_email_templates.md
│   └── images/          # UI mockups and screenshots
└── README.md
```

The `docs` folder contains the static landing page website. The `project-docs` folder contains comprehensive documentation for the athlete management application (Django backend).

## Hosting on GitHub Pages

To host this site on GitHub Pages:

1. Create a new repository on GitHub (e.g., `tailwind-coaching`)
2. Push this code to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/tailwind-coaching.git
   git push -u origin main
   ```
3. Go to your repository settings on GitHub
4. Navigate to "Pages" in the left sidebar
5. Under "Source", select "main" branch and "**/docs** folder"
6. Click "Save"
7. Your site will be available at `https://YOUR_USERNAME.github.io/tailwind-coaching/`

## Local Development

To view the site locally, navigate to the docs folder and open `index.html` in your web browser, or use a local server:

```bash
# Using Python 3
cd docs
python3 -m http.server 8000

# Using Node.js (if you have npx)
cd docs
npx serve
```

Then navigate to `http://localhost:8000` in your browser.

## Athlete Management App Documentation

Comprehensive documentation for the athlete management application is available in the [`project-docs/`](project-docs/) directory:

- **[Implementation Plan](project-docs/implementation_plan.md)** - Complete technical specifications, data models, features, and deployment strategy
- **[UI Mockups](project-docs/complete_ui_mockups.md)** - All screens (mobile + desktop), invoice states, responsive design specs
- **[Design Decisions](project-docs/design_decisions.md)** - Architectural choices, technology stack rationale, and key design decisions
- **[Future Roadmap](project-docs/future_roadmap.md)** - Long-term vision with analytics, insights engine, and phased implementation
- **[Email Templates](project-docs/invoice_email_templates.md)** - Invoice email templates with HTML design

### Key Features (Planned)

- **Athlete Management** - Profile, subscription, payment tracking
- **Automated Invoicing** - Indian GST format with conditional GST calculation
- **Workout Tracking** - Calendar view with 7 color-coded states
- **Payment Plans** - 8 HSN/SAC codes (RUNFOCUS1MO, TRIPERSONAL1QTR, etc.)
- **Email Integration** - Automated invoice delivery
- **Responsive Design** - Mobile-first, works on all devices

**Tech Stack**: Django + PostgreSQL | **Deployment**: Railway.app | **Domain**: app.tailwindrun.com

## Contact

- Email: mehul@mehulved.com
- Phone: +91 96195 96659

## Future Enhancements

### Landing Page
- Add photos and testimonials
- Implement newsletter signup
- Add contact form

### Athlete Management App
See [Future Roadmap](project-docs/future_roadmap.md) for detailed plans including:
- Analytics dashboard
- Athlete behavior insights
- Churn prediction
- Automated review preparation


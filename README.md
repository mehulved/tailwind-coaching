# Tailwind - Running & Triathlon Coaching

A minimalist landing page for Tailwind coaching services, focusing on long-term athletic development for runners and triathletes.

## About

Tailwind provides personalized coaching for running and triathlon athletes, with a focus on sustainable practices and long-term goal achievement. With over 17 years of endurance sports experience, we specialize in working with beginners and developing athletes.

## Project Structure

```
tailwind-coaching/
├── docs/           # Website files (GitHub Pages)
│   ├── index.html
│   └── style.css
└── README.md
```

The `docs` folder contains the static website, keeping the repository organized for future backend development.

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

## Contact

- Email: mehul@mehulved.com
- Phone: +91 96195 96659

## Future Enhancements

- Add photos and testimonials
- Implement newsletter signup
- Add contact form

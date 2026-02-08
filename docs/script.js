// Accordion functionality for mobile plans
document.addEventListener('DOMContentLoaded', function() {
    const planHeaders = document.querySelectorAll('.plan-header');
    
    // Open first accordion by default on mobile
    if (window.innerWidth <= 768 && planHeaders.length > 0) {
        const firstHeader = planHeaders[0];
        const firstContent = document.querySelector(`[data-content="${firstHeader.dataset.plan}"]`);
        if (firstHeader && firstContent) {
            firstHeader.classList.add('active');
            firstContent.classList.add('active');
        }
    }
    
    // Add click handlers to all accordion headers
    planHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const planName = this.dataset.plan;
            const content = document.querySelector(`[data-content="${planName}"]`);
            
            // Toggle active state
            const isActive = this.classList.contains('active');
            
            if (isActive) {
                // Close this accordion
                this.classList.remove('active');
                content.classList.remove('active');
            } else {
                // Open this accordion
                this.classList.add('active');
                content.classList.add('active');
            }
        });
        
        // Add keyboard support
        header.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        // Make header focusable
        header.setAttribute('tabindex', '0');
        header.setAttribute('role', 'button');
        header.setAttribute('aria-expanded', 'false');
    });
    
    // Update aria-expanded when accordion state changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                const header = mutation.target;
                const isExpanded = header.classList.contains('active');
                header.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
            }
        });
    });
    
    planHeaders.forEach(header => {
        observer.observe(header, { attributes: true });
    });
});

// Payment toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-option');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const period = this.dataset.period;
            const pricingSection = this.closest('.plan-pricing');
            
            // Update toggle button states
            pricingSection.querySelectorAll('.toggle-option').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            // Update pricing tier display
            pricingSection.querySelectorAll('.pricing-tier').forEach(tier => {
                tier.classList.remove('active');
            });
            const activeTier = pricingSection.querySelector(`[data-tier="${period}"]`);
            if (activeTier) {
                activeTier.classList.add('active');
            }
        });
    });
});

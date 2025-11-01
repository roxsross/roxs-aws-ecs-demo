// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.animation = 'slideOut 0.3s ease';
            setTimeout(function() {
                flash.remove();
            }, 300);
        }, 5000);
    });
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation
const forms = document.querySelectorAll('.form');
forms.forEach(function(form) {
    form.addEventListener('submit', function(e) {
        const nameInput = form.querySelector('input[name="name"]');
        if (nameInput && nameInput.value.trim() === '') {
            e.preventDefault();
            alert('Por favor ingresa un nombre para el item');
            nameInput.focus();
        }
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading state to buttons on form submit
const forms2 = document.querySelectorAll('.form');
forms2.forEach(function(form) {
    form.addEventListener('submit', function(e) {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            submitButton.disabled = true;
        }
    });
});

// Add animation to cards on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeIn 0.5s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.item-card, .stat-card, .info-card').forEach(function(card) {
    observer.observe(card);
});

// Add fadeIn animation
const fadeInStyle = document.createElement('style');
fadeInStyle.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(fadeInStyle);

// Console easter egg
console.log('%c🚀 ECS Demo Application', 'font-size: 20px; font-weight: bold; color: #3b82f6;');
console.log('%cRunning on AWS ECS with DynamoDB', 'font-size: 14px; color: #64748b;');
console.log('%cBuilt with Flask + HTML + CSS + JavaScript', 'font-size: 12px; color: #10b981;');

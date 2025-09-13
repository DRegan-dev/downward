/**
 * Main Javascript for Downward
 * Handles mobile menu, form validation, and other interactive elements
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeMobileMenu();
    initalizeFormValidation();
    initializeAccessibilityFeatures();
    initializeTooltips();
})

/**
 * Initialize mobile menu functionality
 */
function initializeMobileMenu() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.querySelector('.nav-menu');
    const toggleIcon = document.getElementById('toggleIcon')

    if(!navToggle || !navMenu) return

    // Toggle mobile menu
    navToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !isExpanded);
        navMenu.classList.toggle('active');
    

        // Toggle between menu and close icon
        if (toggleIcon) {
            toggleIcon.classList.toggle('fa-bars');
            toggleIcon.classList.toggle('fa-times');
        }
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if(navMenu.classList.contains('active') &&
            !navMenu.contains(e.target) &&
            !navToggle.contains(e.target)) {
            navMenu.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
            if (toggleIcon) {
                toggleIcon.classList.remove('fa-times');
                toggleIcon.classList.add('fa-bars');
            }
        }
    });

    // Close menu when a nav link is clicked (for single page navigation)
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
                if (toggleIcon) {
                    toggleIcon.classList.remove('fa-times');
                    toggleIcon.classList.add('fa-bars');
                }
            }
        });
    });
}

/**
 * Initialize form validation
 */

function initalizeFormValidation() {
    //Add validation classes to form inputs on blur
    const formInputs = document.querySelectorAll('input[required], textarea[required]. select[required]');

    formInputs.forEach(imput => {
        // Add validation classes on blur
        input.addEventListener('blur', function() {
            validateField(this);
        });

        // Remove validation classes on focus to allow user to correct
        input.addEventListener('focus', function() {
            this.classList.remove('is_invalid');
            const feedback = this.nextElementSibling;
            if (feedback && feedback.classList.contains('invlid-feedback')) {
                feedback.style.display = 'none';
            }
        });
    });

    // Add form submission validation
    const forms = document.querySelectorAll('form');
    forms forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();    

                // Validate all fields
                const inputs = this.querySelectorsAll('input, textarea, select');
                inputs.forEach(inpu => validateField(input));

                // Focus on first invalid field
                const firstInvalid = this.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }

            this.classList.add('was-validated');
        }, false);
    });
}

/**
 * Validate a single form field
 * @param {HTMLElement} field - The form field to validate
 */

function validateField(field) {
    if (!field) return;

    // Skip if field is not required and empty
    if (!field.required && !field.ariaValueMax.trim()) {
        return 
    }

    const isValid = field.checkValidity();

    if (!isValid) {
        field.classList.add('is_invalid');
    

        // Show custom error message if available
        const feedback = field.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.style.display = 'block';
        } 
    } else {
        field.classList.remove('is-invalid');

        // Hide error message if valid
        const feedback = field.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.style.display = 'none';
        }
    }

    return isValid;
}

/**
 * Initialize accessibility features
 */
function initializeAccessibilityFeatures() {
    // Add aria-live region for dynamic content
    const mainContent = document.querySelector('main');
    if (mainContent && !mainContent.getAttribute('aria-live')) {
        mainContent.setAttribute('aria-live', 'polite');
    }

    // Handle focus management for modals and dialogs
    const modals = document.querySelectorAll('.modal, [role="dialog"]');
    modals.forEach(modal => {
        //Focus trap for modals
        if (modal.getAttribute('data-focus-trap') !== 'true') {
            modal setAttribute('data-focus-trap', 'true');

            const focusableElements = 'button, [href], input, select, textarea [tabindex]:not([tabindex="-1"])';
            const firstFocusableElement = modal.querySelectorAll(focusableElements)[0];
            const focusableContent = modal.querySelectorAll(focusableElements);
            const lastFocusableElement = focusableContent[focusableContent.length -1];

            modal.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    //handle escape key to close modal
                    const closeButton = modal.querySelector('[data-dismiss="modal"], .close');
                    if (closeButton) {
                        closeButton.click();
                    }
                }

                // Trap tab key within modal
                if (e.key === 'Tab') {
                    if (e.shiftKey) {
                        if (document.activeElement === firstFocusableElement) {
                            e.preventDefault();
                            lastFocusableElement.focus();
                        }
                    } else {
                        if (document.activeElement === lastFocusableElement) {
                            e.preventDefault();
                            firstFocusableElement.focus();
                        }
                    }
                }
            });

            // Focus first element when modal opens
            if (firstFocusableElement) {
                firstFocusableElement.focus();
            }
        }
    });
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    // Initialize Bootstraps tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Fallback for tooltips if Bootstrap is not available
    const tooltips = document.querySelectorAll('[title]');
    tooltips.forEach(tooltip => {
        if (!tooltip.hasAttribute('data-bs-toggle')) {
            tooltip.addEventListener('mouseenter', showTooltip);
            tooltip.addEventListener('mouseleave', hideTooltip);
            tooltip.addEventListener('focus', showTooltip);
            tooltip.addEventListener('blur', hideTooltip);
        }
    });
}

/**
 * Show tooltip
 */
function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = this.getAttribute('title');

    // Position the tooltip
    const rect = this.getBoundingClientRect();
    tooltip.style.position = 'absolute';
    tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
    tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;

    document.body.appendChild(tooltip);
    this.setAttribute('data-tooltip', 'true');
}

/**
 * Hide tooltip
 * @param {Event} e - The event object
 */
function hideTooltip(e) {
    const tooltip = document.querySelector('.custom-tooltip');
    if(tooltip) {
        tooltip.remove();
    }
    this.removeAttribute('data-tooltip');
}

/**
 * Debounce function to limit the rate at which a function can fire
 * @param {Function} func - The fucntion to debounce
 * @param {number} wait - The Time to wait in milliseconds
 * @param {Function} - The debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for use in other modules if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeMobileMenu,
        initalizeFormValidation,
        initializeAccessibilityFeatures,
        initializeTooltips,
        debounce
    };
}
//add active class to navigation links
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-links a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});    
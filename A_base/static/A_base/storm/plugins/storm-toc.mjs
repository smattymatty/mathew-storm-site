// Storm Table of Contents Plugin
// Epic storm-themed navigation with lightning effects

export const StormTOCPlugin = {
    name: 'StormTOC',
    version: '1.0.0',
    
    config: {
        animations: {
            expandDuration: 300,
            glowPulseDuration: 2000,
            lightningDuration: 400
        },
        colors: {
            background: '#0a0a0a',
            backgroundGradientEnd: '#1a2332',
            electric: '#00ffff',
            electricDim: 'rgba(0, 255, 255, 0.3)',
            white: '#ffffff',
            activeGlow: '#00ff00'
        }
    },

    init(StormEvents) {
        this.setupStyles();
        this.enhanceTOC();
        this.setupEventListeners(StormEvents);
    },

    setupStyles() {
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            /* Storm TOC Container */
            .toc-wrapper {
                background: linear-gradient(180deg, 
                    ${this.config.colors.background} 0%, 
                    ${this.config.colors.backgroundGradientEnd} 100%) !important;
                border: 1px solid ${this.config.colors.electricDim} !important;
                box-shadow: 
                    0 0 20px rgba(0, 255, 255, 0.2),
                    inset 0 0 10px rgba(0, 255, 255, 0.05) !important;
                border-radius: 12px !important;
                padding: 1.5rem !important;
                position: relative;
                overflow: hidden;
            }

            /* Lightning border effect */
            .toc-wrapper::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, 
                    transparent, 
                    ${this.config.colors.electric}, 
                    transparent);
                animation: lightningBorder 3s linear infinite;
            }

            .toc-wrapper::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, 
                    transparent, 
                    ${this.config.colors.electric}, 
                    transparent);
                animation: lightningBorder 3s linear infinite reverse;
            }

            @keyframes lightningBorder {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }

            /* TOC List Styles */
            .toc-list {
                list-style: none !important;
                padding: 0 !important;
                margin: 0 !important;
            }

            .toc-sublist {
                list-style: none !important;
                padding-left: 1.5rem !important;
                margin: 0 !important;
                transition: max-height 0.3s ease-out, opacity 0.3s ease-out !important;
                overflow: hidden !important;
            }

            .toc-sublist.collapsed {
                opacity: 0 !important;
            }

            /* TOC Item */
            .toc-item {
                margin: 0.5rem 0 !important;
                position: relative;
            }

            .toc-item-header {
                display: flex;
                align-items: center;
                position: relative;
                padding: 0.5rem 0;
            }

            /* Lightning bolt toggle arrow */
            .toc-toggle {
                background: transparent !important;
                border: none !important;
                color: ${this.config.colors.electric} !important;
                cursor: pointer;
                padding: 0 0.5rem 0 0 !important;
                display: inline-flex;
                align-items: center;
                transition: all 0.3s !important;
            }

            .toc-toggle svg {
                fill: currentColor !important;
                transition: transform 0.3s !important;
            }

            .toc-toggle:not(.collapsed) svg {
                transform: rotate(90deg);
            }

            .toc-toggle:hover {
                filter: drop-shadow(0 0 5px ${this.config.colors.electric});
            }

            /* Replace arrow with lightning bolt */
            .toc-arrow {
                display: none !important;
            }

            .toc-toggle::before {
                content: '⚡';
                font-size: 14px;
                display: inline-block;
                transition: transform 0.3s;
            }

            .toc-toggle:not(.collapsed)::before {
                transform: rotate(90deg);
            }

            /* TOC Links */
            .toc-link {
                color: ${this.config.colors.white} !important;
                text-decoration: none !important;
                padding: 0.5rem 0.75rem !important;
                display: inline-block !important;
                position: relative;
                transition: all 0.3s !important;
                text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
                border-radius: 6px;
            }

            .toc-link:hover {
                color: ${this.config.colors.electric} !important;
                text-shadow: 
                    0 0 10px rgba(0, 255, 255, 1),
                    0 0 20px rgba(0, 255, 255, 0.5) !important;
                transform: translateX(5px);
                background: rgba(0, 255, 255, 0.05);
            }

            /* Active page indicator */
            .toc-link.active {
                color: ${this.config.colors.electric} !important;
                background: rgba(0, 255, 255, 0.1) !important;
                box-shadow: 
                    0 0 10px rgba(0, 255, 255, 0.3),
                    inset 0 0 5px rgba(0, 255, 255, 0.1) !important;
                animation: activePulse 2s ease-in-out infinite;
            }

            @keyframes activePulse {
                0%, 100% { 
                    box-shadow: 
                        0 0 10px rgba(0, 255, 255, 0.3),
                        inset 0 0 5px rgba(0, 255, 255, 0.1);
                }
                50% { 
                    box-shadow: 
                        0 0 20px rgba(0, 255, 255, 0.5),
                        inset 0 0 10px rgba(0, 255, 255, 0.2);
                }
            }

            /* Lightning strike on click */
            .toc-link.lightning-strike::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 0;
                width: 100%;
                height: 2px;
                background: linear-gradient(90deg, 
                    transparent, 
                    ${this.config.colors.electric}, 
                    transparent);
                animation: strikeThrough 0.3s ease-out forwards;
                pointer-events: none;
            }

            @keyframes strikeThrough {
                0% {
                    transform: translateX(-100%) translateY(-50%);
                    opacity: 0;
                }
                50% {
                    opacity: 1;
                }
                100% {
                    transform: translateX(100%) translateY(-50%);
                    opacity: 0;
                }
            }

            /* Electric connector lines */
            .toc-item.has-children > .toc-item-header::before {
                content: '';
                position: absolute;
                left: 8px;
                top: 100%;
                width: 1px;
                height: calc(100% + 0.5rem);
                background: linear-gradient(180deg, 
                    ${this.config.colors.electricDim}, 
                    transparent);
                opacity: 0.5;
            }

            /* Hover particle effect */
            .storm-toc-particle {
                position: absolute;
                width: 3px;
                height: 3px;
                background: ${this.config.colors.electric};
                border-radius: 50%;
                pointer-events: none;
                animation: tocParticle 1s ease-out forwards;
            }

            @keyframes tocParticle {
                0% {
                    transform: translate(0, 0) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translate(20px, -20px) scale(0);
                    opacity: 0;
                }
            }

            /* Mobile optimizations */
            @media (max-width: 768px) {
                .toc-wrapper {
                    padding: 1rem !important;
                    margin: 0.5rem !important;
                }
                
                .toc-link {
                    font-size: 0.9rem;
                    padding: 0.4rem 0.6rem !important;
                }
            }

            /* Reduced motion support */
            @media (prefers-reduced-motion: reduce) {
                .toc-wrapper::before,
                .toc-wrapper::after,
                .toc-link,
                .toc-toggle,
                .storm-toc-particle {
                    animation: none !important;
                    transition: none !important;
                }
            }
        `;
        document.head.appendChild(styleSheet);
    },

    enhanceTOC() {
        document.addEventListener('DOMContentLoaded', () => {
            // Mark current page as active
            const currentPath = window.location.pathname;
            const tocLinks = document.querySelectorAll('.toc-link');
            
            tocLinks.forEach(link => {
                if (link.href && link.href.includes(currentPath)) {
                    link.classList.add('active');
                }
                
                // Add click effect
                link.addEventListener('click', (e) => {
                    this.createLightningStrike(link);
                });
                
                // Add hover particles
                link.addEventListener('mouseenter', (e) => {
                    this.createTOCParticle(e);
                });
            });

            // Enhance toggle buttons
            const toggleButtons = document.querySelectorAll('.toc-toggle');
            toggleButtons.forEach(button => {
                button.addEventListener('click', () => {
                    this.animateToggle(button);
                });
            });

            // Mark items with children
            const itemsWithChildren = document.querySelectorAll('.toc-item:has(.toc-sublist)');
            itemsWithChildren.forEach(item => {
                item.classList.add('has-children');
            });
        });
    },

    createLightningStrike(element) {
        element.classList.add('lightning-strike');
        setTimeout(() => {
            element.classList.remove('lightning-strike');
        }, 300);
    },

    createTOCParticle(event) {
        const particle = document.createElement('div');
        particle.className = 'storm-toc-particle';
        
        const rect = event.target.getBoundingClientRect();
        particle.style.left = `${event.clientX - rect.left}px`;
        particle.style.top = `${event.clientY - rect.top}px`;
        
        event.target.appendChild(particle);
        
        setTimeout(() => particle.remove(), 1000);
    },

    animateToggle(button) {
        const sublist = button.closest('.toc-item').querySelector('.toc-sublist');
        if (sublist) {
            // Create a mini lightning flash
            const flash = document.createElement('div');
            flash.style.position = 'absolute';
            flash.style.width = '100%';
            flash.style.height = '100%';
            flash.style.background = `radial-gradient(circle at center, ${this.config.colors.electricDim}, transparent)`;
            flash.style.opacity = '0';
            flash.style.pointerEvents = 'none';
            flash.style.animation = 'flashIn 0.2s ease-out';
            
            button.appendChild(flash);
            setTimeout(() => flash.remove(), 200);
        }
    },

    setupEventListeners(StormEvents) {
        // Listen for TOC navigation events
        StormEvents.on('toc:navigate', (data) => {
            const link = document.querySelector(`[href="${data.url}"]`);
            if (link) {
                this.createLightningStrike(link);
            }
        });

        // Add storm effect on scroll to current section
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.highlightCurrentSection();
            }, 100);
        });
    },

    highlightCurrentSection() {
        const sections = document.querySelectorAll('h1[id], h2[id], h3[id]');
        const tocLinks = document.querySelectorAll('.toc-link');
        
        let currentSection = null;
        sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 100 && rect.bottom >= 0) {
                currentSection = section.id;
            }
        });

        if (currentSection) {
            tocLinks.forEach(link => {
                if (link.href && link.href.includes(`#${currentSection}`)) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        }
    }
};

// Auto-initialize when Storm Events is available
if (typeof window !== 'undefined') {
    window.StormTOCPlugin = StormTOCPlugin;
}

// Export for module systems
export default StormTOCPlugin;
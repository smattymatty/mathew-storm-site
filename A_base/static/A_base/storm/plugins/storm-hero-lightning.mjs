// Storm Hero Lightning Plugin
// Epic hero animations for "Leading the Storm" with lightning effects

export const StormHeroLightningPlugin = {
    name: 'StormHeroLightning',
    version: '1.0.0',
    
    config: {
        animations: {
            lightningDuration: 600,
            glowPulseDuration: 2000,
            typingSpeed: 100,
            particleLifetime: 3000
        },
        colors: {
            lightning: '#73bed3',      // Light blue from palette
            electricBlue: '#4f8fba',   // Main blue
            stormPurple: '#7a367b',    // Purple from palette
            glowWhite: '#d7b594'       // Warm text color
        }
    },

    init(StormEvents) {
        this.setupStyles();
        this.initializeHeroAnimations();
        this.setupEventListeners(StormEvents);
    },

    setupStyles() {
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            /* Storm Hero Gradient Background */
            .storm-hero-gradient {
                background: linear-gradient(180deg,
                    #000000 0%,      /* Pure black at top */
                    #050505 10%,     /* Nearly opaque for first 10% */
                    #0a0a0a 20%,     /* Very dark gray */
                    #0f1420 40%,     /* Dark blue-gray */
                    #1a2332 70%,     /* Slightly lighter blue-gray */
                    #1f2937 100%     /* Dark gray-blue at bottom */
                );
                position: relative;
                overflow: hidden;
                /* Optional subtle animation - much slower */
                animation: stormGradientSubtle 30s ease infinite;
            }

            @keyframes stormGradientSubtle {
                0%, 100% { 
                    background: linear-gradient(180deg,
                        #000000 0%,
                        #050505 10%,
                        #0a0a0a 20%,
                        #0f1420 40%,
                        #1a2332 70%,
                        #1f2937 100%
                    );
                }
                50% { 
                    background: linear-gradient(180deg,
                        #000000 0%,
                        #030303 10%,
                        #080808 20%,
                        #0d1118 40%,
                        #171f2a 70%,
                        #1a2332 100%
                    );
                }
            }

            /* Lightning Text Effect - Simplified, more readable */
            .storm-text-lightning {
                position: relative;
                display: inline-block;
                color: #ffffff !important;
                font-weight: 700;
                text-shadow: 
                    0 2px 4px rgba(0, 0, 0, 0.3),
                    0 0 10px rgba(115, 190, 211, 0.2);
            }
            
            /* Yellow lightning bolt emoji */
            .lightning-emoji {
                color: #ffff00;
                filter: drop-shadow(0 0 10px rgba(255, 255, 0, 0.8));
            }

            /* Lightning Strike Animation */
            @keyframes lightningStrike {
                0% { 
                    opacity: 0;
                    transform: translateY(-50px) scaleY(0);
                    filter: blur(5px);
                }
                20% {
                    opacity: 1;
                    transform: translateY(0) scaleY(1.2);
                    filter: blur(0) brightness(2);
                }
                40% {
                    transform: scaleY(1);
                    filter: brightness(1.5);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0) scaleY(1);
                    filter: brightness(1);
                }
            }

            .storm-strike-in {
                animation: lightningStrike 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
            }

            /* Glowing Name Effect - Simplified */
            .storm-text-glow {
                color: #c7cfcc;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
            }

            /* Electric Badge */
            .storm-badge-electric {
                position: relative;
                background: linear-gradient(45deg, #1f2f3aa8, #1c4141ff);
                color: #000000 !important;
                font-weight: bold;
                overflow: hidden;
                animation: electricPulse 2s linear infinite;
            }

            @keyframes electricPulse {
                0%, 100% { 
                    box-shadow: 
                        0 0 5px rgba(115, 190, 211, 0.5),
                        0 0 10px rgba(79, 143, 186, 0.3);
                }
                50% { 
                    box-shadow: 
                        0 0 10px rgba(115, 190, 211, 0.8),
                        0 0 20px rgba(79, 143, 186, 0.5);
                }
            }



            /* Storm Particles Background */
            .storm-particles {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                overflow: hidden;
            }

            .storm-particle {
                position: absolute;
                background: radial-gradient(circle, rgba(115, 190, 211, 0.8) 0%, transparent 70%);
                border-radius: 50%;
                pointer-events: none;
                animation: floatParticle 10s linear infinite;
            }

            @keyframes floatParticle {
                0% {
                    transform: translateY(-10vh) translateX(0) scale(0);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                    transform: translateY(0vh) translateX(-5px) scale(1);
                }
                90% {
                    opacity: 1;
                    transform: translateY(90vh) translateX(10px) scale(1);
                }
                100% {
                    transform: translateY(110vh) translateX(15px) scale(0);
                    opacity: 0;
                }
            }

            /* Lightning Bolt SVG Animation */
            .lightning-bolt {
                position: absolute;
                width: 100px;
                height: 200px;
                opacity: 0;
                filter: blur(1px) brightness(2);
                animation: boltStrike 0.3s ease-out forwards;
                pointer-events: none;
                z-index: 100;
            }

            @keyframes boltStrike {
                0% {
                    opacity: 0;
                    transform: scaleY(0) translateY(-50px);
                }
                50% {
                    opacity: 1;
                    transform: scaleY(1.2) translateY(0);
                }
                100% {
                    opacity: 0;
                    transform: scaleY(1) translateY(50px);
                }
            }

            /* Mobile Optimizations */
            @media (max-width: 768px) {
                .storm-text-lightning {
                    font-size: 2.5rem !important;
                }
                .storm-text-glow {
                    font-size: 1.5rem !important;
                }
            }

            /* Reduced Motion Support */
            @media (prefers-reduced-motion: reduce) {
                .storm-hero-gradient,
                .storm-text-lightning,
                .storm-text-glow,
                .storm-badge-electric,
                .storm-typing,
                .storm-particle {
                    animation: none !important;
                }
            }
        `;
        document.head.appendChild(styleSheet);
    },

    initializeHeroAnimations() {
        // Auto-initialize hero elements on page load
        document.addEventListener('DOMContentLoaded', () => {
            // Just show title and tagline normally - no complex animations
            const heroTitle = document.querySelector('[data-storm-hero="title"]');
            const heroTagline = document.querySelector('[data-storm-hero="tagline"]');
            
            // Simple fade-in for title and tagline
            if (heroTitle) {
                heroTitle.style.opacity = '1';
            }
            
            if (heroTagline) {
                heroTagline.style.opacity = '1';
            }

            // Create floating particles
            this.createFloatingParticles();
        });
    },

    createLightningEffect(element) {
        const bolt = document.createElement('div');
        bolt.className = 'lightning-bolt';
        
        // Check if there's a storm cloud border to emerge from
        const stormCloud = document.querySelector('[data-storm-cloud="border"]');
        let startY = -100; // Default position
        
        if (stormCloud) {
            const cloudRect = stormCloud.getBoundingClientRect();
            const scrollY = window.scrollY || window.pageYOffset;
            // Position bolt to emerge from center-bottom of storm cloud
            startY = cloudRect.top + scrollY + cloudRect.height - 20;
        }
        
        bolt.innerHTML = `
            <svg viewBox="0 0 100 300" style="width: 100%; height: 100%;">
                <path d="M 50 0 L 35 100 L 65 95 L 45 300" 
                      stroke="rgba(115, 190, 211, 0.9)" 
                      stroke-width="4" 
                      fill="none"
                      filter="url(#glow)"/>
                <defs>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="5" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
            </svg>
        `;
        
        const rect = element.getBoundingClientRect();
        const scrollY = window.scrollY || window.pageYOffset;
        bolt.style.position = 'absolute';
        bolt.style.width = '150px';
        bolt.style.height = '300px';
        bolt.style.left = `${rect.left + rect.width / 2 - 75}px`;
        
        if (stormCloud) {
            // Bolt emerges from cloud and strikes the title
            bolt.style.top = `${startY}px`;
        } else {
            bolt.style.top = `${rect.top + scrollY - 150}px`;
        }
        
        // Also trigger thunder in the cloud if it exists
        if (stormCloud && window.StormEvents) {
            window.StormEvents.trigger('cloud:thunder', {});
        }
        
        document.body.appendChild(bolt);
        setTimeout(() => bolt.remove(), 600);
    },

    typeText(element) {
        const text = element.textContent;
        element.textContent = '';
        element.style.opacity = '1';
        element.classList.add('storm-typing');
        
        let index = 0;
        const typeInterval = setInterval(() => {
            if (index < text.length) {
                element.textContent += text[index];
                index++;
            } else {
                clearInterval(typeInterval);
                setTimeout(() => {
                    element.classList.remove('storm-typing');
                    element.style.borderRight = 'none';
                }, 1000);
            }
        }, this.config.animations.typingSpeed);
    },

    createFloatingParticles() {
        const container = document.querySelector('.storm-hero-gradient');
        if (!container) return;

        const particlesDiv = document.createElement('div');
        particlesDiv.className = 'storm-particles';
        container.appendChild(particlesDiv);

        // Create initial particles immediately with staggered positions
        for (let i = 0; i < 15; i++) {
            this.createParticle(particlesDiv, i * 7); // Pass initial vertical offset
        }

        // Continue creating particles more frequently
        setInterval(() => {
            this.createParticle(particlesDiv, 0);
        }, 1000);
    },

    createParticle(container, initialOffset = 0) {
        const particle = document.createElement('div');
        particle.className = 'storm-particle';
        
        const size = Math.random() * 4 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${Math.random() * 100}%`;
        
        // Faster animation, no delay for immediate movement
        const duration = Math.random() * 5 + 8; // 8-13 seconds instead of 10-20
        particle.style.animationDuration = `${duration}s`;
        
        // If initial offset provided, set starting position
        if (initialOffset > 0) {
            particle.style.top = `${initialOffset}%`;
            particle.style.animationDelay = '0s'; // No delay, start immediately
        } else {
            particle.style.animationDelay = '0s'; // No delay for new particles either
        }
        
        container.appendChild(particle);
        
        // Remove after animation completes
        setTimeout(() => particle.remove(), duration * 1000 + 1000);
    },

    setupEventListeners(StormEvents) {
        // Listen for custom storm events
        StormEvents.on('hero:lightning', (data) => {
            const element = data.element || document.querySelector('[data-storm-hero="title"]');
            if (element) {
                this.createLightningEffect(element);
            }
        });

        // Add hover effects for hero elements
        document.addEventListener('mouseover', (e) => {
            if (e.target.hasAttribute('data-storm-hero')) {
                const type = e.target.getAttribute('data-storm-hero');
                if (type === 'badge') {
                    this.createMiniLightning(e.target);
                }
            }
        });
    },

    createMiniLightning(element) {
        const spark = document.createElement('div');
        spark.style.position = 'absolute';
        spark.style.width = '2px';
        spark.style.height = '20px';
        spark.style.background = 'linear-gradient(to bottom, transparent, rgba(115, 190, 211, 0.8), transparent)';
        spark.style.left = `${Math.random() * element.offsetWidth}px`;
        spark.style.top = '0';
        spark.style.animation = 'sparkFall 0.3s ease-out forwards';
        spark.style.pointerEvents = 'none';
        
        element.style.position = 'relative';
        element.appendChild(spark);
        
        setTimeout(() => spark.remove(), 300);
    }
};

// Auto-initialize when Storm Events is available
if (typeof window !== 'undefined') {
    window.StormHeroLightningPlugin = StormHeroLightningPlugin;
}

// Export for module systems
export default StormHeroLightningPlugin;
// Storm Cloud Border Plugin
// Creates an animated storm cloud border effect with lightning flashes

export const StormCloudBorderPlugin = {
    name: 'StormCloudBorder',
    version: '1.0.0',
    
    config: {
        animations: {
            cloudSpeed: 40000, // Base cloud movement duration
            flashFrequency: 8000, // How often lightning flashes occur
            turbulenceSpeed: 3000, // Turbulence animation speed
        },
        colors: {
            cloudDark: '#0a0a0a',
            cloudMid: '#1a1a1a',
            cloudLight: '#2a2a2a',
            lightning: '#ffffff',
            electricBlue: '#00ffff',
            cloudGray: '#333333'
        }
    },

    init(StormEvents) {
        this.setupStyles();
        this.initializeCloudBorders();
        this.setupEventListeners(StormEvents);
    },

    setupStyles() {
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            /* Storm Cloud Border Container */
            .storm-cloud-border {
                position: relative;
                width: 100%;
                height: 3.4rem;
                overflow: visible;
                background: transparent;
                margin-bottom: -80px;
                z-index: 10;
                pointer-events: none;
            }

            /* SVG Filter for Cloud Turbulence */
            .storm-cloud-svg-filters {
                position: absolute;
                width: 0;
                height: 0;
            }

            /* Cloud Layers */
            .storm-cloud-layer {
                position: absolute;
                width: 200%;
                height: 150px;
                background-repeat: repeat-x;
                bottom: 0;
                pointer-events: none;
            }

            .storm-cloud-layer-1 {
                background: url("data:image/svg+xml,%3Csvg width='800' height='150' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3CradialGradient id='cloud1'%3E%3Cstop offset='0%25' stop-color='%231a1a1a' stop-opacity='0.8'/%3E%3Cstop offset='70%25' stop-color='%230a0a0a' stop-opacity='0.4'/%3E%3Cstop offset='100%25' stop-color='%230a0a0a' stop-opacity='0'/%3E%3C/radialGradient%3E%3C/defs%3E%3Cellipse cx='100' cy='120' rx='150' ry='50' fill='url(%23cloud1)'/%3E%3Cellipse cx='400' cy='125' rx='180' ry='45' fill='url(%23cloud1)'/%3E%3Cellipse cx='700' cy='115' rx='140' ry='55' fill='url(%23cloud1)'/%3E%3Cellipse cx='0' cy='125' rx='100' ry='45' fill='url(%23cloud1)'/%3E%3Cellipse cx='800' cy='120' rx='100' ry='50' fill='url(%23cloud1)'/%3E%3C/svg%3E") repeat-x;
                background-size: 800px 150px;
                animation: cloudDrift1 ${this.config.animations.cloudSpeed}ms linear infinite;
                opacity: 0.6;
                filter: blur(3px);
            }

            .storm-cloud-layer-2 {
                background: url("data:image/svg+xml,%3Csvg width='1000' height='150' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3CradialGradient id='cloud2'%3E%3Cstop offset='0%25' stop-color='%232a2a2a' stop-opacity='0.7'/%3E%3Cstop offset='80%25' stop-color='%231a1a1a' stop-opacity='0.3'/%3E%3Cstop offset='100%25' stop-color='%231a1a1a' stop-opacity='0'/%3E%3C/radialGradient%3E%3C/defs%3E%3Cellipse cx='200' cy='130' rx='200' ry='45' fill='url(%23cloud2)'/%3E%3Cellipse cx='600' cy='120' rx='170' ry='50' fill='url(%23cloud2)'/%3E%3Cellipse cx='900' cy='125' rx='150' ry='40' fill='url(%23cloud2)'/%3E%3Cellipse cx='0' cy='120' rx='120' ry='45' fill='url(%23cloud2)'/%3E%3Cellipse cx='1000' cy='130' rx='120' ry='45' fill='url(%23cloud2)'/%3E%3C/svg%3E") repeat-x;
                background-size: 1000px 150px;
                animation: cloudDrift2 ${this.config.animations.cloudSpeed * 1.5}ms linear infinite reverse;
                opacity: 0.4;
                filter: blur(2px);
            }

            .storm-cloud-layer-3 {
                background: url("data:image/svg+xml,%3Csvg width='1200' height='150' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3CradialGradient id='cloud3' cx='50%25' cy='100%25' r='60%25'%3E%3Cstop offset='0%25' stop-color='%23333333' stop-opacity='0.5'/%3E%3Cstop offset='85%25' stop-color='%230a0a0a' stop-opacity='0.2'/%3E%3Cstop offset='100%25' stop-color='%230a0a0a' stop-opacity='0'/%3E%3C/radialGradient%3E%3C/defs%3E%3Cellipse cx='300' cy='140' rx='250' ry='30' fill='url(%23cloud3)'/%3E%3Cellipse cx='800' cy='135' rx='200' ry='35' fill='url(%23cloud3)'/%3E%3Cellipse cx='0' cy='137' rx='150' ry='32' fill='url(%23cloud3)'/%3E%3Cellipse cx='1200' cy='138' rx='150' ry='30' fill='url(%23cloud3)'/%3E%3C/svg%3E") repeat-x;
                background-size: 1200px 150px;
                animation: cloudDrift3 ${this.config.animations.cloudSpeed * 0.7}ms linear infinite;
                opacity: 0.3;
                filter: blur(4px);
            }

            /* Cloud Movement Animations */
            @keyframes cloudDrift1 {
                from { transform: translateX(0); }
                to { transform: translateX(-800px); }
            }

            @keyframes cloudDrift2 {
                from { transform: translateX(0); }
                to { transform: translateX(-1000px); }
            }

            @keyframes cloudDrift3 {
                from { transform: translateX(0); }
                to { transform: translateX(-1200px); }
            }

            /* Lightning Flash Effect */
            .storm-cloud-flash {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: radial-gradient(ellipse at center top, 
                    rgba(255, 255, 255, 0.8) 0%, 
                    rgba(0, 255, 255, 0.4) 30%, 
                    transparent 70%);
                opacity: 0;
                pointer-events: none;
                mix-blend-mode: screen;
            }

            .storm-cloud-flash.active {
                animation: lightningFlash 0.3s ease-out;
            }

            @keyframes lightningFlash {
                0% { opacity: 0; }
                20% { opacity: 1; }
                40% { opacity: 0.3; }
                60% { opacity: 0.9; }
                100% { opacity: 0; }
            }

            /* Cloud Wisps */
            .storm-cloud-wisp {
                position: absolute;
                width: 100px;
                height: 30px;
                background: radial-gradient(ellipse, 
                    rgba(45, 53, 97, 0.4) 0%, 
                    transparent 70%);
                border-radius: 50%;
                opacity: 0;
                animation: wispFloat 15s linear infinite;
            }

            @keyframes wispFloat {
                0% {
                    transform: translateX(-100px) translateY(0) scale(0.8);
                    opacity: 0;
                }
                10% {
                    opacity: 0.6;
                }
                90% {
                    opacity: 0.6;
                }
                100% {
                    transform: translateX(calc(100vw + 100px)) translateY(-10px) scale(1.2);
                    opacity: 0;
                }
            }

            /* Turbulence Animation */
            @keyframes turbulenceAnimation {
                0%, 100% { 
                    filter: url(#turbulence);
                }
                25% { 
                    filter: url(#turbulence2);
                }
                50% { 
                    filter: url(#turbulence3);
                }
                75% { 
                    filter: url(#turbulence4);
                }
            }

            /* Mobile Optimizations */
            @media (max-width: 768px) {
                .storm-cloud-border {
                    height: 3.2rem
                    margin-bottom: -60px;
                }
                .storm-cloud-layer {
                    animation-duration: ${this.config.animations.cloudSpeed * 2}ms;
                }
            }

            /* Reduced Motion Support */
            @media (prefers-reduced-motion: reduce) {
                .storm-cloud-layer,
                .storm-cloud-wisp,
                .storm-cloud-flash {
                    animation: none !important;
                }
            }
        `;
        document.head.appendChild(styleSheet);

        // Add SVG filters for turbulence effect
        this.addSVGFilters();
    },

    addSVGFilters() {
        const svgNS = "http://www.w3.org/2000/svg";
        const svg = document.createElementNS(svgNS, "svg");
        svg.setAttribute("class", "storm-cloud-svg-filters");
        svg.innerHTML = `
            <defs>
                <filter id="turbulence">
                    <feTurbulence type="fractalNoise" baseFrequency="0.01 0.02" numOctaves="3" seed="1" />
                    <feDisplacementMap in="SourceGraphic" scale="3" />
                </filter>
                <filter id="turbulence2">
                    <feTurbulence type="fractalNoise" baseFrequency="0.012 0.018" numOctaves="3" seed="2" />
                    <feDisplacementMap in="SourceGraphic" scale="4" />
                </filter>
                <filter id="turbulence3">
                    <feTurbulence type="fractalNoise" baseFrequency="0.008 0.022" numOctaves="3" seed="3" />
                    <feDisplacementMap in="SourceGraphic" scale="2" />
                </filter>
                <filter id="turbulence4">
                    <feTurbulence type="fractalNoise" baseFrequency="0.015 0.015" numOctaves="3" seed="4" />
                    <feDisplacementMap in="SourceGraphic" scale="3" />
                </filter>
            </defs>
        `;
        document.body.appendChild(svg);
    },

    initializeCloudBorders() {
        document.addEventListener('DOMContentLoaded', () => {
            // Find all elements with storm-cloud-border attribute
            const cloudBorders = document.querySelectorAll('[data-storm-cloud="border"]');
            
            cloudBorders.forEach(border => {
                this.createCloudBorder(border);
            });
        });
    },

    createCloudBorder(element) {
        // Clear existing content
        element.innerHTML = '';
        element.classList.add('storm-cloud-border');

        // Create cloud layers
        for (let i = 1; i <= 3; i++) {
            const layer = document.createElement('div');
            layer.className = `storm-cloud-layer storm-cloud-layer-${i}`;
            element.appendChild(layer);
        }

        // Create flash overlay
        const flash = document.createElement('div');
        flash.className = 'storm-cloud-flash';
        element.appendChild(flash);

        // Start lightning flashes
        this.startLightningFlashes(flash);
    },

    startLightningFlashes(flashElement) {
        const flash = () => {
            // Random delay between flashes
            const delay = Math.random() * this.config.animations.flashFrequency + 3000;
            
            setTimeout(() => {
                flashElement.classList.add('active');
                
                setTimeout(() => {
                    flashElement.classList.remove('active');
                }, 300);
                
                // Continue flashing
                flash();
            }, delay);
        };

        // Start the flash cycle
        flash();
    },

    createWisps(container) {
        // Create initial wisps
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                this.createSingleWisp(container);
            }, i * 5000);
        }

        // Continue creating wisps
        setInterval(() => {
            this.createSingleWisp(container);
        }, 10000);
    },

    createSingleWisp(container) {
        const wisp = document.createElement('div');
        wisp.className = 'storm-cloud-wisp';
        
        // Random vertical position
        const yPos = Math.random() * 60;
        wisp.style.top = `${yPos}px`;
        
        // Random size
        const scale = 0.8 + Math.random() * 0.4;
        wisp.style.transform = `scale(${scale})`;
        
        // Random animation duration
        const duration = 12000 + Math.random() * 8000;
        wisp.style.animationDuration = `${duration}ms`;
        
        container.appendChild(wisp);
        
        // Remove wisp after animation
        setTimeout(() => wisp.remove(), duration);
    },

    setupEventListeners(StormEvents) {
        // Listen for custom storm events
        StormEvents.on('cloud:thunder', (data) => {
            const borders = document.querySelectorAll('.storm-cloud-border');
            borders.forEach(border => {
                const flash = border.querySelector('.storm-cloud-flash');
                if (flash) {
                    flash.classList.add('active');
                    setTimeout(() => flash.classList.remove('active'), 300);
                }
            });
        });

        // Add interactivity
        document.addEventListener('click', (e) => {
            if (e.target.closest('.storm-cloud-border')) {
                StormEvents.trigger('cloud:thunder', {});
            }
        });
    }
};

// Auto-initialize when Storm Events is available
if (typeof window !== 'undefined') {
    window.StormCloudBorderPlugin = StormCloudBorderPlugin;
}

// Export for module systems
export default StormCloudBorderPlugin;
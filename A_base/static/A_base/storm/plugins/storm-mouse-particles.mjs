// Project: StormDevelopmentDjango/base/static/base/mjs/storm-events/plugins/storm-mouse-particles.mjs
// Storm Events Mouse-Based Particle System Plugin
// Smart mouse position detection and reusable particle animations

/**
 * 🌩️ STORM MOUSE PARTICLES PLUGIN
 *
 * Advanced mouse-based particle system that integrates with Storm Event System
 * and Storm Animation System for smooth, reusable click-based animations.
 *
 * Features:
 * - Smart mouse position detection (handles scrolling, viewport, zoom)
 * - Reusable particle factory system
 * - Integration with Storm Animation System
 * - Performance optimization with requestAnimationFrame
 * - Accessibility support (reduced motion)
 * - Business analytics integration
 * - Multiple particle types (M-shape, lightning, sparkles, custom)
 *
 * Usage:
 * StormEvents.trigger('mouse:particle-burst', {
 *     mouseEvent: clickEvent,
 *     particleType: 'mystery-m-shape',
 *     particleCount: 5,
 *     source: 'storm-cloud'
 * });
 */

export const StormMouseParticlesPlugin = {
    name: 'StormMouseParticles',
    version: '1.0.0',

    // Plugin configuration
    config: {
        debug: false,
        analytics: false,
        performance: {
            maxConcurrentParticles: 100,
            useRequestAnimationFrame: true,
            enableGPUAcceleration: true
        },
        accessibility: {
            respectReducedMotion: true,
            fallbackDuration: 300
        }
    },

    // Plugin state
    state: {
        activeParticles: new Set(),
        particleCount: 0,
        startTime: performance.now(),
        lastMouseEvent: null
    },

    // Particle type definitions
    particleTypes: {
        'mystery-m-shape': {
            count: 5,
            positions: [
                { x: -60, y: 40 }, // Bottom left of M
                { x: -30, y: -20 }, // Top left of M
                { x: 0, y: 20 }, // Center valley of M
                { x: 30, y: -20 }, // Top right of M
                { x: 60, y: 40 } // Bottom right of M
            ],
            randomOffset: 10,
            size: 8,
            colors: ['var(--storm-cyan)', 'var(--storm-blue)'],
            duration: 2500,
            animation: 'mysteryParticle'
        },

        'lightning-bolts': {
            count: 3,
            positions: [
                { x: -50, y: 0 }, // Left bolt
                { x: 0, y: 0 }, // Center bolt
                { x: 50, y: 0 } // Right bolt
            ],
            randomOffset: 20,
            size: { width: 4, height: 20 },
            colors: ['var(--storm-blue)', 'var(--storm-yellow)'],
            duration: 800,
            animation: 'lightningBolt'
        },

        sparkles: {
            count: 20,
            positions: 'random-circle', // Special position type
            circleRadius: 100,
            randomOffset: 0,
            size: 5,
            colors: ['var(--storm-blue)', 'var(--storm-yellow)'],
            duration: 1200,
            animation: 'sparkleParticle'
        },

        custom: {
            count: 1,
            positions: [{ x: 0, y: 0 }],
            randomOffset: 0,
            size: 10,
            colors: ['var(--storm-yellow)'],
            duration: 1000,
            animation: 'customParticle'
        }
    },

    // Initialize plugin
    init(stormEvents) {
        this.stormEvents = stormEvents;
        this.registerEvents();
        this.injectStyles();
        this.setupAccessibility();

        if (this.config.debug) {
            // Storm Mouse Particles Plugin initialized
        }
    },

    // Register event listeners
    registerEvents() {
        // Main particle burst event
        this.stormEvents.on('mouse:particle-burst', data => {
            this.createParticleBurst(data);
        });

        // Position testing event
        this.stormEvents.on('mouse:position-test', data => {
            this.testMousePosition(data);
        });

        // Cleanup event
        this.stormEvents.on('mouse:cleanup-particles', () => {
            this.cleanupAllParticles();
        });

        // Analytics event
        this.stormEvents.on('mouse:particle-analytics', data => {
            this.trackParticleAnalytics(data);
        });

        // Downward lightning bolts event (separate from particle bursts)
        this.stormEvents.on('mouse:lightning-bolts', data => {
            this.createDownwardLightningBolts(data);
        });

        // Rain animation removed - user requested to remove rain effects
    },

    // Smart mouse position detection
    getSmartMousePosition(mouseEvent) {
        if (!mouseEvent) {
            this.log('⚠️ No mouse event provided, using fallback position');
            return { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        }

        // Method 1: Use pageX/pageY for scroll-aware positioning
        if (mouseEvent.pageX !== undefined && mouseEvent.pageY !== undefined) {
            return {
                x: mouseEvent.pageX,
                y: mouseEvent.pageY,
                method: 'pageXY'
            };
        }

        // Method 2: Calculate from clientX/clientY + scroll offset
        if (mouseEvent.clientX !== undefined && mouseEvent.clientY !== undefined) {
            const scrollX = window.pageXOffset || document.documentElement.scrollLeft || 0;
            const scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;

            return {
                x: mouseEvent.clientX + scrollX,
                y: mouseEvent.clientY + scrollY,
                method: 'clientXY+scroll'
            };
        }

        // Method 3: Fallback to center of viewport
        this.log('⚠️ Mouse position fallback used');
        return {
            x: window.innerWidth / 2,
            y: window.innerHeight / 2,
            method: 'fallback'
        };
    },

    // Get position relative to specific element
    getRelativeMousePosition(mouseEvent, element) {
        const mousePos = this.getSmartMousePosition(mouseEvent);
        const rect = element.getBoundingClientRect();
        const scrollX = window.pageXOffset || document.documentElement.scrollLeft || 0;
        const scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;

        return {
            x: mousePos.x - (rect.left + scrollX),
            y: mousePos.y - (rect.top + scrollY),
            absolute: mousePos
        };
    },

    // Create particle burst
    createParticleBurst(data) {
        const {
            mouseEvent,
            particleType = 'sparkles',
            particleCount,
            source = 'unknown',
            customConfig = {}
        } = data;

        // Get particle configuration
        const config = { ...this.particleTypes[particleType], ...customConfig };
        if (!config) {
            this.log(`⚠️ Unknown particle type: ${particleType}`);
            return;
        }

        // Override count if specified
        if (particleCount) {
            config.count = particleCount;
        }

        // Get smart mouse position
        const mousePos = this.getSmartMousePosition(mouseEvent);

        // Check performance limits
        if (this.state.activeParticles.size >= this.config.performance.maxConcurrentParticles) {
            this.log('⚠️ Max concurrent particles reached, skipping burst');
            return;
        }

        // Create particles
        const particles = this.createParticles(mousePos, config, particleType);

        // Track analytics
        if (this.config.analytics) {
            this.trackParticleAnalytics({
                type: particleType,
                count: particles.length,
                source,
                position: mousePos,
                timestamp: Date.now()
            });
        }

        // Trigger Storm Event for business analytics
        this.stormEvents.trigger('business:user-engaged', {
            action: 'particle-burst',
            element: `${source}-${particleType}`,
            particleCount: particles.length
        });

        this.log(
            `✨ Created ${particles.length} particles of type "${particleType}" at position`,
            mousePos
        );

        return particles;
    },

    // Create downward traveling lightning bolts (separate from particle system)
    createDownwardLightningBolts(data) {
        const { mouseEvent, source = 'unknown', boltCount = 3 } = data;

        // Get smart mouse position or fallback to element center
        let centerX;
        let centerY;
        if (mouseEvent) {
            const mousePos = this.getSmartMousePosition(mouseEvent);
            centerX = mousePos.x;
            centerY = mousePos.y;
        } else {
            // Fallback to screen center
            centerX = window.innerWidth / 2;
            centerY = 100;
        }

        // Create 3 lightning bolts that travel down from the cloud
        const cloudPositions = [
            { x: centerX - 50, name: 'left' }, // Left cloud section
            { x: centerX, name: 'center' }, // Center cloud section
            { x: centerX + 50, name: 'right' } // Right cloud section
        ];

        for (let i = 0; i < Math.min(boltCount, cloudPositions.length); i++) {
            const bolt = this.createDownwardLightningBolt(cloudPositions[i], centerY);
            if (bolt) {
                this.state.activeParticles.add(bolt);
            }
        }

        // Track analytics
        if (this.config.analytics) {
            this.trackParticleAnalytics({
                type: 'downward-lightning',
                count: boltCount,
                source,
                position: { x: centerX, y: centerY },
                timestamp: Date.now()
            });
        }

        // Trigger Storm Event for business analytics
        this.stormEvents.trigger('business:user-engaged', {
            action: 'lightning-bolts',
            element: `${source}-downward-lightning`,
            boltCount
        });

        this.log(`⚡ Created ${boltCount} downward lightning bolts at position`, {
            x: centerX,
            y: centerY
        });
    },

    // Create single downward lightning bolt
    createDownwardLightningBolt(position, startY) {
        const bolt = document.createElement('div');
        bolt.className = 'storm-lightning-bolt-downward';
        bolt.id = `storm-lightning-bolt-${this.state.particleCount++}`;

        // Calculate bolt properties
        const distance = 120 + Math.random() * 80; // How far down it travels
        const angle = Math.PI / 2 + (Math.random() - 0.5) * 0.3; // Mostly downward with slight randomness
        const endX = position.x + Math.cos(angle) * (Math.random() - 0.5) * 40; // Slight horizontal drift
        const endY = startY + distance;

        // Set bolt styles
        bolt.style.cssText = `
            position: absolute;
            width: 4px;
            height: 20px;
            background: linear-gradient(to bottom, var(--storm-blue), var(--storm-yellow), var(--storm-yellow));
            border-radius: 2px;
            pointer-events: none;
            z-index: 1000;
            left: ${position.x}px;
            top: ${startY}px;
            transform-origin: top center;
            box-shadow: 0 0 10px var(--storm-yellow);
            animation: stormLightningBoltDownward 0.8s ease-out forwards;
        `;

        // Set CSS variables for animation
        bolt.style.setProperty('--end-x', `${endX - position.x}px`);
        bolt.style.setProperty('--end-y', `${endY - startY}px`);
        bolt.style.setProperty('--rotation', `${(Math.random() - 0.5) * 20}deg`);

        // Add to DOM
        document.body.appendChild(bolt);

        // Schedule cleanup
        setTimeout(() => {
            this.cleanupParticle(bolt);
        }, 800);

        return bolt;
    },

    // Rain animation removed - user requested to remove rain effects
    /*
    createRainAnimation(data) {
        // This method has been removed to eliminate rain animations
        // User requested to remove rain effects from the storm cloud
        return [];
    },
    */

    // Rain methods removed - user requested to remove rain effects
    /*
    getRainParameters(intensity) {
        // This method has been removed to eliminate rain animations
        return { dropCount: 0, dropSize: 0, fallSpeed: 0, spreadTime: 0 };
    },
    */

    // Rain methods removed - user requested to remove rain effects
    /*
    createRainDrop(originX, originY, cloudWidth, params) {
        // This method has been removed to eliminate rain animations
        return null;
    },
    */

    // Create individual particles
    createParticles(centerPos, config, particleType) {
        const particles = [];

        for (let i = 0; i < config.count; i++) {
            const particle = this.createSingleParticle(centerPos, config, i, particleType);
            if (particle) {
                particles.push(particle);
            }
        }

        return particles;
    },

    // Create single particle
    createSingleParticle(centerPos, config, index, particleType) {
        // Create particle element
        const particle = document.createElement('div');
        particle.className = `storm-particle storm-particle-${particleType}`;
        particle.id = `storm-particle-${this.state.particleCount++}`;

        // Calculate particle position
        const particlePos = this.calculateParticlePosition(centerPos, config, index);

        // Set particle styles
        this.setParticleStyles(particle, particlePos, config, index);

        // Add to DOM
        document.body.appendChild(particle);

        // Add to active particles
        this.state.activeParticles.add(particle);

        // Animate particle
        this.animateParticle(particle, particlePos, config);

        // Schedule cleanup
        setTimeout(() => {
            this.cleanupParticle(particle);
        }, config.duration);

        return particle;
    },

    // Calculate particle position
    calculateParticlePosition(centerPos, config, index) {
        let targetPos;

        if (config.positions === 'random-circle') {
            // Random circle formation
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * config.circleRadius;
            targetPos = {
                x: centerPos.x + Math.cos(angle) * distance,
                y: centerPos.y + Math.sin(angle) * distance
            };
        } else {
            // Predefined positions
            const basePos = config.positions[index] || { x: 0, y: 0 };
            const randomOffset = config.randomOffset || 0;

            targetPos = {
                x: centerPos.x + basePos.x + (Math.random() - 0.5) * randomOffset,
                y: centerPos.y + basePos.y + (Math.random() - 0.5) * randomOffset
            };
        }

        return {
            start: centerPos,
            end: targetPos
        };
    },

    // Set particle styles
    setParticleStyles(particle, particlePos, config, index) {
        const color = config.colors[index % config.colors.length];
        const size = config.size;

        // Base styles
        particle.style.cssText = `
            position: absolute;
            pointer-events: none;
            z-index: 1001;
            left: ${particlePos.start.x}px;
            top: ${particlePos.start.y}px;
            width: ${typeof size === 'object' ? size.width : size}px;
            height: ${typeof size === 'object' ? size.height : size}px;
            background: ${color};
            border-radius: 50%;
            box-shadow: 0 0 10px ${color};
            transition: none;
        `;

        // GPU acceleration
        if (this.config.performance.enableGPUAcceleration) {
            particle.style.willChange = 'transform, opacity';
            particle.style.transform = 'translateZ(0)';
        }

        // Set CSS variables for animation
        particle.style.setProperty('--end-x', `${particlePos.end.x - particlePos.start.x}px`);
        particle.style.setProperty('--end-y', `${particlePos.end.y - particlePos.start.y}px`);
        particle.style.setProperty('--rotation', `${(Math.random() - 0.5) * 360}deg`);
        particle.style.setProperty('--scale', `${0.5 + Math.random() * 0.5}`);
    },

    // Animate particle
    animateParticle(particle, particlePos, config) {
        const duration =
            this.config.accessibility.respectReducedMotion &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches
                ? this.config.accessibility.fallbackDuration
                : config.duration;

        // Set animation
        particle.style.animation = `${config.animation} ${duration}ms ease-out forwards`;

        // Manual animation fallback for better control
        if (this.config.performance.useRequestAnimationFrame) {
            this.manualAnimateParticle(particle, particlePos, duration);
        }
    },

    // Manual animation using requestAnimationFrame
    manualAnimateParticle(particle, particlePos, duration) {
        const startTime = performance.now();
        const startPos = particlePos.start;
        const endPos = particlePos.end;

        const animate = currentTime => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (ease-out)
            const eased = 1 - Math.pow(1 - progress, 3);

            // Calculate current position
            const currentX = startPos.x + (endPos.x - startPos.x) * eased;
            const currentY = startPos.y + (endPos.y - startPos.y) * eased;

            // Apply transform
            particle.style.left = `${currentX}px`;
            particle.style.top = `${currentY}px`;
            particle.style.opacity = 1 - progress;
            particle.style.transform = `scale(${1 - progress * 0.5}) rotate(${progress * 360}deg)`;

            // Continue animation
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    },

    // Test mouse position (debug utility)
    testMousePosition(data) {
        const mousePos = this.getSmartMousePosition(data.mouseEvent);

        // Create test marker
        const marker = document.createElement('div');
        marker.style.cssText = `
            position: absolute;
            left: ${mousePos.x - 5}px;
            top: ${mousePos.y - 5}px;
            width: 10px;
            height: 10px;
            background: red;
            border-radius: 50%;
            z-index: 10000;
            pointer-events: none;
        `;

        document.body.appendChild(marker);

        // Remove after 3 seconds
        setTimeout(() => marker.remove(), 3000);

        this.log('🎯 Mouse position test marker created at', mousePos);
    },

    // Cleanup single particle
    cleanupParticle(particle) {
        if (particle && particle.parentNode) {
            particle.remove();
        }
        this.state.activeParticles.delete(particle);
    },

    // Cleanup all particles
    cleanupAllParticles() {
        this.state.activeParticles.forEach(particle => {
            if (particle && particle.parentNode) {
                particle.remove();
            }
        });
        this.state.activeParticles.clear();
        this.log('🧹 All particles cleaned up');
    },

    // Track particle analytics
    trackParticleAnalytics(data) {
        const analyticsData = {
            type: data.type,
            count: data.count,
            source: data.source,
            position: data.position,
            timestamp: data.timestamp || Date.now(),
            session: {
                totalParticles: this.state.particleCount,
                activeParticles: this.state.activeParticles.size,
                uptime: performance.now() - this.state.startTime
            }
        };

        // Send to business analytics
        this.stormEvents.trigger('analytics:particle-interaction', analyticsData);

        if (this.config.debug) {
            // Particle analytics tracked
        }
    },

    // Setup accessibility
    setupAccessibility() {
        // Listen for reduced motion changes
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
            mediaQuery.addListener(() => {
                this.log(`♿ Reduced motion preference changed: ${mediaQuery.matches}`);
            });
        }
    },

    // Inject CSS styles for particles
    injectStyles() {
        const styles = `
            <style id="storm-mouse-particles-styles">
            /* Storm Mouse Particles - Generated Styles */

            @keyframes mysteryParticle {
                0% {
                    transform: translate(0, 0) scale(1) rotate(0deg);
                    opacity: 1;
                    box-shadow: 0 0 15px var(--storm-cyan);
                }
                25% {
                    transform: translate(calc(var(--end-x) * 0.3), calc(var(--end-y) * 0.3)) scale(1.5) rotate(90deg);
                    opacity: 0.9;
                    box-shadow: 0 0 25px var(--storm-cyan);
                }
                50% {
                    transform: translate(calc(var(--end-x) * 0.7), calc(var(--end-y) * 0.7)) scale(1.2) rotate(180deg);
                    opacity: 0.8;
                    box-shadow: 0 0 20px var(--storm-blue);
                }
                75% {
                    transform: translate(calc(var(--end-x) * 0.9), calc(var(--end-y) * 0.9)) scale(0.8) rotate(270deg);
                    opacity: 0.4;
                    box-shadow: 0 0 15px var(--storm-blue);
                }
                100% {
                    transform: translate(var(--end-x), var(--end-y)) scale(0.2) rotate(360deg);
                    opacity: 0;
                    box-shadow: 0 0 8px var(--storm-cyan);
                }
            }

            @keyframes lightningBolt {
                0% {
                    transform: translate(0, 0) rotate(var(--rotation)) scale(1);
                    opacity: 1;
                    height: 20px;
                }
                25% {
                    transform: translate(calc(var(--end-x) * 0.2), calc(var(--end-y) * 0.2)) rotate(var(--rotation)) scale(1.1);
                    opacity: 0.9;
                    height: 40px;
                }
                50% {
                    transform: translate(calc(var(--end-x) * 0.6), calc(var(--end-y) * 0.6)) rotate(var(--rotation)) scale(1.2);
                    opacity: 0.8;
                    height: 60px;
                }
                100% {
                    transform: translate(var(--end-x), var(--end-y)) rotate(var(--rotation)) scale(0.8);
                    opacity: 0;
                    height: 80px;
                }
            }

            @keyframes sparkleParticle {
                0% {
                    transform: translate(0, 0) scale(1) rotate(0deg);
                    opacity: 1;
                    box-shadow: 0 0 8px currentColor;
                }
                50% {
                    transform: translate(calc(var(--end-x) * 0.6), calc(var(--end-y) * 0.6)) scale(1.5) rotate(180deg);
                    opacity: 0.8;
                    box-shadow: 0 0 15px currentColor;
                }
                100% {
                    transform: translate(var(--end-x), var(--end-y)) scale(0.3) rotate(360deg);
                    opacity: 0;
                    box-shadow: 0 0 5px currentColor;
                }
            }

            @keyframes customParticle {
                0% {
                    transform: translate(0, 0) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translate(var(--end-x), var(--end-y)) scale(0.5);
                    opacity: 0;
                }
            }

            @keyframes stormLightningBoltDownward {
                0% {
                    transform: translate(0, 0) rotate(var(--rotation)) scale(1);
                    opacity: 1;
                    height: 20px;
                }
                20% {
                    transform: translate(calc(var(--end-x) * 0.1), calc(var(--end-y) * 0.2)) rotate(var(--rotation)) scale(1.1);
                    opacity: 0.95;
                    height: 40px;
                }
                40% {
                    transform: translate(calc(var(--end-x) * 0.3), calc(var(--end-y) * 0.5)) rotate(var(--rotation)) scale(1.2);
                    opacity: 0.9;
                    height: 60px;
                }
                70% {
                    transform: translate(calc(var(--end-x) * 0.7), calc(var(--end-y) * 0.8)) rotate(var(--rotation)) scale(1.3);
                    opacity: 0.7;
                    height: 80px;
                }
                100% {
                    transform: translate(var(--end-x), var(--end-y)) rotate(var(--rotation)) scale(0.8);
                    opacity: 0;
                    height: 100px;
                }
            }

            @keyframes rainDropFall {
                0% {
                    transform: translate(0, 0);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                90% {
                    opacity: 0.8;
                }
                100% {
                    transform: translate(var(--end-x), var(--end-y));
                    opacity: 0;
                }
            }

            /* Rain drop styles */
            .storm-rain-drop {
                filter: blur(0.5px);
                box-shadow: 0 0 2px rgba(135, 206, 235, 0.3);
            }

            /* Accessibility: Respect reduced motion */
            @media (prefers-reduced-motion: reduce) {
                .storm-particle {
                    animation-duration: 300ms !important;
                }
            }

            /* Performance optimization */
            .storm-particle {
                will-change: transform, opacity;
                backface-visibility: hidden;
            }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
        this.log('💅 Mouse particle styles injected');
    },

    // Get performance metrics
    getPerformanceMetrics() {
        return {
            activeParticles: this.state.activeParticles.size,
            totalParticlesCreated: this.state.particleCount,
            uptime: performance.now() - this.state.startTime,
            averageParticlesPerSecond:
                this.state.particleCount / ((performance.now() - this.state.startTime) / 1000),
            memoryUsage: performance.memory
                ? Math.round(performance.memory.usedJSHeapSize / 1024 / 1024)
                : 0
        };
    },

    // Debug logging
    log(message, data = null) {
        if (this.config.debug) {
            const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
            console.log(`[${timestamp}] Storm Mouse Particles: ${message}`, data || '');
        }
    }
};

// Export default
export default StormMouseParticlesPlugin;

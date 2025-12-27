/**
 * Mobile Navbar Toggle
 * Handles hamburger menu open/close functionality
 */

class MobileNavbar {
  constructor() {
    this.toggle = document.querySelector('.mobile-menu-toggle');
    this.menu = document.getElementById('mobile-menu');
    this.isOpen = false;

    if (this.toggle && this.menu) {
      this.init();
    }
  }

  init() {
    // Toggle button click
    this.toggle.addEventListener('click', (e) => {
      e.preventDefault();
      this.toggleMenu();
    });

    // Close menu when clicking a link
    this.menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        this.closeMenu();
      });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (this.isOpen &&
          !this.menu.contains(e.target) &&
          !this.toggle.contains(e.target)) {
        this.closeMenu();
      }
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.closeMenu();
      }
    });

    // Close menu on resize to desktop
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 768 && this.isOpen) {
        this.closeMenu();
      }
    });
  }

  toggleMenu() {
    if (this.isOpen) {
      this.closeMenu();
    } else {
      this.openMenu();
    }
  }

  openMenu() {
    this.isOpen = true;
    this.toggle.classList.add('active');
    this.toggle.setAttribute('aria-expanded', 'true');
    this.menu.classList.add('open');
  }

  closeMenu() {
    this.isOpen = false;
    this.toggle.classList.remove('active');
    this.toggle.setAttribute('aria-expanded', 'false');
    this.menu.classList.remove('open');
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new MobileNavbar());
} else {
  new MobileNavbar();
}

export default MobileNavbar;

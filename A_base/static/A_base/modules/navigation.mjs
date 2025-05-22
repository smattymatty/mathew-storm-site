const TIME_TO_REMOVE_CLICK_ANIMATION = 370;

// navigation.mjs
export function setupNavLinks(initialActive = "home") {
  const navLinks = document.querySelectorAll(".nav-links a, .nav-title");

  navLinks.forEach((link) => {
    link.addEventListener("mousedown", (e) => {
      e.preventDefault();
      link.classList.add("click-animation");

      navLinks.forEach((navLink) => {
        navLink.classList.remove("active");
      });

      link.classList.add("active");

      setTimeout(() => {
        link.classList.remove("click-animation");
      }, TIME_TO_REMOVE_CLICK_ANIMATION);
    });
  });

  // Set initial states
  const initialNavLink = document.querySelector(`#${initialActive}`);
  if (initialNavLink) {
    initialNavLink.classList.add("active");
    }
  
}
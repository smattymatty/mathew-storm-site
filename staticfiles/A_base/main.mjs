// main.mjs
import { setupNavLinks } from "./modules/navigation.mjs";

async function initializeApp() {
  console.log("🚀 Initializing application");

  // Get initial route from URL
  const location = window.location.pathname;
  console.log(`🚀 Initial route: ${location}`);

  let initialPage = location.split("/")[1];
  console.log(`🚀 Initial page: ${initialPage}`);

  if (initialPage === "") {
    initialPage = "home";
  }
  console.log(`🚀 Initial page: ${initialPage}`);
  setupNavLinks(initialPage);
}
// INIT
initializeApp();
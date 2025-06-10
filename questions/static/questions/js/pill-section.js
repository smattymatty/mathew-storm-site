// questions/static/questions/js/pill-selection.js

class PillSelectionManager {
  constructor() {
    this.selectedFilters = new Map(); // Map<string, {type: string, value: string, display: string}>
    this.init();
  }

  init() {
    // Event delegation for pill clicks
    document.addEventListener("click", (e) => {
      if (e.target.matches(".pill-selectable")) {
        this.handlePillClick(e.target);
      } else if (e.target.matches(".selected-pill")) {
        this.handleSelectedPillClick(e.target);
      }
    });
  }

  handlePillClick(pillElement) {
    const type = pillElement.dataset.pillType;
    const value = pillElement.dataset.pillValue;
    const display = pillElement.dataset.pillDisplay;

    // Toggle selection
    const key = `${type}-${value}`;
    if (this.selectedFilters.has(key)) {
      this.removeFilter(key);
    } else {
      this.addFilter(key, { type, value, display });
    }

    this.updateUI();
  }

  handleSelectedPillClick(selectedPillElement) {
    const key = selectedPillElement.dataset.filterKey;
    this.removeFilter(key);
    this.updateUI();
  }

  addFilter(key, filter) {
    // Allow multiple selections for both tutorials and tags
    this.selectedFilters.set(key, filter);
  }

  removeFilter(key) {
    this.selectedFilters.delete(key);
  }

  updateUI() {
    this.updateSourcePills();
    this.updateSelectedContainer();
  }

  updateSourcePills() {
    // Update visual state of source pills
    document.querySelectorAll(".pill-selectable").forEach((pill) => {
      const type = pill.dataset.pillType;
      const value = pill.dataset.pillValue;
      const key = `${type}-${value}`;

      pill.classList.toggle("selected", this.selectedFilters.has(key));
    });
  }

  updateSelectedContainer() {
    const container = document.getElementById("selected-pills-list");
    const emptyState = container.querySelector(".empty-state");

    // Clear existing selected pills (but keep empty state)
    container
      .querySelectorAll(".selected-pill")
      .forEach((pill) => pill.remove());

    if (this.selectedFilters.size === 0) {
      container.classList.add("empty");
      emptyState.style.display = "flex";
    } else {
      container.classList.remove("empty");
      emptyState.style.display = "none";

      // Add selected pills
      for (const [key, filter] of this.selectedFilters) {
        const selectedPill = this.createSelectedPill(key, filter);
        container.appendChild(selectedPill);
      }
    }
  }

  createSelectedPill(key, filter) {
    const pill = document.createElement("div");
    pill.className = `selected-pill ${filter.type}-name-pill sb-p-2 sb-rounded sb-text-xs sb-text-center sb-cursor-pointer`;
    pill.dataset.filterKey = key;
    pill.textContent = filter.display;
    pill.title = `Click to remove ${filter.display}`;
    return pill;
  }

  // Method to get current selections for HTMX requests
  getSelectedFilters() {
    const tutorials = [];
    const tags = [];

    for (const filter of this.selectedFilters.values()) {
      if (filter.type === "tutorial") {
        tutorials.push(filter.value);
      } else if (filter.type === "tag") {
        tags.push(filter.value);
      }
    }

    return { tutorials, tags };
  }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  window.pillSelectionManager = new PillSelectionManager();
});

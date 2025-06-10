/**
 * questions/static/questions/mjs/utils.mjs
 * Utilities for collecting and managing quiz filter data
 */

/**
 * Collects all selected pills from the PillSelectionManager
 * @returns {Object} Object containing tutorials, tags, and difficulties arrays
 */
export function collectSelectedFilters() {
  const pillManager = window.pillSelectionManager;
  if (!pillManager) {
    console.warn("PillSelectionManager not found");
    return { tutorials: [], tags: [], difficulties: [] };
  }

  const tutorials = [];
  const tags = [];
  const difficulties = [];

  // Iterate through all selected filters
  for (const filter of pillManager.selectedFilters.values()) {
    switch (filter.type) {
      case "tutorial":
        tutorials.push(filter.value);
        break;
      case "tag":
        tags.push(filter.value);
        break;
      case "difficulty":
        difficulties.push(filter.value);
        break;
      default:
        console.warn(`Unknown filter type: ${filter.type}`);
    }
  }

  return { tutorials, tags, difficulties };
}

/**
 * Formats selected filters for HTMX request
 * @returns {Object} Object formatted for HTMX hx-vals, omitting empty values
 */
export function formatFiltersForHTMX() {
  const filters = collectSelectedFilters();
  const htmxParams = {};

  // Only add parameters if they have values
  if (filters.tutorials.length > 0) {
    htmxParams["title-id"] = filters.tutorials.join(",");
  }

  if (filters.tags.length > 0) {
    htmxParams["tags"] = filters.tags.join(",");
  }

  if (filters.difficulties.length > 0) {
    htmxParams["difficulty"] = filters.difficulties.join(",");
  }

  return htmxParams;
}

/**
 * Logs current filter state for debugging
 */
export function debugFilters() {
  const filters = collectSelectedFilters();
  const htmxFormat = formatFiltersForHTMX();

  console.group("🔍 Current Filter State");
  console.log("Raw filters:", filters);
  console.log("HTMX format:", htmxFormat);
  console.log(
    "Total selected:",
    filters.tutorials.length +
      filters.tags.length +
      filters.difficulties.length,
  );
  console.groupEnd();
}

/**
 * Validates that at least one filter is selected
 * @returns {boolean} True if any filters are selected
 */
export function hasSelectedFilters() {
  const filters = collectSelectedFilters();
  return (
    filters.tutorials.length > 0 ||
    filters.tags.length > 0 ||
    filters.difficulties.length > 0
  );
}

/*global gettext, interpolate, ngettext*/
'use strict';
{
    /**
     * Makes all elements matching the selector visible by removing the 'hidden' class.
     *
     * @param {string} selector - A CSS selector for the elements to show.
     */
    function show(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            el.classList.remove('hidden');
        });
    }

    /**
     * Hides all elements matching the given selector by adding the 'hidden' class.
     *
     * @param {string} selector - A CSS selector identifying elements to hide.
     */
    function hide(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            el.classList.add('hidden');
        });
    }

    /**
     * Displays the bulk action question prompt and hides clear selection and all actions containers.
     *
     * @param {Object} options - Configuration object containing selectors for UI elements.
     */
    function showQuestion(options) {
        hide(options.acrossClears);
        show(options.acrossQuestions);
        hide(options.allContainer);
    }

    /**
     * Updates the UI to display the option for clearing bulk selections.
     *
     * Shows elements for clearing selections, hides question prompts, removes the selected class from the action container, displays the all actions container, and hides the counter container.
     */
    function showClear(options) {
        show(options.acrossClears);
        hide(options.acrossQuestions);
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
        show(options.allContainer);
        hide(options.counterContainer);
    }

    /**
     * Resets the bulk action UI to its default state by hiding selection prompts and showing the counter container.
     */
    function reset(options) {
        hide(options.acrossClears);
        hide(options.acrossQuestions);
        hide(options.allContainer);
        show(options.counterContainer);
    }

    /**
     * Clears the "select across all pages" option and resets the bulk action UI state.
     *
     * Resets the UI, sets all inputs matching the across input selector to zero, and removes the selected class from the action container.
     */
    function clearAcross(options) {
        reset(options);
        const acrossInputs = document.querySelectorAll(options.acrossInput);
        acrossInputs.forEach(function(acrossInput) {
            acrossInput.value = 0;
        });
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
    }

    /**
     * Sets the checked state for all action checkboxes and updates the UI to reflect bulk selection.
     *
     * If {@link checked} is true, displays the bulk action question prompt; otherwise, resets the selection UI.
     *
     * @param {NodeList|Array<HTMLInputElement>} actionCheckboxes - The checkboxes to update.
     * @param {Object} options - Configuration options for UI class names and selectors.
     * @param {boolean} checked - Whether to check or uncheck all action checkboxes.
     */
    function checker(actionCheckboxes, options, checked) {
        if (checked) {
            showQuestion(options);
        } else {
            reset(options);
        }
        actionCheckboxes.forEach(function(el) {
            el.checked = checked;
            el.closest('tr').classList.toggle(options.selectedClass, checked);
        });
    }

    /**
     * Updates the selection counter display and toggles UI elements based on the number of checked action checkboxes.
     *
     * Updates the counter with a localized string showing how many items are selected out of the total. Toggles the "select all" checkbox and shows or hides bulk action prompts depending on whether all items are selected.
     */
    function updateCounter(actionCheckboxes, options) {
        const sel = Array.from(actionCheckboxes).filter(function(el) {
            return el.checked;
        }).length;
        const counter = document.querySelector(options.counterContainer);
        // data-actions-icnt is defined in the generated HTML
        // and contains the total amount of objects in the queryset
        const actions_icnt = Number(counter.dataset.actionsIcnt);
        counter.textContent = interpolate(
            ngettext('%(sel)s of %(cnt)s selected', '%(sel)s of %(cnt)s selected', sel), {
                sel: sel,
                cnt: actions_icnt
            }, true);
        const allToggle = document.getElementById(options.allToggleId);
        allToggle.checked = sel === actionCheckboxes.length;
        if (allToggle.checked) {
            showQuestion(options);
        } else {
            clearAcross(options);
        }
    }

    const defaults = {
        actionContainer: "div.actions",
        counterContainer: "span.action-counter",
        allContainer: "div.actions span.all",
        acrossInput: "div.actions input.select-across",
        acrossQuestions: "div.actions span.question",
        acrossClears: "div.actions span.clear",
        allToggleId: "action-toggle",
        selectedClass: "selected"
    };

    window.Actions = function(actionCheckboxes, options) {
        options = Object.assign({}, defaults, options);
        let list_editable_changed = false;
        let lastChecked = null;
        let shiftPressed = false;

        document.addEventListener('keydown', (event) => {
            shiftPressed = event.shiftKey;
        });

        document.addEventListener('keyup', (event) => {
            shiftPressed = event.shiftKey;
        });

        document.getElementById(options.allToggleId).addEventListener('click', function(event) {
            checker(actionCheckboxes, options, this.checked);
            updateCounter(actionCheckboxes, options);
        });

        document.querySelectorAll(options.acrossQuestions + " a").forEach(function(el) {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                const acrossInputs = document.querySelectorAll(options.acrossInput);
                acrossInputs.forEach(function(acrossInput) {
                    acrossInput.value = 1;
                });
                showClear(options);
            });
        });

        document.querySelectorAll(options.acrossClears + " a").forEach(function(el) {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                document.getElementById(options.allToggleId).checked = false;
                clearAcross(options);
                checker(actionCheckboxes, options, false);
                updateCounter(actionCheckboxes, options);
            });
        });

        /**
         * Returns the set of checkboxes affected by a selection action, supporting shift-click multi-selection.
         *
         * If shift-click is used and a previous checkbox was selected, returns all checkboxes in the range between the last checked and the current target. Otherwise, returns only the target checkbox.
         *
         * @param {HTMLInputElement} target - The checkbox that was interacted with.
         * @param {boolean} withModifier - Whether a modifier key (such as Shift) is held.
         * @returns {HTMLInputElement[]} Array of affected checkboxes.
         */
        function affectedCheckboxes(target, withModifier) {
            const multiSelect = (lastChecked && withModifier && lastChecked !== target);
            if (!multiSelect) {
                return [target];
            }
            const checkboxes = Array.from(actionCheckboxes);
            const targetIndex = checkboxes.findIndex(el => el === target);
            const lastCheckedIndex = checkboxes.findIndex(el => el === lastChecked);
            const startIndex = Math.min(targetIndex, lastCheckedIndex);
            const endIndex = Math.max(targetIndex, lastCheckedIndex);
            const filtered = checkboxes.filter((el, index) => (startIndex <= index) && (index <= endIndex));
            return filtered;
        };

        Array.from(document.getElementById('result_list').tBodies).forEach(function(el) {
            el.addEventListener('change', function(event) {
                const target = event.target;
                if (target.classList.contains('action-select')) {
                    const checkboxes = affectedCheckboxes(target, shiftPressed);
                    checker(checkboxes, options, target.checked);
                    updateCounter(actionCheckboxes, options);
                    lastChecked = target;
                } else {
                    list_editable_changed = true;
                }
            });
        });

        document.querySelector('#changelist-form button[name=index]').addEventListener('click', function(event) {
            if (list_editable_changed) {
                const confirmed = confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."));
                if (!confirmed) {
                    event.preventDefault();
                }
            }
        });

        const el = document.querySelector('#changelist-form input[name=_save]');
        // The button does not exist if no fields are editable.
        if (el) {
            el.addEventListener('click', function(event) {
                if (document.querySelector('[name=action]').value) {
                    const text = list_editable_changed
                        ? gettext("You have selected an action, but you haven’t saved your changes to individual fields yet. Please click OK to save. You’ll need to re-run the action.")
                        : gettext("You have selected an action, and you haven’t made any changes on individual fields. You’re probably looking for the Go button rather than the Save button.");
                    if (!confirm(text)) {
                        event.preventDefault();
                    }
                }
            });
        }
        // Sync counter when navigating to the page, such as through the back
        // button.
        window.addEventListener('pageshow', (event) => updateCounter(actionCheckboxes, options));
    };

    // Call function fn when the DOM is loaded and ready. If it is already
    // loaded, call the function now.
    /**
     * Executes a function when the DOM is fully loaded.
     *
     * If the DOM is already ready, the function is called immediately; otherwise, it is called after the DOMContentLoaded event.
     *
     * @param {Function} fn - The function to execute when the DOM is ready.
     */
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    ready(function() {
        const actionsEls = document.querySelectorAll('tr input.action-select');
        if (actionsEls.length > 0) {
            Actions(actionsEls);
        }
    });
}

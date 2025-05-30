/*global SelectBox, interpolate*/
// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.
'use strict';
{
    const $ = django.jQuery;
    let popupIndex = 0;
    const relatedWindows = [];

    /**
     * Closes all open related-object popup windows and their child popups recursively.
     *
     * Iterates through the list of tracked related windows, dismissing any child popups before closing each window.
     */
    function dismissChildPopups() {
        relatedWindows.forEach(function(win) {
            if(!win.closed) {
                win.dismissChildPopups();
                win.close();    
            }
        });
    }

    /**
     * Sets the current popup index based on the window's name.
     *
     * If the window was opened as a popup (detected by the presence of an element named "_popup"), extracts the popup index from the window's name. Otherwise, resets the popup index to 0.
     */
    function setPopupIndex() {
        if(document.getElementsByName("_popup").length > 0) {
            const index = window.name.lastIndexOf("__") + 2;
            popupIndex = parseInt(window.name.substring(index));   
        } else {
            popupIndex = 0;
        }
    }

    /**
     * Appends a unique popup index suffix to the given name.
     *
     * @param {string} name - The base name to which the popup index will be appended.
     * @returns {string} The name with a popup index suffix in the format `__<index>`.
     */
    function addPopupIndex(name) {
        return name + "__" + (popupIndex + 1);
    }

    /**
     * Removes the popup index suffix from a given name string.
     *
     * @param {string} name - The string from which to remove the popup index suffix.
     * @returns {string} The name without the `__<popupIndex+1>` suffix.
     */
    function removePopupIndex(name) {
        return name.replace(new RegExp("__" + (popupIndex + 1) + "$"), '');
    }

    /**
     * Opens a related object popup window with a unique name and optional popup parameter.
     *
     * @param {HTMLElement} triggeringLink - The link element that triggered the popup.
     * @param {RegExp} name_regexp - Regular expression to remove from the triggering link's ID for naming the popup.
     * @param {boolean} add_popup - Whether to add the `_popup=1` parameter to the popup URL.
     * @returns {boolean} Always returns false to prevent default link behavior.
     *
     * @remark The opened window is tracked in the {@link relatedWindows} array for lifecycle management.
     */
    function showAdminPopup(triggeringLink, name_regexp, add_popup) {
        const name = addPopupIndex(triggeringLink.id.replace(name_regexp, ''));
        const href = new URL(triggeringLink.href);
        if (add_popup) {
            href.searchParams.set('_popup', 1);
        }
        const win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
        relatedWindows.push(win);
        win.focus();
        return false;
    }

    /**
     * Opens a related object lookup popup window for a raw ID field in the admin interface.
     *
     * @param {HTMLElement} triggeringLink - The link element that triggers the popup.
     * @returns {Window|null} The opened popup window, or null if the popup could not be opened.
     */
    function showRelatedObjectLookupPopup(triggeringLink) {
        return showAdminPopup(triggeringLink, /^lookup_/, true);
    }

    /**
     * Updates the corresponding input field with the selected ID from a related lookup popup and closes the popup window.
     *
     * If the input is a ManyToMany raw ID field and already has a value, the new ID is appended; otherwise, the value is replaced.
     *
     * @param {Window} win - The popup window being dismissed.
     * @param {string} chosenId - The ID selected in the popup.
     */
    function dismissRelatedLookupPopup(win, chosenId) {
        const name = removePopupIndex(win.name);
        const elem = document.getElementById(name);
        if (elem.classList.contains('vManyToManyRawIdAdminField') && elem.value) {
            elem.value += ',' + chosenId;
        } else {
            document.getElementById(name).value = chosenId;
        }
        const index = relatedWindows.indexOf(win);
        if (index > -1) {
            relatedWindows.splice(index, 1);
        }
        win.close();
    }

    /**
     * Opens a popup window for adding, changing, or deleting a related object in the admin interface.
     *
     * @param {HTMLElement} triggeringLink - The link element that triggered the popup.
     * @returns {Window|null} The opened popup window, or null if the popup could not be opened.
     */
    function showRelatedObjectPopup(triggeringLink) {
        return showAdminPopup(triggeringLink, /^(change|add|delete)_/, false);
    }

    /**
     * Updates the URLs and enabled state of related object action links adjacent to an input or select element.
     *
     * If the input has a value, sets the `href` of sibling view, change, and delete links using their `data-href-template` and enables them. If the input is empty, disables these links and removes their `href` attributes.
     */
    function updateRelatedObjectLinks(triggeringLink) {
        const $this = $(triggeringLink);
        const siblings = $this.nextAll('.view-related, .change-related, .delete-related');
        if (!siblings.length) {
            return;
        }
        const value = $this.val();
        if (value) {
            siblings.each(function() {
                const elm = $(this);
                elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
                elm.removeAttr('aria-disabled');
            });
        } else {
            siblings.removeAttr('href');
            siblings.attr('aria-disabled', true);
        }
    }

    /**
     * Updates all related select elements on the page to reflect changes to a related object.
     *
     * After adding or editing a related object via a popup, this function updates all select elements referencing the same model (excluding autocomplete selects) by adding a new option or updating an existing one, except for the select that triggered the popup.
     *
     * @param {HTMLSelectElement} currentSelect - The select element that initiated the popup.
     * @param {Window} win - The popup window from which the model and action are determined.
     * @param {string} objId - The original ID of the related object (if editing).
     * @param {string} newRepr - The new display representation of the related object.
     * @param {string} newId - The new or updated ID of the related object.
     */
    function updateRelatedSelectsOptions(currentSelect, win, objId, newRepr, newId) {
        // After create/edit a model from the options next to the current
        // select (+ or :pencil:) update ForeignKey PK of the rest of selects
        // in the page.

        const path = win.location.pathname;
        // Extract the model from the popup url '.../<model>/add/' or
        // '.../<model>/<id>/change/' depending the action (add or change).
        const modelName = path.split('/')[path.split('/').length - (objId ? 4 : 3)];
        // Exclude autocomplete selects.
        const selectsRelated = document.querySelectorAll(`[data-model-ref="${modelName}"] select:not(.admin-autocomplete)`);

        selectsRelated.forEach(function(select) {
            if (currentSelect === select) {
                return;
            }

            let option = select.querySelector(`option[value="${objId}"]`);

            if (!option) {
                option = new Option(newRepr, newId);
                select.options.add(option);
                return;
            }

            option.textContent = newRepr;
            option.value = newId;
        });
    }

    /**
     * Handles closing the popup after adding a related object and updates the corresponding form field.
     *
     * Updates the target input or select element with the new object's ID and display text. For select elements, adds the new option and selects it; for ManyToMany raw ID fields, appends the new ID. If the element is not found, updates the SelectBox cache. Triggers a change event on the updated element and closes the popup window.
     *
     * @param {Window} win - The popup window being dismissed.
     * @param {string} newId - The ID of the newly added related object.
     * @param {string} newRepr - The display representation of the new object.
     */
    function dismissAddRelatedObjectPopup(win, newId, newRepr) {
        const name = removePopupIndex(win.name);
        const elem = document.getElementById(name);
        if (elem) {
            const elemName = elem.nodeName.toUpperCase();
            if (elemName === 'SELECT') {
                elem.options[elem.options.length] = new Option(newRepr, newId, true, true);
                updateRelatedSelectsOptions(elem, win, null, newRepr, newId);
            } else if (elemName === 'INPUT') {
                if (elem.classList.contains('vManyToManyRawIdAdminField') && elem.value) {
                    elem.value += ',' + newId;
                } else {
                    elem.value = newId;
                }
            }
            // Trigger a change event to update related links if required.
            $(elem).trigger('change');
        } else {
            const toId = name + "_to";
            const o = new Option(newRepr, newId);
            SelectBox.add_to_cache(toId, o);
            SelectBox.redisplay(toId);
        }
        const index = relatedWindows.indexOf(win);
        if (index > -1) {
            relatedWindows.splice(index, 1);
        }
        win.close();
    }

    /**
     * Handles closing the popup after editing a related object and updates all relevant select elements with the new representation and ID.
     *
     * Updates the text and value of matching options in related select boxes, refreshes Select2-rendered elements if present, and removes the popup window from the tracked list before closing it.
     *
     * @param {Window} win - The popup window being dismissed.
     * @param {string} objId - The original ID of the related object that was changed.
     * @param {string} newRepr - The new display representation for the related object.
     * @param {string} newId - The new ID for the related object.
     */
    function dismissChangeRelatedObjectPopup(win, objId, newRepr, newId) {
        const id = removePopupIndex(win.name.replace(/^edit_/, ''));
        const selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
        const selects = $(selectsSelector);
        selects.find('option').each(function() {
            if (this.value === objId) {
                this.textContent = newRepr;
                this.value = newId;
            }
        }).trigger('change');
        updateRelatedSelectsOptions(selects[0], win, objId, newRepr, newId);
        selects.next().find('.select2-selection__rendered').each(function() {
            // The element can have a clear button as a child.
            // Use the lastChild to modify only the displayed value.
            this.lastChild.textContent = newRepr;
            this.title = newRepr;
        });
        const index = relatedWindows.indexOf(win);
        if (index > -1) {
            relatedWindows.splice(index, 1);
        }
        win.close();
    }

    /**
     * Handles the dismissal of a related object delete popup and removes the deleted object from all relevant select elements.
     *
     * Removes any `<option>` elements with a value matching the deleted object's ID from associated select boxes, triggers a change event, and closes the popup window.
     *
     * @param {Window} win - The popup window being dismissed.
     * @param {string} objId - The ID of the object that was deleted.
     */
    function dismissDeleteRelatedObjectPopup(win, objId) {
        const id = removePopupIndex(win.name.replace(/^delete_/, ''));
        const selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
        const selects = $(selectsSelector);
        selects.find('option').each(function() {
            if (this.value === objId) {
                $(this).remove();
            }
        }).trigger('change');
        const index = relatedWindows.indexOf(win);
        if (index > -1) {
            relatedWindows.splice(index, 1);
        }
        win.close();
    }

    window.showRelatedObjectLookupPopup = showRelatedObjectLookupPopup;
    window.dismissRelatedLookupPopup = dismissRelatedLookupPopup;
    window.showRelatedObjectPopup = showRelatedObjectPopup;
    window.updateRelatedObjectLinks = updateRelatedObjectLinks;
    window.dismissAddRelatedObjectPopup = dismissAddRelatedObjectPopup;
    window.dismissChangeRelatedObjectPopup = dismissChangeRelatedObjectPopup;
    window.dismissDeleteRelatedObjectPopup = dismissDeleteRelatedObjectPopup;
    window.dismissChildPopups = dismissChildPopups;

    // Kept for backward compatibility
    window.showAddAnotherPopup = showRelatedObjectPopup;
    window.dismissAddAnotherPopup = dismissAddRelatedObjectPopup;

    window.addEventListener('unload', function(evt) {
        window.dismissChildPopups();
    });

    $(document).ready(function() {
        setPopupIndex();
        $("a[data-popup-opener]").on('click', function(event) {
            event.preventDefault();
            opener.dismissRelatedLookupPopup(window, $(this).data("popup-opener"));
        });
        $('body').on('click', '.related-widget-wrapper-link[data-popup="yes"]', function(e) {
            e.preventDefault();
            if (this.href) {
                const event = $.Event('django:show-related', {href: this.href});
                $(this).trigger(event);
                if (!event.isDefaultPrevented()) {
                    showRelatedObjectPopup(this);
                }
            }
        });
        $('body').on('change', '.related-widget-wrapper select', function(e) {
            const event = $.Event('django:update-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                updateRelatedObjectLinks(this);
            }
        });
        $('.related-widget-wrapper select').trigger('change');
        $('body').on('click', '.related-lookup', function(e) {
            e.preventDefault();
            const event = $.Event('django:lookup-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                showRelatedObjectLookupPopup(this);
            }
        });
    });
}

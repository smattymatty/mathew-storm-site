var htmx=function(){"use strict";const Q={onLoad:null,process:null,on:null,off:null,trigger:null,ajax:null,find:null,findAll:null,closest:null,values:function(e,t){const n=cn(e,t||"post");return n.values},remove:null,addClass:null,removeClass:null,toggleClass:null,takeClass:null,swap:null,defineExtension:null,removeExtension:null,logAll:null,logNone:null,logger:null,config:{historyEnabled:true,historyCacheSize:10,refreshOnHistoryMiss:false,defaultSwapStyle:"innerHTML",defaultSwapDelay:0,defaultSettleDelay:20,includeIndicatorStyles:true,indicatorClass:"htmx-indicator",requestClass:"htmx-request",addedClass:"htmx-added",settlingClass:"htmx-settling",swappingClass:"htmx-swapping",allowEval:true,allowScriptTags:true,inlineScriptNonce:"",inlineStyleNonce:"",attributesToSettle:["class","style","width","height"],withCredentials:false,timeout:0,wsReconnectDelay:"full-jitter",wsBinaryType:"blob",disableSelector:"[hx-disable], [data-hx-disable]",scrollBehavior:"instant",defaultFocusScroll:false,getCacheBusterParam:false,globalViewTransitions:false,methodsThatUseUrlParams:["get","delete"],selfRequestsOnly:true,ignoreTitle:false,scrollIntoViewOnBoost:true,triggerSpecsCache:null,disableInheritance:false,responseHandling:[{code:"204",swap:false},{code:"[23]..",swap:true},{code:"[45]..",swap:false,error:true}],allowNestedOobSwaps:true},parseInterval:null,_:null,version:"2.0.4"};Q.onLoad=j;Q.process=kt;Q.on=ye;Q.off=be;Q.trigger=he;Q.ajax=Rn;Q.find=u;Q.findAll=x;Q.closest=g;Q.remove=z;Q.addClass=K;Q.removeClass=G;Q.toggleClass=W;Q.takeClass=Z;Q.swap=$e;Q.defineExtension=Fn;Q.removeExtension=Bn;Q.logAll=V;Q.logNone=_;Q.parseInterval=d;Q._=e;const n={addTriggerHandler:St,bodyContains:le,canAccessLocalStorage:B,findThisElement:Se,filterValues:hn,swap:$e,hasAttribute:s,getAttributeValue:te,getClosestAttributeValue:re,getClosestMatch:o,getExpressionVars:En,getHeaders:fn,getInputValues:cn,getInternalData:ie,getSwapSpecification:gn,getTriggerSpecs:st,getTarget:Ee,makeFragment:P,mergeObjects:ce,makeSettleInfo:xn,oobSwap:He,querySelectorExt:ae,settleImmediately:Kt,shouldCancel:ht,triggerEvent:he,triggerErrorEvent:fe,withExtensions:Ft};const r=["get","post","put","delete","patch"];const H=r.map(function(e){return"[hx-"+e+"], [data-hx-"+e+"]"}).join(", ");/**
 * Parses a time interval string and returns its value in milliseconds.
 *
 * Accepts strings with units "ms" (milliseconds), "s" (seconds), or "m" (minutes), or a plain number (interpreted as milliseconds).
 *
 * @param {string|undefined} e - The interval string to parse (e.g., "500ms", "2s", "1m", or "1000").
 * @returns {number|undefined} The interval in milliseconds, or `undefined` if parsing fails or input is `undefined`.
 */
function d(e){if(e==undefined){return undefined}let t=NaN;if(e.slice(-2)=="ms"){t=parseFloat(e.slice(0,-2))}else if(e.slice(-1)=="s"){t=parseFloat(e.slice(0,-1))*1e3}else if(e.slice(-1)=="m"){t=parseFloat(e.slice(0,-1))*1e3*60}else{t=parseFloat(e)}return isNaN(t)?undefined:t}/**
 * Retrieves the value of a specified attribute from an element.
 *
 * @param {Element} e - The element from which to retrieve the attribute.
 * @param {string} t - The name of the attribute to retrieve.
 * @returns {string|null} The value of the attribute, or {@code null} if not present or if {@link e} is not an Element.
 */
function ee(e,t){return e instanceof Element&&e.getAttribute(t)}/**
 * Determines whether an element has a specified attribute or its corresponding data attribute.
 *
 * @param {Element} e - The element to check.
 * @param {string} t - The attribute name to look for.
 * @returns {boolean} True if the element has the attribute or `data-` prefixed attribute; otherwise, false.
 */
function s(e,t){return!!e.hasAttribute&&(e.hasAttribute(t)||e.hasAttribute("data-"+t))}/**
 * Retrieves the value of an attribute or its corresponding data attribute from an element.
 *
 * Checks for the attribute {@link t} on element {@link e}; if not found, checks for `data-{@link t}`.
 *
 * @param {Element} e - The element to query.
 * @param {string} t - The attribute name to look for.
 * @returns {string|null} The value of the attribute or data attribute, or null if neither is present.
 */
function te(e,t){return ee(e,t)||ee(e,"data-"+t)}/**
 * Returns the parent element of a given node, or its shadow root host if inside a Shadow DOM.
 *
 * @param {Element} e - The element whose parent or shadow root host is to be retrieved.
 * @returns {Element|ShadowRoot|null} The parent element, the shadow root host, or null if none exists.
 */
function c(e){const t=e.parentElement;if(!t&&e.parentNode instanceof ShadowRoot)return e.parentNode;return t}/**
 * Returns the main document object.
 *
 * @returns {Document} The global document.
 */
function ne(){return document}/**
 * Returns the root node of the given element, optionally including shadow DOM ancestors.
 *
 * @param {Element} e - The element whose root node is to be retrieved.
 * @param {boolean} [t] - If true, includes shadow DOM ancestors in the composed tree.
 * @returns {Node} The root node of the element, or the document if unavailable.
 */
function m(e,t){return e.getRootNode?e.getRootNode({composed:t}):ne()}/**
 * Traverses ancestor elements of a given node until a predicate returns true.
 *
 * Starts from the provided element and moves up through its ancestors, returning the first ancestor for which the predicate function returns true. Returns null if no such ancestor is found.
 *
 * @param {Element} e - The starting element.
 * @param {function(Element): boolean} t - Predicate function to test each ancestor.
 * @returns {Element|null} The first ancestor matching the predicate, or null if none is found.
 */
function o(e,t){while(e&&!t(e)){e=c(e)}return e||null}/**
 * Resolves the effective value of an attribute for an element, considering inheritance and disinheritance rules.
 *
 * If inheritance is disabled via configuration, only explicitly inherited attributes are considered. If the attribute is marked for disinheritance, returns "unset". Otherwise, returns the attribute value from the target element.
 *
 * @param {Element} e - The source element.
 * @param {Element} t - The target element to check for the attribute.
 * @param {string} n - The attribute name to resolve.
 * @returns {string|null} The resolved attribute value, "unset" if disinherited, or null if not present.
 */
function i(e,t,n){const r=te(t,n);const o=te(t,"hx-disinherit");var i=te(t,"hx-inherit");if(e!==t){if(Q.config.disableInheritance){if(i&&(i==="*"||i.split(" ").indexOf(n)>=0)){return r}else{return null}}if(o&&(o==="*"||o.split(" ").indexOf(n)>=0)){return"unset"}}return r}/**
 * Retrieves the first non-"unset" value found by applying a lookup function to an element and its ancestors.
 *
 * Traverses up the DOM tree from the given element, applying a lookup based on a derived attribute name and an optional context. Returns the first value found that is not equal to "unset", or `undefined` if none is found.
 *
 * @param {Element} t - The starting element for the lookup.
 * @param {string} n - The attribute or context used in the lookup function.
 * @returns {*} The first found value that is not "unset", or `undefined` if none is found.
 */
function re(t,n){let r=null;o(t,function(e){return!!(r=i(t,ue(e),n))});if(r!=="unset"){return r}}/**
 * Determines if an element matches a given CSS selector.
 *
 * @param {Element} e - The element to test.
 * @param {string} t - The CSS selector to match against.
 * @returns {boolean} True if {@link e} matches {@link t}; otherwise, false.
 */
function h(e,t){const n=e instanceof Element&&(e.matches||e.matchesSelector||e.msMatchesSelector||e.mozMatchesSelector||e.webkitMatchesSelector||e.oMatchesSelector);return!!n&&n.call(e,t)}/**
 * Extracts and returns the tag name from an HTML string.
 *
 * @param {string} e - The HTML string to parse.
 * @returns {string} The lowercase tag name if found, otherwise an empty string.
 */
function T(e){const t=/<([a-z][^\/\0>\x20\t\r\n\f]*)/i;const n=t.exec(e);if(n){return n[1].toLowerCase()}else{return""}}/**
 * Parses an HTML string into a Document object.
 *
 * @param {string} e - The HTML string to parse.
 * @returns {Document} A Document representing the parsed HTML.
 */
function q(e){const t=new DOMParser;return t.parseFromString(e,"text/html")}/**
 * Moves all child nodes from one element to another.
 *
 * Transfers all child nodes from {@link t} to {@link e}, preserving their order.
 */
function L(e,t){while(t.childNodes.length>0){e.append(t.childNodes[0])}}/**
 * Clones a script element, copying all attributes and content, and sets execution properties for safe insertion into the DOM.
 *
 * If a nonce is configured in {@link Q.config.inlineScriptNonce}, it is applied to the cloned script for CSP compliance.
 *
 * @param {Element} e - The script element to clone.
 * @returns {HTMLScriptElement} A new script element with the same attributes and content as {@link e}, ready for execution.
 */
function A(e){const t=ne().createElement("script");se(e.attributes,function(e){t.setAttribute(e.name,e.value)});t.textContent=e.textContent;t.async=false;if(Q.config.inlineScriptNonce){t.nonce=Q.config.inlineScriptNonce}return t}/**
 * Determines if the given element is a script tag with a supported type.
 *
 * @param {Element} e - The element to check.
 * @returns {boolean} True if {@link e} is a `<script>` element with type "text/javascript", "module", or an empty type.
 */
function N(e){return e.matches("script")&&(e.type==="text/javascript"||e.type==="module"||e.type==="")}/**
 * Replaces all executable script elements within the given element with cloned, executable copies.
 *
 * This ensures that scripts within dynamically inserted HTML fragments are executed as intended.
 *
 * @param {Element} e - The root element containing script tags to process.
 */
function I(e){Array.from(e.querySelectorAll("script")).forEach(e=>{if(N(e)){const t=A(e);const n=e.parentNode;try{n.insertBefore(t,e)}catch(e){O(e)}finally{e.remove()}}})}/**
 * Converts an HTML string into a DocumentFragment, preserving the document title and handling script tags according to configuration.
 *
 * If the HTML string contains a `<head>` section, it is removed. The function extracts the title from the HTML and assigns it to the fragment. Script tags are either executed or removed based on the `allowScriptTags` configuration.
 *
 * @param {string} e - The HTML string to parse.
 * @returns {DocumentFragment} A fragment containing the parsed HTML content, with the `title` property set if a title is present.
 */
function P(e){const t=e.replace(/<head(\s[^>]*)?>[\s\S]*?<\/head>/i,"");const n=T(t);let r;if(n==="html"){r=new DocumentFragment;const i=q(e);L(r,i.body);r.title=i.title}else if(n==="body"){r=new DocumentFragment;const i=q(t);L(r,i.body);r.title=i.title}else{const i=q('<body><template class="internal-htmx-wrapper">'+t+"</template></body>");r=i.querySelector("template").content;r.title=i.title;var o=r.querySelector("title");if(o&&o.parentNode===r){o.remove();r.title=o.innerText}}if(r){if(Q.config.allowScriptTags){I(r)}else{r.querySelectorAll("script").forEach(e=>e.remove())}}return r}/**
 * Invokes the provided function if it is defined.
 *
 * @param {Function} e - The function to invoke, if present.
 */
function oe(e){if(e){e()}}/**
 * Checks if a value is of a specified object type.
 *
 * @param {*} e - The value to check.
 * @param {string} t - The expected object type name (e.g., "Array", "Function").
 * @returns {boolean} True if the value is of the specified type; otherwise, false.
 */
function t(e,t){return Object.prototype.toString.call(e)==="[object "+t+"]"}/**
 * Determines whether the provided value is a function.
 *
 * @param {*} e - The value to check.
 * @returns {boolean} True if {@link e} is a function; otherwise, false.
 */
function k(e){return typeof e==="function"}/**
 * Determines if the provided value is an object.
 *
 * @param {*} e - The value to check.
 * @returns {boolean} True if {@link e} is an object; otherwise, false.
 */
function D(e){return t(e,"Object")}/**
 * Retrieves or initializes the internal data storage object for a given element.
 *
 * @param {Element} e - The element for which to access internal data.
 * @returns {Object} The internal data object associated with the element.
 */
function ie(e){const t="htmx-internal-data";let n=e[t];if(!n){n=e[t]={}}return n}/**
 * Converts an array-like object to a true array.
 *
 * @param {ArrayLike<any>} t - The array-like object to convert.
 * @returns {Array<any>} A new array containing the elements of {@link t}.
 */
function M(t){const n=[];if(t){for(let e=0;e<t.length;e++){n.push(t[e])}}return n}/**
 * Iterates over an array-like object and applies a callback to each element.
 *
 * @param {Array|NodeList} t - The array or array-like object to iterate over.
 * @param {Function} n - The callback function to execute for each element.
 */
function se(t,n){if(t){for(let e=0;e<t.length;e++){n(t[e])}}}/**
 * Determines if an element is visible within the viewport.
 *
 * @param {Element} e - The element to check.
 * @returns {boolean} True if any part of the element is within the vertical bounds of the viewport; otherwise, false.
 */
function X(e){const t=e.getBoundingClientRect();const n=t.top;const r=t.bottom;return n<window.innerHeight&&r>=0}/**
 * Determines if the given element is part of the main document, including through Shadow DOM.
 *
 * @param {Element} e - The element to check.
 * @returns {boolean} True if {@link e} is in the main document; otherwise, false.
 */
function le(e){return e.getRootNode({composed:true})===document}/**
 * Splits a string into an array of non-empty, trimmed tokens separated by whitespace.
 *
 * @param {string} e - The input string to tokenize.
 * @returns {string[]} An array of whitespace-separated tokens from the input string.
 */
function F(e){return e.trim().split(/\s+/)}/**
 * Copies all own enumerable properties from the source object to the target object.
 *
 * @param {Object} e - The target object to receive properties.
 * @param {Object} t - The source object whose properties are copied.
 * @returns {Object} The updated target object {@link e}.
 */
function ce(e,t){for(const n in t){if(t.hasOwnProperty(n)){e[n]=t[n]}}return e}/**
 * Safely parses a JSON string and returns the resulting object, or null if parsing fails.
 *
 * @param {string} e - The JSON string to parse.
 * @returns {any|null} The parsed object, or null if parsing fails.
 *
 * @remark If parsing fails, the error is logged and null is returned.
 */
function S(e){try{return JSON.parse(e)}catch(e){O(e);return null}}/**
 * Checks if localStorage is available and writable.
 *
 * @returns {boolean} True if localStorage can be used, false otherwise.
 */
function B(){const e="htmx:localStorageTest";try{localStorage.setItem(e,e);localStorage.removeItem(e);return true}catch(e){return false}}/**
 * Normalizes a URL string to its pathname and search components, removing trailing slashes except for the root path.
 *
 * If the input is not a valid URL, returns the original string unchanged.
 *
 * @param {string} t - The URL string to normalize.
 * @returns {string} The normalized URL path.
 */
function U(t){try{const e=new URL(t);if(e){t=e.pathname+e.search}if(!/^\/$/.test(t)){t=t.replace(/\/+$/,"")}return t}catch(e){return t}}/**
 * Evaluates a JavaScript expression in the context of the document body.
 *
 * @param {string} e - The JavaScript code to evaluate.
 * @returns {*} The result of the evaluated expression.
 *
 * @remark The code is executed using `eval` with the document body as context, which may have security implications if the input is not trusted.
 */
function e(e){return vn(ne().body,function(){return eval(e)})}/**
 * Registers a callback to be invoked whenever an element is loaded by htmx.
 *
 * The callback receives the loaded element as its argument.
 *
 * @param {function} t - Callback function to execute with the loaded element.
 * @returns {function} A function to remove the event listener.
 */
function j(t){const e=Q.on("htmx:load",function(e){t(e.detail.elt)});return e}/**
 * Enables verbose logging by setting the logger to output messages to the console.
 *
 * @remark After calling this function, htmx will log debug information to the browser console.
 */
function V(){Q.logger=function(e,t,n){if(console){console.log(t,e,n)}}}/**
 * Disables logging by removing the current logger.
 */
function _(){Q.logger=null}/**
 * Returns the first descendant element matching the selector {@link t} within the context {@link e}.
 *
 * If {@link e} is a string, it is treated as a selector and the search is performed within the main document.
 *
 * @param {Element|string} e - The context element or a selector string.
 * @param {string} t - The CSS selector to match.
 * @returns {Element|null} The first matching element, or null if none is found.
 */
function u(e,t){if(typeof e!=="string"){return e.querySelector(t)}else{return u(ne(),e)}}/**
 * Returns all elements matching a selector within a given context.
 *
 * If {@link e} is a string, it is treated as a selector and the search is performed within the main document. If {@link e} is an element, the search is performed within that element.
 *
 * @param {Element|string} e - The context element or a selector string.
 * @param {string} t - The selector to match.
 * @returns {NodeListOf<Element>} A list of matching elements.
 */
function x(e,t){if(typeof e!=="string"){return e.querySelectorAll(t)}else{return x(ne(),e)}}/**
 * Returns the global window object.
 *
 * @returns {Window} The global window object.
 */
function E(){return window}/**
 * Removes an element from the DOM, optionally after a specified delay.
 *
 * @param {Element|string} e - The element to remove, or a selector string to find the element.
 * @param {number} [t] - Optional delay in milliseconds before removal.
 */
function z(e,t){e=y(e);if(t){E().setTimeout(function(){z(e);e=null},t)}else{c(e).removeChild(e)}}/**
 * Returns the given value if it is a DOM Element, otherwise returns null.
 *
 * @param {*} e - The value to check.
 * @returns {Element|null} The input if it is an Element, or null otherwise.
 */
function ue(e){return e instanceof Element?e:null}/**
 * Returns the element if it is an HTMLElement, otherwise returns null.
 *
 * @param {*} e - The value to check.
 * @returns {HTMLElement|null} The HTMLElement if {@link e} is an HTMLElement, or null otherwise.
 */
function $(e){return e instanceof HTMLElement?e:null}/**
 * Returns the input if it is a string; otherwise returns null.
 *
 * @param {*} e - The value to check.
 * @returns {?string} The string value if {@link e} is a string, or null otherwise.
 */
function J(e){return typeof e==="string"?e:null}/**
 * Returns the input if it is a DOM Element, Document, or DocumentFragment; otherwise returns null.
 *
 * @param {*} e - The value to check.
 * @returns {Element|Document|DocumentFragment|null} The input if it is a DOM node, or null otherwise.
 */
function f(e){return e instanceof Element||e instanceof Document||e instanceof DocumentFragment?e:null}/**
 * Adds a CSS class to an element, optionally after a specified delay.
 *
 * @param {Element|string} e - The target element or a selector string.
 * @param {string} t - The CSS class to add.
 * @param {number} [n] - Optional delay in milliseconds before adding the class.
 */
function K(e,t,n){e=ue(y(e));if(!e){return}if(n){E().setTimeout(function(){K(e,t);e=null},n)}else{e.classList&&e.classList.add(t)}}/**
 * Removes a CSS class from an element, optionally after a delay.
 *
 * If the element has no remaining classes after removal, the `class` attribute is also removed.
 *
 * @param {Element|string} e - The target element or a selector string.
 * @param {string} t - The CSS class to remove.
 * @param {number} [n] - Optional delay in milliseconds before removing the class.
 */
function G(e,t,n){let r=ue(y(e));if(!r){return}if(n){E().setTimeout(function(){G(r,t);r=null},n)}else{if(r.classList){r.classList.remove(t);if(r.classList.length===0){r.removeAttribute("class")}}}}/**
 * Toggles a CSS class on the specified element.
 *
 * @param {Element|string} e - The target element or a selector string.
 * @param {string} t - The CSS class to toggle.
 */
function W(e,t){e=y(e);e.classList.toggle(t)}/**
 * Applies a CSS class to an element and removes it from its siblings.
 *
 * @param {Element|string} e - The target element or a selector string.
 * @param {string} t - The CSS class to apply exclusively to the target element.
 */
function Z(e,t){e=y(e);se(e.parentElement.children,function(e){G(e,t)});K(ue(e),t)}/**
 * Returns the closest ancestor of the given element that matches the specified selector or predicate.
 *
 * If the element supports the `closest` method, it is used to find the ancestor matching {@link t}. Otherwise, traverses up the DOM tree, returning the first ancestor for which the predicate {@link h} returns true.
 *
 * @param {Element|string} e - The starting element or a selector to resolve to an element.
 * @param {string} t - A CSS selector or predicate to match ancestors against.
 * @returns {Element|null} The closest matching ancestor element, or {@code null} if none is found.
 */
function g(e,t){e=ue(y(e));if(e&&e.closest){return e.closest(t)}else{do{if(e==null||h(e,t)){return e}}while(e=e&&ue(c(e)));return null}}/**
 * Determines whether a string starts with a specified substring.
 *
 * @param {string} e - The string to check.
 * @param {string} t - The substring to look for at the start of {@link e}.
 * @returns {boolean} True if {@link e} begins with {@link t}; otherwise, false.
 */
function l(e,t){return e.substring(0,t.length)===t}/**
 * Determines whether a string ends with the specified substring.
 *
 * @param {string} e - The string to check.
 * @param {string} t - The substring to look for at the end of {@link e}.
 * @returns {boolean} True if {@link e} ends with {@link t}; otherwise, false.
 */
function Y(e,t){return e.substring(e.length-t.length)===t}/**
 * Extracts the tag name from an HTML string if it is a self-closing tag; otherwise, returns the trimmed string.
 *
 * If the input string starts with '<' and ends with '/>', the function returns the substring between these markers, representing the tag name. For all other cases, it returns the trimmed input string unchanged.
 *
 * @param {string} e - The HTML string or tag name to process.
 * @returns {string} The extracted tag name or the original trimmed string.
 */
function ge(e){const t=e.trim();if(l(t,"<")&&Y(t,"/>")){return t.substring(1,t.length-2)}else{return t}}/**
 * Resolves a selector path relative to a given element, supporting advanced keywords and combinators.
 *
 * Supports keywords such as `global`, `closest`, `find`, `next`, `previous`, `document`, `window`, `body`, `root`, and `host`, as well as standard CSS selectors. Returns an array of matching elements or objects.
 *
 * @param {Element|string} t - The reference element or a selector string to resolve from.
 * @param {string} r - The selector path, which may include keywords and combinators.
 * @param {boolean} [n] - If true, enables global or shadow DOM traversal for certain keywords.
 * @returns {Array} An array of resolved elements or objects matching the selector path.
 */
function p(t,r,n){if(r.indexOf("global ")===0){return p(t,r.slice(7),true)}t=y(t);const o=[];{let t=0;let n=0;for(let e=0;e<r.length;e++){const l=r[e];if(l===","&&t===0){o.push(r.substring(n,e));n=e+1;continue}if(l==="<"){t++}else if(l==="/"&&e<r.length-1&&r[e+1]===">"){t--}}if(n<r.length){o.push(r.substring(n))}}const i=[];const s=[];while(o.length>0){const r=ge(o.shift());let e;if(r.indexOf("closest ")===0){e=g(ue(t),ge(r.substr(8)))}else if(r.indexOf("find ")===0){e=u(f(t),ge(r.substr(5)))}else if(r==="next"||r==="nextElementSibling"){e=ue(t).nextElementSibling}else if(r.indexOf("next ")===0){e=pe(t,ge(r.substr(5)),!!n)}else if(r==="previous"||r==="previousElementSibling"){e=ue(t).previousElementSibling}else if(r.indexOf("previous ")===0){e=me(t,ge(r.substr(9)),!!n)}else if(r==="document"){e=document}else if(r==="window"){e=window}else if(r==="body"){e=document.body}else if(r==="root"){e=m(t,!!n)}else if(r==="host"){e=t.getRootNode().host}else{s.push(r)}if(e){i.push(e)}}if(s.length>0){const e=s.join(",");const c=f(m(t,!!n));i.push(...M(c.querySelectorAll(e)))}return i}var pe=function(t,e,n){const r=f(m(t,n)).querySelectorAll(e);for(let e=0;e<r.length;e++){const o=r[e];if(o.compareDocumentPosition(t)===Node.DOCUMENT_POSITION_PRECEDING){return o}}};var me=function(t,e,n){const r=f(m(t,n)).querySelectorAll(e);for(let e=r.length-1;e>=0;e--){const o=r[e];if(o.compareDocumentPosition(t)===Node.DOCUMENT_POSITION_FOLLOWING){return o}}};/**
 * Finds the first matching element based on a selector or returns the element itself.
 *
 * If {@link e} is a string, queries the document body for the first element matching the selector.
 * If {@link e} is an element, returns it or the first matching descendant based on {@link t}.
 *
 * @param {string|Element} e - A CSS selector string or a DOM element.
 * @param {string} [t] - An optional selector to query within the element if {@link e} is not a string.
 * @returns {Element|undefined} The first matching element, or undefined if none is found.
 */
function ae(e,t){if(typeof e!=="string"){return p(e,t)[0]}else{return p(ne().body,e)[0]}}/**
 * Resolves an input to a DOM element.
 *
 * If {@link e} is a string, queries for the element within the context of {@link t} or the document. If {@link e} is already an element, returns it unchanged.
 *
 * @param {string|Element} e - Selector string or DOM element.
 * @param {Element} [t] - Optional context element for the query.
 * @returns {Element|null} The resolved DOM element, or null if not found.
 */
function y(e,t){if(typeof e==="string"){return u(f(t)||document,e)}else{return e}}/**
 * Normalizes event listener arguments into a consistent object structure.
 *
 * Accepts either a function as the second argument (for global listeners) or an event name, returning an object with standardized properties for event handling.
 *
 * @param {Element|string|Function} e - The target element or event name, depending on usage.
 * @param {string|Function} t - The event name or listener function.
 * @param {Function|Object} [n] - The event listener function or options.
 * @param {Object} [r] - Additional options for the event listener.
 * @returns {{target: Element, event: string, listener: Function, options: Object|undefined}} An object describing the event listener configuration.
 */
function xe(e,t,n,r){if(k(t)){return{target:ne().body,event:J(e),listener:t,options:n}}else{return{target:y(e),event:J(t),listener:n,options:r}}}/**
 * Adds an event listener to a target element, supporting delegation and custom options.
 *
 * @param {Element|Document|Window} t - The target to attach the event listener to.
 * @param {string} n - The event type to listen for.
 * @param {Function} r - The event handler function.
 * @param {Object} [o] - Optional event listener options.
 * @returns {Function} The event handler function if the event type is not delegated; otherwise, returns the delegation selector.
 */
function ye(t,n,r,o){Vn(function(){const e=xe(t,n,r,o);e.target.addEventListener(e.event,e.listener,e.options)});const e=k(n);return e?n:r}/**
 * Removes an event listener from a target element.
 *
 * @param {Element|Document|Window} t - The target from which to remove the event listener.
 * @param {string|function} n - The event type or the listener function, depending on usage.
 * @param {function} [r] - The event listener function to remove.
 * @returns {string|function} Returns the event type if {@link n} is a string, or the listener function if {@link n} is a function.
 */
function be(t,n,r){Vn(function(){const e=xe(t,n,r);e.target.removeEventListener(e.event,e.listener)});return k(n)?n:r}const ve=ne().createElement("output");/**
 * Resolves a target selector for a given element and attribute, returning the matching elements.
 *
 * If the selector is "this", returns the element itself. If the selector yields no matches, logs an error and returns a placeholder element.
 *
 * @param {Element} e - The source element.
 * @param {string} t - The attribute name containing the selector.
 * @returns {Element[]} An array of matched elements, or a placeholder if no matches are found.
 */
function we(e,t){const n=re(e,t);if(n){if(n==="this"){return[Se(e,t)]}else{const r=p(e,n);if(r.length===0){O('The selector "'+n+'" on '+t+" returned no matches!");return[ve]}else{return r}}}}/**
 * Returns the first ancestor of the given element that has the specified attribute, searching up the DOM tree.
 *
 * @param {Element} e - The starting element.
 * @param {string} t - The attribute name to search for.
 * @returns {Element|null} The closest ancestor element with the specified attribute, or {@code null} if none is found.
 */
function Se(e,t){return ue(o(e,function(e){return te(ue(e),t)!=null}))}/**
 * Determines the target element for content swapping based on the `hx-target` attribute or boost context.
 *
 * If the `hx-target` attribute is set to "this", returns the element itself. If `hx-target` specifies a selector, returns the first matching descendant. If no `hx-target` is present and the element is boosted, returns the document body; otherwise, returns the element itself.
 *
 * @param {Element} e - The source element to evaluate.
 * @returns {Element} The resolved target element for swapping.
 */
function Ee(e){const t=re(e,"hx-target");if(t){if(t==="this"){return Se(e,"hx-target")}else{return ae(e,t)}}else{const n=ie(e);if(n.boosted){return ne().body}else{return e}}}/**
 * Determines whether a given attribute name is included in the configured list of attributes to settle after a swap.
 *
 * @param {string} t - The attribute name to check.
 * @returns {boolean} True if the attribute should be settled, otherwise false.
 */
function Ce(t){const n=Q.config.attributesToSettle;for(let e=0;e<n.length;e++){if(t===n[e]){return true}}return false}/**
 * Synchronizes the attributes of an element with another element, copying only allowed attributes.
 *
 * Removes any allowed attribute from {@link t} that does not exist on {@link n}, and sets all allowed attributes from {@link n} onto {@link t}.
 *
 * @param {Element} t - The target element whose attributes will be updated.
 * @param {Element} n - The source element to copy attributes from.
 */
function Oe(t,n){se(t.attributes,function(e){if(!n.hasAttribute(e.name)&&Ce(e.name)){t.removeAttribute(e.name)}});se(n.attributes,function(e){if(Ce(e.name)){t.setAttribute(e.name,e.value)}})}/**
 * Determines if a swap style should be treated as an inline swap.
 *
 * Checks registered extensions for custom inline swap handling. If none apply, returns true if the swap style is "outerHTML".
 *
 * @param {string} t - The swap style to evaluate.
 * @param {Element} e - The target element for the swap.
 * @returns {boolean} True if the swap should be considered inline; otherwise, false.
 */
function Re(t,e){const n=Un(e);for(let e=0;e<n.length;e++){const r=n[e];try{if(r.isInlineSwap(t)){return true}}catch(e){O(e)}}return t==="outerHTML"}/**
 * Performs an out-of-band (OOB) DOM swap using the provided element and swap specification.
 *
 * Locates the target element in the current document by ID or selector, then swaps its content or structure according to the specified swap style (e.g., `outerHTML`, `innerHTML`). Triggers lifecycle events before and after the swap. If the target is not found, removes the OOB element and triggers an error event.
 *
 * @param {string} e - Swap style or swap style with selector (e.g., "outerHTML:#targetId").
 * @param {Element} o - The element containing the OOB content to swap into the document.
 * @param {Object} i - Swap context, typically containing elements involved in the swap.
 * @param {Document} [t] - Optional document context; defaults to the main document.
 * @returns {string} The swap style or specification used.
 */
function He(e,o,i,t){t=t||ne();let n="#"+ee(o,"id");let s="outerHTML";if(e==="true"){}else if(e.indexOf(":")>0){s=e.substring(0,e.indexOf(":"));n=e.substring(e.indexOf(":")+1)}else{s=e}o.removeAttribute("hx-swap-oob");o.removeAttribute("data-hx-swap-oob");const r=p(t,n,false);if(r){se(r,function(e){let t;const n=o.cloneNode(true);t=ne().createDocumentFragment();t.appendChild(n);if(!Re(s,e)){t=f(n)}const r={shouldSwap:true,target:e,fragment:t};if(!he(e,"htmx:oobBeforeSwap",r))return;e=r.target;if(r.shouldSwap){qe(t);_e(s,e,e,t,i);Te()}se(i.elts,function(e){he(e,"htmx:oobAfterSwap",r)})});o.parentNode.removeChild(o)}else{o.parentNode.removeChild(o);fe(ne().body,"htmx:oobErrorNoTarget",{content:o})}return e}/**
 * Restores elements previously preserved in the DOM by moving them back to their original locations.
 *
 * This function locates the special container with the ID `--htmx-preserve-pantry--`, moves each of its child elements back to their corresponding original positions in the document (identified by matching IDs), and then removes the pantry container.
 */
function Te(){const e=u("#--htmx-preserve-pantry--");if(e){for(const t of[...e.children]){const n=u("#"+t.id);n.parentNode.moveBefore(t,n);n.remove()}e.remove()}}/**
 * Restores elements marked with `hx-preserve` or `data-hx-preserve` by replacing or moving them back into the DOM.
 *
 * Elements with a matching `id` are either moved before a placeholder or replaced in their original location, preserving their state across DOM updates.
 */
function qe(e){se(x(e,"[hx-preserve], [data-hx-preserve]"),function(e){const t=te(e,"id");const n=ne().getElementById(t);if(n!=null){if(e.moveBefore){let e=u("#--htmx-preserve-pantry--");if(e==null){ne().body.insertAdjacentHTML("afterend","<div id='--htmx-preserve-pantry--'></div>");e=u("#--htmx-preserve-pantry--")}e.moveBefore(n,null)}else{e.parentNode.replaceChild(n,e)}}})}/**
 * Preserves elements with IDs from a source fragment by replacing matching elements in the target DOM, enabling restoration after DOM updates.
 *
 * @param {Element} l - The root element of the target DOM where preservation is managed.
 * @param {Element} e - The source fragment containing elements to preserve.
 * @param {Object} c - An object with a `tasks` array to which restoration tasks are added.
 */
function Le(l,e,c){se(e.querySelectorAll("[id]"),function(t){const n=ee(t,"id");if(n&&n.length>0){const r=n.replace("'","\\'");const o=t.tagName.replace(":","\\:");const e=f(l);const i=e&&e.querySelector(o+"[id='"+r+"']");if(i&&i!==e){const s=t.cloneNode();Oe(t,i);c.tasks.push(function(){Oe(t,s)})}}})}/**
 * Finalizes the processing of a newly added element by removing the added class, initializing htmx processing, focusing elements, and triggering the `htmx:load` event.
 *
 * @param {Element} e - The element that has been added to the DOM and requires initialization.
 */
function Ae(e){return function(){G(e,Q.config.addedClass);kt(ue(e));Ne(f(e));he(e,"htmx:load")}}/**
 * Focuses the first descendant element with the `autofocus` attribute, or the element itself if it has `autofocus`.
 *
 * If the target element or one of its descendants has the `autofocus` attribute, that element receives focus.
 */
function Ne(e){const t="[autofocus]";const n=$(h(e,t)?e:e.querySelector(t));if(n!=null){n.focus()}}/**
 * Inserts all child nodes from a source element into a target element before a reference node.
 *
 * Each inserted node is marked with the configured "added" class, and non-text/comment nodes are scheduled for further processing.
 *
 * @param {Element} e - The target element where nodes will be inserted.
 * @param {Node|null} t - The reference node before which new nodes are inserted. If null, nodes are appended.
 * @param {Element} n - The source element whose child nodes are moved.
 * @param {Object} r - An object containing a `tasks` array to which processing tasks for inserted nodes are added.
 */
function a(e,t,n,r){Le(e,n,r);while(n.childNodes.length>0){const o=n.firstChild;K(ue(o),Q.config.addedClass);e.insertBefore(o,t);if(o.nodeType!==Node.TEXT_NODE&&o.nodeType!==Node.COMMENT_NODE){r.tasks.push(Ae(o))}}}/**
 * Computes a 32-bit integer hash code for a given string.
 *
 * @param {string} e - The input string to hash.
 * @param {number} t - The initial hash value.
 * @returns {number} The resulting 32-bit integer hash.
 */
function Ie(e,t){let n=0;while(n<e.length){t=(t<<5)-t+e.charCodeAt(n++)|0}return t}/**
 * Computes a hash code for an element based on its attribute names and values.
 *
 * @param {Element} t - The element whose attributes are hashed.
 * @returns {number} A numeric hash representing the element's attributes.
 */
function Pe(t){let n=0;if(t.attributes){for(let e=0;e<t.attributes.length;e++){const r=t.attributes[e];if(r.value){n=Ie(r.name,n);n=Ie(r.value,n)}}}return n}/**
 * Removes all event listeners registered via `hx-on` attributes from the given element.
 *
 * @param {Element} t - The element from which to remove `hx-on` event listeners.
 */
function ke(t){const n=ie(t);if(n.onHandlers){for(let e=0;e<n.onHandlers.length;e++){const r=n.onHandlers[e];be(t,r.event,r.listener)}delete n.onHandlers}}/**
 * Cleans up event listeners, timeouts, and internal state associated with a given element.
 *
 * Removes any active timeouts, detaches registered event listeners, and resets internal tracking properties for the element except for the `firstInitCompleted` flag.
 *
 * @param {Element} e - The element to clean up.
 */
function De(e){const t=ie(e);if(t.timeout){clearTimeout(t.timeout)}if(t.listenerInfos){se(t.listenerInfos,function(e){if(e.on){be(e.on,e.trigger,e.listener)}})}ke(e);se(Object.keys(t),function(e){if(e!=="firstInitCompleted")delete t[e]})}/**
 * Recursively cleans up an element and its descendants before removal.
 *
 * Dispatches the `htmx:beforeCleanupElement` event on the element, performs cleanup, and applies the same process to all child elements.
 */
function b(e){he(e,"htmx:beforeCleanupElement");De(e);if(e.children){se(e.children,function(e){b(e)})}}/**
 * Removes an element from the DOM and updates the provided context with its siblings.
 *
 * If the element is the `<body>`, delegates to a specialized handler. Otherwise, removes the element, updates the context's element list to exclude it, and adds its siblings to the context.
 *
 * @param {Node} t - The element or node to remove.
 * @param {Element} e - The parent element or context for removal.
 * @param {Object} n - The context object containing an `elts` array to update.
 */
function Me(t,e,n){if(t instanceof Element&&t.tagName==="BODY"){return Ve(t,e,n)}let r;const o=t.previousSibling;const i=c(t);if(!i){return}a(i,t,e,n);if(o==null){r=i.firstChild}else{r=o.nextSibling}n.elts=n.elts.filter(function(e){return e!==t});while(r&&r!==t){if(r instanceof Element){n.elts.push(r)}r=r.nextSibling}b(t);if(t instanceof Element){t.remove()}else{t.parentNode.removeChild(t)}}/**
 * Inserts a node or fragment {@link t} before the first child of element {@link e}, optionally applying a filter function {@link n}.
 *
 * @returns {Node} The inserted node or fragment.
 */
function Xe(e,t,n){return a(e,e.firstChild,t,n)}/**
 * Traverses the ancestors of a given element, applying a predicate function to each ancestor.
 *
 * @param {Element} e - The starting element.
 * @param {Function} t - Predicate function applied to each ancestor; traversal stops if it returns a truthy value.
 * @param {*} [n] - Optional value passed to the predicate function.
 * @returns {*} The first truthy value returned by the predicate, or undefined if none is found.
 */
function Fe(e,t,n){return a(c(e),e,t,n)}/**
 * Finds the closest ancestor of a given element that matches a selector.
 *
 * @param {Element} e - The starting element.
 * @param {string} t - The CSS selector to match.
 * @param {Element} [n] - An optional boundary element; search stops at this ancestor.
 * @returns {Element|null} The closest matching ancestor element, or null if none is found.
 */
function Be(e,t,n){return a(e,null,t,n)}/**
 * Inserts a node or fragment before the next sibling of a given element.
 *
 * @param {Node} e - The reference element whose next sibling is the insertion point.
 * @param {Node|DocumentFragment} t - The node or fragment to insert.
 * @param {boolean} [n] - Optional flag passed to the underlying insertion logic.
 * @returns {Node|DocumentFragment} The inserted node or fragment.
 */
function Ue(e,t,n){return a(c(e),e.nextSibling,t,n)}/**
 * Removes the specified element from its parent node.
 *
 * @param {Element} e - The element to remove from the DOM.
 * @returns {Element|undefined} The removed element, or undefined if it had no parent.
 */
function je(e){b(e);const t=c(e);if(t){return t.removeChild(e)}}/**
 * Removes all child nodes from the given element, invoking a callback for each node before removal.
 *
 * @param {Element} e - The parent element whose children will be removed.
 * @param {Function} t - Callback invoked for each child node before removal.
 * @param {*} n - Additional data passed to the callback.
 */
function Ve(e,t,n){const r=e.firstChild;a(e,r,t,n);if(r){while(r.nextSibling){b(r.nextSibling);e.removeChild(r.nextSibling)}b(r);e.removeChild(r)}}/**
 * Performs a DOM swap operation on the target element using the specified swap style.
 *
 * Depending on the swap style, this function updates, inserts, or removes elements in the DOM. If a custom extension provides a `handleSwap` method for the given style, it will be used. If the style is unrecognized, the default swap style from the configuration is applied.
 *
 * @param {string} t - The swap style (e.g., "outerHTML", "innerHTML", "beforebegin", "afterend", "delete", or custom).
 * @param {Element} e - The source element for extension lookup.
 * @param {Element} n - The target element to be swapped or updated.
 * @param {DocumentFragment|string} r - The content to insert or use for the swap.
 * @param {Object} o - Swap context, including tasks to be performed after the swap.
 */
function _e(t,e,n,r,o){switch(t){case"none":return;case"outerHTML":Me(n,r,o);return;case"afterbegin":Xe(n,r,o);return;case"beforebegin":Fe(n,r,o);return;case"beforeend":Be(n,r,o);return;case"afterend":Ue(n,r,o);return;case"delete":je(n);return;default:var i=Un(e);for(let e=0;e<i.length;e++){const s=i[e];try{const l=s.handleSwap(t,n,r,o);if(l){if(Array.isArray(l)){for(let e=0;e<l.length;e++){const c=l[e];if(c.nodeType!==Node.TEXT_NODE&&c.nodeType!==Node.COMMENT_NODE){o.tasks.push(Ae(c))}}}return}}catch(e){O(e)}}if(t==="innerHTML"){Ve(n,r,o)}else{_e(Q.config.defaultSwapStyle,e,n,r,o)}}}/**
 * Processes and applies out-of-band (OOB) swaps for elements within a given context.
 *
 * Scans the provided element for descendants marked with `hx-swap-oob` or `data-hx-swap-oob` attributes and performs OOB swaps using the specified swap logic. If nested OOB swaps are not allowed and the element is not at the top level, the OOB attributes are removed.
 *
 * @param {Element} e - The root element to search for OOB swap targets.
 * @param {Element} n - The source element for the swap operation.
 * @param {Object} r - Additional swap options or context.
 * @returns {boolean} True if any OOB swaps were processed; otherwise, false.
 */
function ze(e,n,r){var t=x(e,"[hx-swap-oob], [data-hx-swap-oob]");se(t,function(e){if(Q.config.allowNestedOobSwaps||e.parentElement===null){const t=te(e,"hx-swap-oob");if(t!=null){He(t,e,n,r)}}else{e.removeAttribute("hx-swap-oob");e.removeAttribute("data-hx-swap-oob")}});return t.length>0}/**
 * Performs a DOM swap on the target element using the provided HTML, handling out-of-band swaps, focus restoration, and lifecycle events.
 *
 * Processes the HTML fragment, applies the specified swap style, manages out-of-band updates, preserves elements as needed, and triggers relevant htmx lifecycle events. Restores focus and selection to the previously active element if possible, updates the document title unless instructed otherwise, and manages scroll and anchor behavior after the swap.
 *
 * @param {Element|string} e - The target element or selector to be swapped.
 * @param {string} t - The HTML string to insert.
 * @param {Object} r - Swap options, including swapStyle, focusScroll, ignoreTitle, settleDelay, and others.
 * @param {Object} [o] - Additional options such as contextElement, selectOOB, select, anchor, eventInfo, afterSwapCallback, and afterSettleCallback.
 */
function $e(e,t,r,o){if(!o){o={}}e=y(e);const i=o.contextElement?m(o.contextElement,false):ne();const n=document.activeElement;let s={};try{s={elt:n,start:n?n.selectionStart:null,end:n?n.selectionEnd:null}}catch(e){}const l=xn(e);if(r.swapStyle==="textContent"){e.textContent=t}else{let n=P(t);l.title=n.title;if(o.selectOOB){const u=o.selectOOB.split(",");for(let t=0;t<u.length;t++){const a=u[t].split(":",2);let e=a[0].trim();if(e.indexOf("#")===0){e=e.substring(1)}const f=a[1]||"true";const h=n.querySelector("#"+e);if(h){He(f,h,l,i)}}}ze(n,l,i);se(x(n,"template"),function(e){if(e.content&&ze(e.content,l,i)){e.remove()}});if(o.select){const d=ne().createDocumentFragment();se(n.querySelectorAll(o.select),function(e){d.appendChild(e)});n=d}qe(n);_e(r.swapStyle,o.contextElement,e,n,l);Te()}if(s.elt&&!le(s.elt)&&ee(s.elt,"id")){const g=document.getElementById(ee(s.elt,"id"));const p={preventScroll:r.focusScroll!==undefined?!r.focusScroll:!Q.config.defaultFocusScroll};if(g){if(s.start&&g.setSelectionRange){try{g.setSelectionRange(s.start,s.end)}catch(e){}}g.focus(p)}}e.classList.remove(Q.config.swappingClass);se(l.elts,function(e){if(e.classList){e.classList.add(Q.config.settlingClass)}he(e,"htmx:afterSwap",o.eventInfo)});if(o.afterSwapCallback){o.afterSwapCallback()}if(!r.ignoreTitle){kn(l.title)}const c=function(){se(l.tasks,function(e){e.call()});se(l.elts,function(e){if(e.classList){e.classList.remove(Q.config.settlingClass)}he(e,"htmx:afterSettle",o.eventInfo)});if(o.anchor){const e=ue(y("#"+o.anchor));if(e){e.scrollIntoView({block:"start",behavior:"auto"})}}yn(l.elts,r);if(o.afterSettleCallback){o.afterSettleCallback()}};if(r.settleDelay>0){E().setTimeout(c,r.settleDelay)}else{c()}}/**
 * Dispatches custom events on a target element based on values in a response header.
 *
 * If the response header value is a JSON object, each key is used as an event name and its value as event detail. If the value is a string, it is split by commas and each part is dispatched as an event with an empty array as detail.
 *
 * @param {XMLHttpRequest} e - The XMLHttpRequest instance.
 * @param {string} t - The name of the response header to process.
 * @param {Element} n - The target element for event dispatch.
 */
function Je(e,t,n){const r=e.getResponseHeader(t);if(r.indexOf("{")===0){const o=S(r);for(const i in o){if(o.hasOwnProperty(i)){let e=o[i];if(D(e)){n=e.target!==undefined?e.target:n}else{e={value:e}}he(n,i,e)}}}else{const s=r.split(",");for(let e=0;e<s.length;e++){he(n,s[e].trim(),[])}}}const Ke=/\s/;const v=/[\s,]/;const Ge=/[_$a-zA-Z]/;const We=/[_$a-zA-Z0-9]/;const Ze=['"',"'","/"];const w=/[^\s]/;const Ye=/[{(]/;const Qe=/[})]/;/**
 * Splits a string into an array of tokens, treating quoted substrings and bracketed expressions as single tokens.
 *
 * Handles quoted strings (with escape sequences) and bracketed expressions, ensuring they are not split into separate tokens.
 *
 * @param {string} e - The input string to tokenize.
 * @returns {string[]} An array of tokens extracted from the input string.
 */
function et(e){const t=[];let n=0;while(n<e.length){if(Ge.exec(e.charAt(n))){var r=n;while(We.exec(e.charAt(n+1))){n++}t.push(e.substring(r,n+1))}else if(Ze.indexOf(e.charAt(n))!==-1){const o=e.charAt(n);var r=n;n++;while(n<e.length&&e.charAt(n)!==o){if(e.charAt(n)==="\\"){n++}n++}t.push(e.substring(r,n+1))}else{const i=e.charAt(n);t.push(i)}n++}return t}/**
 * Determines if a string should be treated as an expression rather than a literal value.
 *
 * Returns true if the first character of {@link e} matches the expression pattern, and {@link e} is not "true", "false", "this", or equal to {@link n}, and {@link t} is not a period.
 *
 * @param {string} e - The string to evaluate.
 * @param {string} t - The context or attribute name.
 * @param {string} n - A string to compare against {@link e} for exclusion.
 * @returns {boolean} True if {@link e} should be interpreted as an expression.
 */
function tt(e,t,n){return Ge.exec(e.charAt(0))&&e!=="true"&&e!=="false"&&e!=="this"&&e!==n&&t!=="."}/**
 * Parses and compiles a bracketed JavaScript expression from a token array into a function.
 *
 * The function consumes tokens from the array `o`, starting with a "[" and ending with a matching "]", and constructs a JavaScript function body using the provided variable name `i`. The resulting function evaluates the expression in the context of an object, falling back to the global `window` object for missing properties.
 *
 * @param {Object} r - The context object for variable resolution.
 * @param {string[]} o - The array of tokens representing the expression, with the first token expected to be "[".
 * @param {string} i - The variable name to use as the context in the generated function.
 * @returns {Function|null} A compiled function that evaluates the parsed expression, or `null` if a syntax error occurs.
 *
 * @remark
 * If a syntax error is encountered during function creation, a `htmx:syntax:error` event is triggered on the document body and `null` is returned.
 */
function nt(r,o,i){if(o[0]==="["){o.shift();let e=1;let t=" return (function("+i+"){ return (";let n=null;while(o.length>0){const s=o[0];if(s==="]"){e--;if(e===0){if(n===null){t=t+"true"}o.shift();t+=")})";try{const l=vn(r,function(){return Function(t)()},function(){return true});l.source=t;return l}catch(e){fe(ne().body,"htmx:syntax:error",{error:e,source:t});return null}}}else if(s==="["){e++}if(tt(s,n,i)){t+="(("+i+"."+s+") ? ("+i+"."+s+") : (window."+s+"))"}else{t=t+s}n=o.shift()}}}/**
 * Consumes characters from the start of an array until a character matches the given pattern.
 *
 * Removes and concatenates characters from the beginning of {@link e} until the first character matches the regular expression {@link t}, or until the array is empty.
 *
 * @param {string[]} e - The array of characters to process. This array is mutated.
 * @param {RegExp} t - The regular expression to test each character against.
 * @returns {string} The concatenated string of consumed characters.
 */
function C(e,t){let n="";while(e.length>0&&!t.test(e[0])){n+=e.shift()}return n}/**
 * Parses and returns a token from the beginning of the input array, handling quoted or bracketed tokens if present.
 *
 * If the first element matches the opening quote or bracket pattern, the function extracts the enclosed token using the appropriate delimiter and trims whitespace. Otherwise, it extracts the next token using a standard delimiter.
 *
 * @param {string[]} e - The array of string tokens to parse and consume from.
 * @returns {string} The parsed token, with enclosing quotes or brackets removed and whitespace trimmed if applicable.
 */
function rt(e){let t;if(e.length>0&&Ye.test(e[0])){e.shift();t=C(e,Qe).trim();e.shift()}else{t=C(e,v)}return t}const ot="input, textarea, select";/**
 * Parses an `hx-trigger` attribute value into an array of trigger specification objects.
 *
 * Each trigger specification describes how and when an event should trigger an action, including options such as polling intervals, event filters, throttling, queuing, and source/target selectors.
 *
 * @param {Element} e - The element whose trigger is being parsed.
 * @param {string} t - The trigger attribute value to parse.
 * @param {Object} [n] - Optional object to receive the parsed trigger specs under key {@link t}.
 * @returns {Array<Object>} An array of trigger specification objects representing the parsed triggers.
 *
 * @remark
 * If a syntax error is encountered in the trigger string, a `htmx:syntax:error` event is triggered on {@link e}.
 */
function it(e,t,n){const r=[];const o=et(t);do{C(o,w);const l=o.length;const c=C(o,/[,\[\s]/);if(c!==""){if(c==="every"){const u={trigger:"every"};C(o,w);u.pollInterval=d(C(o,/[,\[\s]/));C(o,w);var i=nt(e,o,"event");if(i){u.eventFilter=i}r.push(u)}else{const a={trigger:c};var i=nt(e,o,"event");if(i){a.eventFilter=i}C(o,w);while(o.length>0&&o[0]!==","){const f=o.shift();if(f==="changed"){a.changed=true}else if(f==="once"){a.once=true}else if(f==="consume"){a.consume=true}else if(f==="delay"&&o[0]===":"){o.shift();a.delay=d(C(o,v))}else if(f==="from"&&o[0]===":"){o.shift();if(Ye.test(o[0])){var s=rt(o)}else{var s=C(o,v);if(s==="closest"||s==="find"||s==="next"||s==="previous"){o.shift();const h=rt(o);if(h.length>0){s+=" "+h}}}a.from=s}else if(f==="target"&&o[0]===":"){o.shift();a.target=rt(o)}else if(f==="throttle"&&o[0]===":"){o.shift();a.throttle=d(C(o,v))}else if(f==="queue"&&o[0]===":"){o.shift();a.queue=C(o,v)}else if(f==="root"&&o[0]===":"){o.shift();a[f]=rt(o)}else if(f==="threshold"&&o[0]===":"){o.shift();a[f]=C(o,v)}else{fe(e,"htmx:syntax:error",{token:o.shift()})}C(o,w)}r.push(a)}}if(o.length===l){fe(e,"htmx:syntax:error",{token:o.shift()})}C(o,w)}while(o[0]===","&&o.shift());if(n){n[t]=r}return r}/**
 * Determines the trigger specifications for an element based on its attributes and type.
 *
 * If the element has an `hx-trigger` attribute, parses and returns its trigger specifications. Otherwise, returns default triggers based on the element type: `submit` for forms, `click` for buttons, `change` for inputs matching a specific selector, and `click` as a general fallback.
 *
 * @param {Element} e - The element to analyze for trigger specifications.
 * @returns {Array<Object>} An array of trigger specification objects for the element.
 */
function st(e){const t=te(e,"hx-trigger");let n=[];if(t){const r=Q.config.triggerSpecsCache;n=r&&r[t]||it(e,t,r)}if(n.length>0){return n}else if(h(e,"form")){return[{trigger:"submit"}]}else if(h(e,'input[type="button"], input[type="submit"]')){return[{trigger:"click"}]}else if(h(e,ot)){return[{trigger:"change"}]}else{return[{trigger:"click"}]}}/**
 * Cancels the current request associated with the given element.
 *
 * Marks the request as cancelled, preventing further processing or completion.
 */
function lt(e){ie(e).cancelled=true}/**
 * Sets up a recurring poll on an element, triggering a callback at specified intervals.
 *
 * The callback is invoked only if the element remains in the main document and the poll has not been canceled.
 * Polling continues until canceled or the element is removed from the document.
 *
 * @param {Element} e - The element to poll.
 * @param {Function} t - The callback function to execute on each poll.
 * @param {Object} n - The polling specification, including `pollInterval` and trigger details.
 */
function ct(e,t,n){const r=ie(e);r.timeout=E().setTimeout(function(){if(le(e)&&r.cancelled!==true){if(!gt(n,e,Mt("hx:poll:trigger",{triggerSpec:n,target:e}))){t(e)}ct(e,t,n)}},n.pollInterval)}/**
 * Determines if a given element's link is same-origin and not a fragment-only URL.
 *
 * @param {Element} e - The element to check, typically an anchor.
 * @returns {boolean} True if the element's hostname matches the current location and its `href` is not a fragment-only link.
 */
function ut(e){return location.hostname===e.hostname&&ee(e,"href")&&ee(e,"href").indexOf("#")!==0}/**
 * Returns the closest ancestor of the given element that matches the configured disable selector.
 *
 * @param {Element} e - The element from which to start searching.
 * @returns {Element|null} The closest ancestor matching the disable selector, or null if none is found.
 */
function at(e){return g(e,Q.config.disableSelector)}/**
 * Handles boosted navigation or form submission for anchor and form elements, triggering AJAX requests as appropriate.
 *
 * If the element is a boosted anchor (`<a>`) or a form (excluding dialog forms), this function sets the `boosted` flag, determines the HTTP method and URL, and attaches event listeners to trigger AJAX requests for each specified trigger.
 *
 * @param {Element} t - The anchor or form element to process.
 * @param {Object} n - The request context object, which will have its `boosted` property set if applicable.
 * @param {Array} e - An array of trigger specifications to attach to the element.
 */
function ft(t,n,e){if(t instanceof HTMLAnchorElement&&ut(t)&&(t.target===""||t.target==="_self")||t.tagName==="FORM"&&String(ee(t,"method")).toLowerCase()!=="dialog"){n.boosted=true;let r,o;if(t.tagName==="A"){r="get";o=ee(t,"href")}else{const i=ee(t,"method");r=i?i.toLowerCase():"get";o=ee(t,"action");if(o==null||o===""){o=ne().location.href}if(r==="get"&&o.includes("?")){o=o.replace(/\?[^#]+/,"")}}e.forEach(function(e){pt(t,function(e,t){const n=ue(e);if(at(n)){b(n);return}de(r,o,n,t)},n,e,true)})}}/**
 * Determines whether a given event should be ignored by htmx based on its type and target element.
 *
 * @param {Event} e - The event to evaluate.
 * @param {Element} t - The event target element.
 * @returns {boolean} True if the event should be ignored by htmx; otherwise, false.
 */
function ht(e,t){const n=ue(t);if(!n){return false}if(e.type==="submit"||e.type==="click"){if(n.tagName==="FORM"){return true}if(h(n,'input[type="submit"], button')&&(h(n,"[form]")||g(n,"form")!==null)){return true}if(n instanceof HTMLAnchorElement&&n.href&&(n.getAttribute("href")==="#"||n.getAttribute("href").indexOf("#")!==0)){return true}}return false}/**
 * Determines if a click event on a boosted anchor element should be treated as a modified navigation (e.g., Ctrl+Click or Cmd+Click).
 *
 * @param {Element} e - The element being interacted with.
 * @param {Event} t - The event object, typically a MouseEvent.
 * @returns {boolean} True if the element is a boosted anchor and the click event includes Ctrl or Meta key.
 */
function dt(e,t){return ie(e).boosted&&e instanceof HTMLAnchorElement&&t.type==="click"&&(t.ctrlKey||t.metaKey)}/**
 * Determines whether an event should be filtered out by invoking an optional event filter.
 *
 * If the event filter is defined and returns `true`, or throws an error, the event is considered filtered.
 *
 * @param {Object} e - An object that may contain an `eventFilter` function.
 * @param {Element} t - The context element for the filter.
 * @param {Event} n - The event to be filtered.
 * @returns {boolean} `true` if the event is filtered or an error occurs; otherwise, `false`.
 *
 * @remark
 * If the event filter throws an error, an `htmx:eventFilter:error` event is triggered on the document body.
 */
function gt(e,t,n){const r=e.eventFilter;if(r){try{return r.call(t,n)!==true}catch(e){const o=r.source;fe(ne().body,"htmx:eventFilter:error",{error:e,source:o});return true}}return false}/**
 * Attaches an event listener to one or more elements based on a trigger specification, supporting advanced options such as throttling, debouncing, one-time execution, value change detection, and event consumption.
 *
 * @param {Element} l - The source element to associate with the trigger.
 * @param {Function} c - The callback to invoke when the trigger fires.
 * @param {Element} e - The element to which the event listener is attached.
 * @param {Object} u - The trigger specification, including event type and options (e.g., throttle, delay, once, changed, consume, target).
 * @param {boolean} [a] - If true, prevents the default action for the event.
 *
 * @remark
 * - If `u.changed` is set, the callback only fires when the value of the target element changes.
 * - If `u.once` is set, the callback fires only once per element.
 * - If `u.throttle` or `u.delay` is set, the callback is throttled or delayed accordingly.
 * - If `u.consume` is set, event propagation is stopped after handling.
 */
function pt(l,c,e,u,a){const f=ie(l);let t;if(u.from){t=p(l,u.from)}else{t=[l]}if(u.changed){if(!("lastValue"in f)){f.lastValue=new WeakMap}t.forEach(function(e){if(!f.lastValue.has(u)){f.lastValue.set(u,new WeakMap)}f.lastValue.get(u).set(e,e.value)})}se(t,function(i){const s=function(e){if(!le(l)){i.removeEventListener(u.trigger,s);return}if(dt(l,e)){return}if(a||ht(e,l)){e.preventDefault()}if(gt(u,l,e)){return}const t=ie(e);t.triggerSpec=u;if(t.handledFor==null){t.handledFor=[]}if(t.handledFor.indexOf(l)<0){t.handledFor.push(l);if(u.consume){e.stopPropagation()}if(u.target&&e.target){if(!h(ue(e.target),u.target)){return}}if(u.once){if(f.triggeredOnce){return}else{f.triggeredOnce=true}}if(u.changed){const n=event.target;const r=n.value;const o=f.lastValue.get(u);if(o.has(n)&&o.get(n)===r){return}o.set(n,r)}if(f.delayed){clearTimeout(f.delayed)}if(f.throttle){return}if(u.throttle>0){if(!f.throttle){he(l,"htmx:trigger");c(l,e);f.throttle=E().setTimeout(function(){f.throttle=null},u.throttle)}}else if(u.delay>0){f.delayed=E().setTimeout(function(){he(l,"htmx:trigger");c(l,e)},u.delay)}else{he(l,"htmx:trigger");c(l,e)}}};if(e.listenerInfos==null){e.listenerInfos=[]}e.listenerInfos.push({trigger:u.trigger,listener:s,on:i});i.addEventListener(u.trigger,s)})}let mt=false;let xt=null;/**
 * Initializes and manages the detection of elements with a "revealed" trigger, dispatching events when they enter the viewport.
 *
 * Sets up scroll and resize listeners, and periodically checks for elements with `hx-trigger` or `data-hx-trigger` containing "revealed", triggering the appropriate logic when such elements become visible.
 *
 * @remark This function ensures that the "revealed" trigger is processed only once per page lifecycle.
 */
function yt(){if(!xt){xt=function(){mt=true};window.addEventListener("scroll",xt);window.addEventListener("resize",xt);setInterval(function(){if(mt){mt=false;se(ne().querySelectorAll("[hx-trigger*='revealed'],[data-hx-trigger*='revealed']"),function(e){bt(e)})}},200)}}/**
 * Marks an element as revealed and triggers the "revealed" event if it becomes visible in the viewport.
 *
 * If the element has not already been marked as revealed and is currently visible, sets the `data-hx-revealed` attribute to "true". Immediately triggers the "revealed" event if the element's extension has `initHash` set; otherwise, waits until the "htmx:afterProcessNode" event before triggering "revealed".
 */
function bt(e){if(!s(e,"data-hx-revealed")&&X(e)){e.setAttribute("data-hx-revealed","true");const t=ie(e);if(t.initHash){he(e,"revealed")}else{e.addEventListener("htmx:afterProcessNode",function(){he(e,"revealed")},{once:true})}}}/**
 * Triggers a callback after a specified delay, ensuring it only runs once per element.
 *
 * Dispatches the `htmx:trigger` event on the element before invoking the callback. The callback is only executed if the associated state object's `loaded` property is `false`, preventing duplicate execution.
 *
 * @param {Element} e - The target element.
 * @param {Function} t - The callback to invoke after the delay.
 * @param {Object} n - State object with a `loaded` property to prevent duplicate execution.
 * @param {number} r - Delay in milliseconds before triggering the callback. If zero or less, the callback is invoked immediately.
 */
function vt(e,t,n,r){const o=function(){if(!n.loaded){n.loaded=true;he(e,"htmx:trigger");t(e)}};if(r>0){E().setTimeout(o,r)}else{o()}}/**
 * Attaches event listeners to an element for each HTTP verb attribute present and triggers AJAX requests when those events occur.
 *
 * @param {Element} t - The target element to process.
 * @param {Object} n - An object to receive the path and verb for the request.
 * @param {Array<string>} e - A list of event names to listen for.
 * @returns {boolean} True if any HTTP verb attribute was found and processed on the element; otherwise, false.
 */
function wt(t,n,e){let i=false;se(r,function(r){if(s(t,"hx-"+r)){const o=te(t,"hx-"+r);i=true;n.path=o;n.verb=r;e.forEach(function(e){St(t,e,n,function(e,t){const n=ue(e);if(g(n,Q.config.disableSelector)){b(n);return}de(r,o,n,t)})})}});return i}/**
 * Attaches event listeners or observers to an element based on the specified trigger type.
 *
 * Handles special triggers such as "revealed", "intersect", "load", and polling intervals by setting up the appropriate event listeners, observers, or timers. For other triggers, delegates to the standard trigger handler.
 *
 * @param {Element} r - The target element.
 * @param {Object} e - The trigger specification object.
 * @param {Object} t - State object for initialization and polling.
 * @param {Element} n - The context or root element for event delegation.
 */
function St(r,e,t,n){if(e.trigger==="revealed"){yt();pt(r,n,t,e);bt(ue(r))}else if(e.trigger==="intersect"){const o={};if(e.root){o.root=ae(r,e.root)}if(e.threshold){o.threshold=parseFloat(e.threshold)}const i=new IntersectionObserver(function(t){for(let e=0;e<t.length;e++){const n=t[e];if(n.isIntersecting){he(r,"intersect");break}}},o);i.observe(ue(r));pt(ue(r),n,t,e)}else if(!t.firstInitCompleted&&e.trigger==="load"){if(!gt(e,r,Mt("load",{elt:r}))){vt(ue(r),n,t,e.delay)}}else if(e.pollInterval>0){t.polling=true;ct(ue(r),n,e)}else{pt(r,n,t,e)}}/**
 * Determines whether the given element has any `hx-on` or `data-hx-on` event handler attributes.
 *
 * @param {Element|string} e - The element or selector to check.
 * @returns {boolean} True if the element has at least one `hx-on` or `data-hx-on` attribute; otherwise, false.
 */
function Et(e){const t=ue(e);if(!t){return false}const n=t.attributes;for(let e=0;e<n.length;e++){const r=n[e].name;if(l(r,"hx-on:")||l(r,"data-hx-on:")||l(r,"hx-on-")||l(r,"data-hx-on-")){return true}}return false}const Ct=(new XPathEvaluator).createExpression('.//*[@*[ starts-with(name(), "hx-on:") or starts-with(name(), "data-hx-on:") or'+' starts-with(name(), "hx-on-") or starts-with(name(), "data-hx-on-") ]]');/**
 * Collects elements starting from a given element and its descendants that have `hx-on` event handlers.
 *
 * Adds the provided element and all descendant elements with `hx-on` attributes to the given array.
 *
 * @param {Element} e - The root element to start the search from.
 * @param {Array} t - The array to which matching elements are added.
 */
function Ot(e,t){if(Et(e)){t.push(ue(e))}const n=Ct.evaluate(e);let r=null;while(r=n.iterateNext())t.push(ue(r))}/**
 * Collects all elements within a DocumentFragment or a single element that have `hx-on` attributes.
 *
 * @param {Element|DocumentFragment} e - The element or fragment to search.
 * @returns {Element[]} An array of elements containing `hx-on` attributes.
 */
function Rt(e){const t=[];if(e instanceof DocumentFragment){for(const n of e.childNodes){Ot(n,t)}}else{Ot(e,t)}return t}/**
 * Returns a NodeList of elements within the given root that are relevant for htmx processing.
 *
 * This includes elements with htmx attributes, forms, submit buttons, boosted links, and any selectors provided by registered extensions.
 *
 * @param {Element|Document} e - The root element or document to search within.
 * @returns {NodeList} A NodeList of elements matching htmx-related selectors.
 */
function Ht(e){if(e.querySelectorAll){const n=", [hx-boost] a, [data-hx-boost] a, a[hx-boost], a[data-hx-boost]";const r=[];for(const i in Mn){const s=Mn[i];if(s.getSelectors){var t=s.getSelectors();if(t){r.push(t)}}}const o=e.querySelectorAll(H+n+", form, [type='submit'],"+" [hx-ext], [data-hx-ext], [hx-trigger], [data-hx-trigger]"+r.flat().map(e=>", "+e).join(""));return o}else{return[]}}/**
 * Tracks the last button or submit input clicked within a form during an event.
 *
 * Updates the form's state to record which button or submit input triggered the event, enabling accurate form submission context.
 */
function Tt(e){const t=g(ue(e.target),"button, input[type='submit']");const n=Lt(e);if(n){n.lastButtonClicked=t}}/**
 * Clears the last button clicked state for the form containing the given element.
 *
 * @param {Element} e - The element whose containing form's last button clicked state will be reset.
 */
function qt(e){const t=Lt(e);if(t){t.lastButtonClicked=null}}/**
 * Retrieves the form values from the form associated with the submit button or input that triggered an event.
 *
 * @param {Event} e - The event triggered by a button or input element.
 * @returns {Object|undefined} The form values if a related form is found; otherwise, undefined.
 */
function Lt(e){const t=g(ue(e.target),"button, input[type='submit']");if(!t){return}const n=y("#"+ee(t,"form"),t.getRootNode())||g(t,"form");if(!n){return}return ie(n)}/**
 * Attaches event listeners to an element for tracking button interactions within forms.
 *
 * Adds listeners for `click` and `focusin` events to handle button activation, and a `focusout` listener to handle deactivation or cleanup.
 */
function At(e){e.addEventListener("click",Tt);e.addEventListener("focusin",Tt);e.addEventListener("focusout",qt)}/**
 * Attaches an event listener to an element that executes a dynamically created handler function.
 *
 * The handler is constructed from the provided JavaScript code string and is invoked with the event object when the specified event occurs. The listener is tracked for potential removal.
 *
 * @param {Element} t - The target element to attach the event listener to.
 * @param {string} e - The event type to listen for (e.g., 'click', 'input').
 * @param {string} n - JavaScript code as a string to be executed when the event is triggered.
 */
function Nt(t,e,n){const r=ie(t);if(!Array.isArray(r.onHandlers)){r.onHandlers=[]}let o;const i=function(e){vn(t,function(){if(at(t)){return}if(!o){o=new Function("event",n)}o.call(t,e)})};t.addEventListener(e,i);r.onHandlers.push({event:e,listener:i})}/**
 * Processes all `hx-on` or `data-hx-on` attributes on an element and attaches the corresponding event listeners.
 *
 * For each matching attribute, determines the event name and delegates to the event listener attachment logic.
 */
function It(t){ke(t);for(let e=0;e<t.attributes.length;e++){const n=t.attributes[e].name;const r=t.attributes[e].value;if(l(n,"hx-on")||l(n,"data-hx-on")){const o=n.indexOf("-on")+3;const i=n.slice(o,o+1);if(i==="-"||i===":"){let e=n.slice(o+1);if(l(e,":")){e="htmx"+e}else if(l(e,"-")){e="htmx:"+e.slice(1)}else if(l(e,"htmx-")){e="htmx:"+e.slice(5)}Nt(t,e,r)}}}}/**
 * Processes a DOM node for htmx behavior, initializing triggers, extensions, and event listeners as needed.
 *
 * Skips processing if the node matches the configured disable selector. Initializes htmx triggers, boost behavior, and form handling for the node, and dispatches lifecycle events before and after processing.
 *
 * @param {Element} t - The DOM node to process.
 */
function Pt(t){if(g(t,Q.config.disableSelector)){b(t);return}const n=ie(t);const e=Pe(t);if(n.initHash!==e){De(t);n.initHash=e;he(t,"htmx:beforeProcessNode");const r=st(t);const o=wt(t,n,r);if(!o){if(re(t,"hx-boost")==="true"){ft(t,n,r)}else if(s(t,"hx-trigger")){r.forEach(function(e){St(t,e,n,function(){})})}}if(t.tagName==="FORM"||ee(t,"type")==="submit"&&s(t,"form")){At(t)}n.firstInitCompleted=true;he(t,"htmx:afterProcessNode")}}/**
 * Processes a root element and its descendants, initializing htmx behavior and event listeners.
 *
 * Skips elements matching the configured disable selector. Initializes triggers, extensions, and event handlers for elements with htmx attributes, and processes inline event handlers.
 *
 * @param {Element|string} e - The root element or selector to process.
 */
function kt(e){e=y(e);if(g(e,Q.config.disableSelector)){b(e);return}Pt(e);se(Ht(e),function(e){Pt(e)});se(Rt(e),It)}/**
 * Converts a camelCase string to kebab-case.
 *
 * @param {string} e - The camelCase string to convert.
 * @returns {string} The resulting kebab-case string.
 */
function Dt(e){return e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase()}/**
 * Creates a CustomEvent with the specified name and detail, ensuring compatibility with older browsers.
 *
 * @param {string} e - The name of the event.
 * @param {*} t - The detail data to include with the event.
 * @returns {CustomEvent} A CustomEvent instance with the given name and detail.
 */
function Mt(e,t){let n;if(window.CustomEvent&&typeof window.CustomEvent==="function"){n=new CustomEvent(e,{bubbles:true,cancelable:true,composed:true,detail:t})}else{n=ne().createEvent("CustomEvent");n.initCustomEvent(e,true,true,t)}return n}/**
 * Dispatches a custom error event with the specified type and detail on the given element.
 *
 * @param {Element} e - The target element on which to dispatch the error event.
 * @param {string} t - The error event type.
 * @param {Object} [n] - Additional detail to include in the event.
 */
function fe(e,t,n){he(e,t,ce({error:t},n))}/**
 * Determines if the given event name is "htmx:afterProcessNode".
 *
 * @param {string} e - The event name to check.
 * @returns {boolean} True if {@link e} is "htmx:afterProcessNode"; otherwise, false.
 */
function Xt(e){return e==="htmx:afterProcessNode"}/**
 * Iterates over all extensions associated with an element and applies a callback to each.
 *
 * @param {Element} e - The element whose extensions will be processed.
 * @param {Function} t - The callback function to apply to each extension.
 *
 * @remark
 * If the callback throws an error for any extension, the error is caught and logged without interrupting the iteration.
 */
function Ft(e,t){se(Un(e),function(e){try{t(e)}catch(e){O(e)}})}/**
 * Logs an error message to the console.
 *
 * Uses `console.error` if available; otherwise falls back to `console.log`.
 *
 * @param {*} e - The error or message to log.
 */
function O(e){if(console.error){console.error(e)}else if(console.log){console.log("ERROR: ",e)}}/**
 * Dispatches a custom event with the specified name and detail on the given element.
 *
 * If a logger is configured and the event is not internal, logs the event. If the detail contains an error, logs the error and dispatches an `htmx:error` event. If the event name is transformed by `Dt`, dispatches the transformed event as well. Invokes any registered extension event handlers, and returns whether the event was not canceled.
 *
 * @param {Element|string} e - The target element or a selector string.
 * @param {string} t - The event name to dispatch.
 * @param {Object} [n] - Optional detail object to include with the event.
 * @returns {boolean} True if the event was not canceled by any handler; otherwise, false.
 */
function he(e,t,n){e=y(e);if(n==null){n={}}n.elt=e;const r=Mt(t,n);if(Q.logger&&!Xt(t)){Q.logger(e,t,n)}if(n.error){O(n.error);he(e,"htmx:error",{errorInfo:n})}let o=e.dispatchEvent(r);const i=Dt(t);if(o&&i!==t){const s=Mt(i,r.detail);o=o&&e.dispatchEvent(s)}Ft(ue(e),function(e){o=o&&(e.onEvent(t,r)!==false&&!r.defaultPrevented)});return o}let Bt=location.pathname+location.search;/**
 * Returns the element designated for history state management.
 *
 * If an element with the `hx-history-elt` or `data-hx-history-elt` attribute exists in the main document, it is returned; otherwise, the document body is returned.
 *
 * @returns {Element} The history element or the document body.
 */
function Ut(){const e=ne().querySelector("[hx-history-elt],[data-hx-history-elt]");return e||ne().body}/**
 * Saves the current page state to the htmx history cache in localStorage.
 *
 * Removes any existing cache entry for the given URL, adds the current page's content, title, and scroll position, and ensures the cache does not exceed the configured size. Triggers `htmx:historyItemCreated` after adding an entry, and `htmx:historyCacheError` if saving to localStorage fails.
 *
 * @param {string} t - The URL to associate with the cached state.
 * @param {Element} e - The root element whose content should be cached.
 */
function jt(t,e){if(!B()){return}const n=_t(e);const r=ne().title;const o=window.scrollY;if(Q.config.historyCacheSize<=0){localStorage.removeItem("htmx-history-cache");return}t=U(t);const i=S(localStorage.getItem("htmx-history-cache"))||[];for(let e=0;e<i.length;e++){if(i[e].url===t){i.splice(e,1);break}}const s={url:t,content:n,title:r,scroll:o};he(ne().body,"htmx:historyItemCreated",{item:s,cache:i});i.push(s);while(i.length>Q.config.historyCacheSize){i.shift()}while(i.length>0){try{localStorage.setItem("htmx-history-cache",JSON.stringify(i));break}catch(e){fe(ne().body,"htmx:historyCacheError",{cause:e,cache:i});i.shift()}}}/**
 * Retrieves a cached history entry for the specified URL from localStorage.
 *
 * @param {string} t - The URL whose history cache entry should be retrieved.
 * @returns {object|null} The cached history entry object if found, or {@code null} if not present or localStorage is unavailable.
 */
function Vt(t){if(!B()){return null}t=U(t);const n=S(localStorage.getItem("htmx-history-cache"))||[];for(let e=0;e<n.length;e++){if(n[e].url===t){return n[e]}}return null}/**
 * Returns the HTML content of a cloned element after removing request-related classes and re-enabling elements disabled by htmx.
 *
 * Clones the provided element, removes the configured request class from all descendants, and removes the `disabled` attribute from elements marked as disabled by htmx. Returns the resulting inner HTML of the clone.
 *
 * @param {Element} e - The element to clone and process.
 * @returns {string} The processed inner HTML of the cloned element.
 */
function _t(e){const t=Q.config.requestClass;const n=e.cloneNode(true);se(x(n,"."+t),function(e){G(e,t)});se(x(n,"[data-disabled-by-htmx]"),function(e){e.removeAttribute("disabled")});return n.innerHTML}/**
 * Saves the current page state to the history cache and updates the browser's history state.
 *
 * If no element disables history caching, triggers the `htmx:beforeHistorySave` event and stores the current state in localStorage. Updates the browser's history state if history management is enabled.
 */
function zt(){const e=Ut();const t=Bt||location.pathname+location.search;let n;try{n=ne().querySelector('[hx-history="false" i],[data-hx-history="false" i]')}catch(e){n=ne().querySelector('[hx-history="false"],[data-hx-history="false"]')}if(!n){he(ne().body,"htmx:beforeHistorySave",{path:t,historyElt:e});jt(t,e)}if(Q.config.historyEnabled)history.replaceState({htmx:true},ne().title,window.location.href)}/**
 * Pushes a new browser history state with the given URL, updating the internal history tracking.
 *
 * Removes any cache buster parameter from the URL if configured, then updates the browser's history using `pushState`.
 *
 * @param {string} e - The URL to push onto the browser history stack.
 */
function $t(e){if(Q.config.getCacheBusterParam){e=e.replace(/org\.htmx\.cache-buster=[^&]*&?/,"");if(Y(e,"&")||Y(e,"?")){e=e.slice(0,-1)}}if(Q.config.historyEnabled){history.pushState({htmx:true},"",e)}Bt=e}/**
 * Replaces the current browser history state with a new URL if history management is enabled.
 *
 * @param {string} e - The URL to set in the browser's address bar.
 */
function Jt(e){if(Q.config.historyEnabled)history.replaceState({htmx:true},"",e);Bt=e}/**
 * Invokes each function in the provided array.
 *
 * @param {Function[]} e - An array of functions to be called.
 */
function Kt(e){se(e,function(e){e.call(undefined)})}/**
 * Attempts to restore a history state by making a GET request to the specified URL and updating the DOM with the server response.
 *
 * Triggers custom events for history cache miss, successful load, and restoration. If the request fails, triggers an error event.
 *
 * @param {string} o - The URL to request for restoring the history state.
 */
function Gt(o){const e=new XMLHttpRequest;const i={path:o,xhr:e};he(ne().body,"htmx:historyCacheMiss",i);e.open("GET",o,true);e.setRequestHeader("HX-Request","true");e.setRequestHeader("HX-History-Restore-Request","true");e.setRequestHeader("HX-Current-URL",ne().location.href);e.onload=function(){if(this.status>=200&&this.status<400){he(ne().body,"htmx:historyCacheMissLoad",i);const e=P(this.response);const t=e.querySelector("[hx-history-elt],[data-hx-history-elt]")||e;const n=Ut();const r=xn(n);kn(e.title);qe(e);Ve(n,t,r);Te();Kt(r.tasks);Bt=o;he(ne().body,"htmx:historyRestore",{path:o,cacheMiss:true,serverResponse:this.response})}else{fe(ne().body,"htmx:historyCacheMissLoadError",i)}};e.send()}/**
 * Restores the page state from the history cache for a given path, or reloads the page if the cache is missing.
 *
 * If a cached entry exists for the specified path, restores the DOM, title, scroll position, and triggers the `htmx:historyRestore` event. If no cache is found, either reloads the page or navigates to the path, depending on configuration.
 *
 * @param {string} [e] - The path to restore. Defaults to the current location's pathname and search.
 */
function Wt(e){zt();e=e||location.pathname+location.search;const t=Vt(e);if(t){const n=P(t.content);const r=Ut();const o=xn(r);kn(t.title);qe(n);Ve(r,n,o);Te();Kt(o.tasks);E().setTimeout(function(){window.scrollTo(0,t.scroll)},0);Bt=e;he(ne().body,"htmx:historyRestore",{path:e,item:t})}else{if(Q.config.refreshOnHistoryMiss){window.location.reload(true)}else{Gt(e)}}}/**
 * Activates request indicators for the given element by adding the configured request CSS class.
 *
 * Increments the internal request count for each indicator element. If no `hx-indicator` attribute is present, the element itself is used as the indicator.
 *
 * @param {Element} e - The element to activate indicators for.
 * @returns {Element[]} An array of indicator elements that were activated.
 */
function Zt(e){let t=we(e,"hx-indicator");if(t==null){t=[e]}se(t,function(e){const t=ie(e);t.requestCount=(t.requestCount||0)+1;e.classList.add.call(e.classList,Q.config.requestClass)});return t}/**
 * Disables elements associated with the given element by setting their `disabled` attribute.
 *
 * Increments a request counter on each disabled element and marks them as disabled by htmx.
 *
 * @param {Element} e - The element whose associated disabled elements will be processed.
 * @returns {Element[]} An array of elements that were disabled.
 */
function Yt(e){let t=we(e,"hx-disabled-elt");if(t==null){t=[]}se(t,function(e){const t=ie(e);t.requestCount=(t.requestCount||0)+1;e.setAttribute("disabled","");e.setAttribute("data-disabled-by-htmx","")});return t}/**
 * Decrements the request count for the given elements and updates their state.
 *
 * Removes the request CSS class from elements in {@link e} when their request count reaches zero.
 * Re-enables elements in {@link t} by removing the `disabled` and `data-disabled-by-htmx` attributes when their request count reaches zero.
 *
 * @param {Element[]} e - Elements to update request class and request count.
 * @param {Element[]} t - Elements to re-enable after request completion.
 */
function Qt(e,t){se(e.concat(t),function(e){const t=ie(e);t.requestCount=(t.requestCount||1)-1});se(e,function(e){const t=ie(e);if(t.requestCount===0){e.classList.remove.call(e.classList,Q.config.requestClass)}});se(t,function(e){const t=ie(e);if(t.requestCount===0){e.removeAttribute("disabled");e.removeAttribute("data-disabled-by-htmx")}})}/**
 * Determines whether a given node is present in a list of nodes using `isSameNode` comparison.
 *
 * @param {Node[]} t - The list of nodes to search.
 * @param {Node} n - The node to check for presence in the list.
 * @returns {boolean} `true` if {@link n} is found in {@link t}; otherwise, `false`.
 */
function en(t,n){for(let e=0;e<t.length;e++){const r=t[e];if(r.isSameNode(n)){return true}}return false}/**
 * Determines if a form control element should be included in form submission.
 *
 * Returns `true` if the element is enabled, has a valid name, is not a button, submit, image, reset, or file input, and (for checkboxes and radios) is checked.
 *
 * @param {Element} e - The form control element to evaluate.
 * @returns {boolean} `true` if the element should be included in form data; otherwise, `false`.
 */
function tn(e){const t=e;if(t.name===""||t.name==null||t.disabled||g(t,"fieldset[disabled]")){return false}if(t.type==="button"||t.type==="submit"||t.tagName==="image"||t.tagName==="reset"||t.tagName==="file"){return false}if(t.type==="checkbox"||t.type==="radio"){return t.checked}return true}/**
 * Appends a key-value pair or multiple values to a FormData or similar object.
 *
 * If {@link e} is an array, each value is appended with the same key {@link t}; otherwise, the single value is appended.
 *
 * @param {string} t - The key to append.
 * @param {*} e - The value or array of values to append.
 * @param {FormData} n - The FormData or compatible object to which values are appended.
 */
function nn(t,e,n){if(t!=null&&e!=null){if(Array.isArray(e)){e.forEach(function(e){n.append(t,e)})}else{n.append(t,e)}}}/**
 * Removes specific values from a FormData entry.
 *
 * If {@link n} is an array, all matching values are removed from the FormData entry with key {@link t}. If {@link n} is a single value, only that value is removed. The remaining values for the key are preserved.
 *
 * @param {string} t - The FormData key to modify.
 * @param {string|string[]} n - The value or array of values to remove.
 * @param {FormData} r - The FormData object to update.
 */
function rn(t,n,r){if(t!=null&&n!=null){let e=r.getAll(t);if(Array.isArray(n)){e=e.filter(e=>n.indexOf(e)<0)}else{e=e.filter(e=>e!==n)}r.delete(t);se(e,e=>r.append(t,e))}}/**
 * Collects and serializes form control values from a given element or form into a target object.
 *
 * Handles input elements, select elements (including multiple selections), file inputs, and forms. For forms, iterates through all elements and includes their values. Optionally marks elements as processed.
 *
 * @param {Array} processed - Array tracking already processed elements to avoid duplicates.
 * @param {Object} target - Object to receive name-value pairs.
 * @param {string} prefix - Optional prefix for nested parameter names.
 * @param {Element} element - The element or form to process.
 * @param {boolean} markProcessed - If true, marks processed elements.
 */
function on(t,n,r,o,i){if(o==null||en(t,o)){return}else{t.push(o)}if(tn(o)){const s=ee(o,"name");let e=o.value;if(o instanceof HTMLSelectElement&&o.multiple){e=M(o.querySelectorAll("option:checked")).map(function(e){return e.value})}if(o instanceof HTMLInputElement&&o.files){e=M(o.files)}nn(s,e,n);if(i){sn(o,r)}}if(o instanceof HTMLFormElement){se(o.elements,function(e){if(t.indexOf(e)>=0){rn(e.name,e.value,n)}else{t.push(e)}if(i){sn(e,r)}});new FormData(o).forEach(function(e,t){if(e instanceof File&&e.name===""){return}nn(t,e,n)})}}/**
 * Validates a form control element and records validation errors if present.
 *
 * If the element is subject to validation and fails, its validation message and validity state are added to the provided errors array, and relevant custom events are triggered.
 *
 * @param {HTMLElement} e - The form control element to validate.
 * @param {Array} t - The array to which validation error objects will be appended.
 */
function sn(e,t){const n=e;if(n.willValidate){he(n,"htmx:validation:validate");if(!n.checkValidity()){t.push({elt:n,message:n.validationMessage,validity:n.validity});he(n,"htmx:validation:failed",{message:n.validationMessage,validity:n.validity})}}}/**
 * Replaces all entries in a FormData object with those from another FormData.
 *
 * Removes all existing keys from {@link n}, then appends all key-value pairs from {@link e}.
 *
 * @param {FormData} n - The FormData object to update.
 * @param {FormData} e - The FormData object providing new entries.
 * @returns {FormData} The updated FormData object.
 */
function ln(n,e){for(const t of e.keys()){n.delete(t)}e.forEach(function(e,t){n.append(t,e)});return n}/**
 * Extracts form values and validation errors from an element for a given HTTP method.
 *
 * Collects form data, including values from included elements and the last clicked submit button, and performs validation if required. Returns an object containing any validation errors, the constructed FormData, and a proxy for convenient value access.
 *
 * @param {Element} e - The root element to extract values from, typically a form or input.
 * @param {string} t - The HTTP method (e.g., "get", "post") determining how data is collected.
 * @returns {{errors: Array, formData: FormData, values: Object}} An object with validation errors, the FormData, and a proxy for value access.
 */
function cn(e,t){const n=[];const r=new FormData;const o=new FormData;const i=[];const s=ie(e);if(s.lastButtonClicked&&!le(s.lastButtonClicked)){s.lastButtonClicked=null}let l=e instanceof HTMLFormElement&&e.noValidate!==true||te(e,"hx-validate")==="true";if(s.lastButtonClicked){l=l&&s.lastButtonClicked.formNoValidate!==true}if(t!=="get"){on(n,o,i,g(e,"form"),l)}on(n,r,i,e,l);if(s.lastButtonClicked||e.tagName==="BUTTON"||e.tagName==="INPUT"&&ee(e,"type")==="submit"){const u=s.lastButtonClicked||e;const a=ee(u,"name");nn(a,u.value,o)}const c=we(e,"hx-include");se(c,function(e){on(n,r,i,ue(e),l);if(!h(e,"form")){se(f(e).querySelectorAll(ot),function(e){on(n,r,i,e,l)})}});ln(r,o);return{errors:i,formData:r,values:An(r)}}/**
 * Appends a URL-encoded key-value pair to an existing query string.
 *
 * If the value is an object, it is stringified as JSON before encoding.
 *
 * @param {string} e - The existing query string to append to.
 * @param {string} t - The key to add.
 * @param {*} n - The value to add; objects are JSON-stringified.
 * @returns {string} The updated query string with the new key-value pair.
 */
function un(e,t,n){if(e!==""){e+="&"}if(String(n)==="[object Object]"){n=JSON.stringify(n)}const r=encodeURIComponent(n);e+=encodeURIComponent(t)+"="+r;return e}/**
 * Serializes the given form or object into a URL-encoded query string.
 *
 * Converts the input into a {@link FormData} instance and encodes each key-value pair for use in URL query parameters.
 *
 * @param {HTMLFormElement|Object|FormData} e - The form, object, or FormData to serialize.
 * @returns {string} The URL-encoded query string representing the input data.
 */
function an(e){e=qn(e);let n="";e.forEach(function(e,t){n=un(n,t,e)});return n}/**
 * Builds the headers object for an AJAX request, including htmx-specific headers.
 *
 * Adds headers such as `HX-Request`, `HX-Trigger`, `HX-Trigger-Name`, `HX-Target`, and `HX-Current-URL` based on the source element and target. Optionally includes `HX-Prompt` if a prompt value is provided, and `HX-Boosted` if the request is boosted.
 *
 * @param {Element} e - The source element that triggered the request.
 * @param {Element} t - The target element for the request.
 * @param {string} [n] - Optional prompt value to include in the headers.
 * @returns {Object} An object containing the constructed headers for the AJAX request.
 */
function fn(e,t,n){const r={"HX-Request":"true","HX-Trigger":ee(e,"id"),"HX-Trigger-Name":ee(e,"name"),"HX-Target":te(t,"id"),"HX-Current-URL":ne().location.href};bn(e,"hx-headers",false,r);if(n!==undefined){r["HX-Prompt"]=n}if(ie(e).boosted){r["HX-Boosted"]="true"}return r}/**
 * Filters form parameters from a FormData object based on the `hx-params` attribute.
 *
 * Returns a new FormData instance containing only the parameters specified by `hx-params`, or excludes parameters if prefixed with "not ". If `hx-params` is "none", returns an empty FormData. If `hx-params` is "*", returns the original FormData. If `hx-params` is not present, returns the original FormData.
 *
 * @param {FormData} n - The original FormData object.
 * @param {Element} e - The element from which to read the `hx-params` attribute.
 * @returns {FormData} The filtered FormData object.
 */
function hn(n,e){const t=re(e,"hx-params");if(t){if(t==="none"){return new FormData}else if(t==="*"){return n}else if(t.indexOf("not ")===0){se(t.slice(4).split(","),function(e){e=e.trim();n.delete(e)});return n}else{const r=new FormData;se(t.split(","),function(t){t=t.trim();if(n.has(t)){n.getAll(t).forEach(function(e){r.append(t,e)})}});return r}}else{return n}}/**
 * Determines whether the given element has an `href` attribute containing a hash (`#`).
 *
 * @param {Element} e - The element to check.
 * @returns {boolean} `true` if the element's `href` attribute exists and contains a `#`; otherwise, `false`.
 */
function dn(e){return!!ee(e,"href")&&ee(e,"href").indexOf("#")>=0}/**
 * Parses the `hx-swap` attribute or provided swap specification and returns swap options for DOM updates.
 *
 * The returned object includes swap style, delays, scroll and show behaviors, transition, and other swap-related options, applying defaults and parsing modifiers as needed.
 *
 * @param {Element} e - The element whose swap options are being determined.
 * @param {string} [t] - Optional swap specification string; if omitted, the function reads the `hx-swap` attribute from {@link e}.
 * @returns {Object} An object containing swap options such as `swapStyle`, `swapDelay`, `settleDelay`, `transition`, `ignoreTitle`, `scroll`, `scrollTarget`, `show`, `showTarget`, and `focusScroll`.
 */
function gn(e,t){const n=t||re(e,"hx-swap");const r={swapStyle:ie(e).boosted?"innerHTML":Q.config.defaultSwapStyle,swapDelay:Q.config.defaultSwapDelay,settleDelay:Q.config.defaultSettleDelay};if(Q.config.scrollIntoViewOnBoost&&ie(e).boosted&&!dn(e)){r.show="top"}if(n){const s=F(n);if(s.length>0){for(let e=0;e<s.length;e++){const l=s[e];if(l.indexOf("swap:")===0){r.swapDelay=d(l.slice(5))}else if(l.indexOf("settle:")===0){r.settleDelay=d(l.slice(7))}else if(l.indexOf("transition:")===0){r.transition=l.slice(11)==="true"}else if(l.indexOf("ignoreTitle:")===0){r.ignoreTitle=l.slice(12)==="true"}else if(l.indexOf("scroll:")===0){const c=l.slice(7);var o=c.split(":");const u=o.pop();var i=o.length>0?o.join(":"):null;r.scroll=u;r.scrollTarget=i}else if(l.indexOf("show:")===0){const a=l.slice(5);var o=a.split(":");const f=o.pop();var i=o.length>0?o.join(":"):null;r.show=f;r.showTarget=i}else if(l.indexOf("focus-scroll:")===0){const h=l.slice("focus-scroll:".length);r.focusScroll=h=="true"}else if(e==0){r.swapStyle=l}else{O("Unknown modifier in hx-swap: "+l)}}}}return r}/**
 * Determines if the given element should use multipart/form-data encoding.
 *
 * Returns true if the element has an `hx-encoding` attribute set to "multipart/form-data",
 * or if it is a form element with an `enctype` attribute set to "multipart/form-data".
 *
 * @param {Element} e - The element to check.
 * @returns {boolean} True if multipart/form-data encoding is specified.
 */
function pn(e){return re(e,"hx-encoding")==="multipart/form-data"||h(e,"form")&&ee(e,"enctype")==="multipart/form-data"}/**
 * Encodes request parameters for an AJAX request, using extension hooks if available.
 *
 * If any registered extension provides an `encodeParameters` method, its result is used.
 * Otherwise, parameters are encoded as FormData for non-GET requests, or as a URL-encoded string for GET requests.
 *
 * @param {string} t - The HTTP method (e.g., "GET", "POST").
 * @param {Element} n - The source element initiating the request.
 * @param {object|FormData} r - The parameters to encode.
 * @returns {FormData|string} Encoded parameters suitable for the request type.
 */
function mn(t,n,r){let o=null;Ft(n,function(e){if(o==null){o=e.encodeParameters(t,r,n)}});if(o!=null){return o}else{if(pn(n)){return ln(new FormData,qn(r))}else{return an(r)}}}/**
 * Creates an object representing a processing context for a given element.
 *
 * The returned object contains a `tasks` array for tracking processing steps and an `elts` array initialized with the provided element.
 *
 * @param {Element} e - The root element for the processing context.
 * @returns {{tasks: Array, elts: Array<Element>}} An object with `tasks` and `elts` properties.
 */
function xn(e){return{tasks:[],elts:[e]}}/**
 * Adjusts scroll position and visibility of elements after a DOM update.
 *
 * Depending on the provided options, scrolls a target element or the first/last element in the list to the top or bottom, and optionally brings them into view.
 *
 * @param {Element[]} e - Array of elements affected by the DOM update.
 * @param {Object} t - Options controlling scroll and show behavior.
 * @remark
 * - If `t.scroll` is set, scrolls the target or first/last element to the specified position.
 * - If `t.show` is set, scrolls the target or first/last element into view with the configured scroll behavior.
 */
function yn(e,t){const n=e[0];const r=e[e.length-1];if(t.scroll){var o=null;if(t.scrollTarget){o=ue(ae(n,t.scrollTarget))}if(t.scroll==="top"&&(n||o)){o=o||n;o.scrollTop=0}if(t.scroll==="bottom"&&(r||o)){o=o||r;o.scrollTop=o.scrollHeight}}if(t.show){var o=null;if(t.showTarget){let e=t.showTarget;if(t.showTarget==="window"){e="body"}o=ue(ae(n,e))}if(t.show==="top"&&(n||o)){o=o||n;o.scrollIntoView({block:"start",behavior:Q.config.scrollBehavior})}if(t.show==="bottom"&&(r||o)){o=o||r;o.scrollIntoView({block:"end",behavior:Q.config.scrollBehavior})}}}/**
 * Recursively collects and merges configuration objects from the specified attribute on an element and its ancestors.
 *
 * If the attribute value starts with "js:" or "javascript:", it is evaluated as JavaScript; otherwise, it is parsed as JSON. Attribute values of "unset" return null. Later (closer) values override earlier ones unless already set in the accumulator.
 *
 * @param {Element} r - The starting element.
 * @param {string} e - The attribute name to search for.
 * @param {boolean} o - Whether to evaluate the attribute value as JavaScript.
 * @param {Object} [i={}] - Accumulator for merged configuration values.
 * @returns {Object|null} The merged configuration object, or null if "unset" is encountered.
 */
function bn(r,e,o,i){if(i==null){i={}}if(r==null){return i}const s=te(r,e);if(s){let e=s.trim();let t=o;if(e==="unset"){return null}if(e.indexOf("javascript:")===0){e=e.slice(11);t=true}else if(e.indexOf("js:")===0){e=e.slice(3);t=true}if(e.indexOf("{")!==0){e="{"+e+"}"}let n;if(t){n=vn(r,function(){return Function("return ("+e+")")()},{})}else{n=S(e)}for(const l in n){if(n.hasOwnProperty(l)){if(i[l]==null){i[l]=n[l]}}}}return bn(ue(c(r)),e,o,i)}/**
 * Executes a function if code evaluation is allowed by configuration; otherwise, triggers an error event and returns a fallback value.
 *
 * @param {Element} e - The element related to the evaluation context.
 * @param {Function} t - The function to execute if evaluation is permitted.
 * @param {*} n - The value to return if evaluation is disallowed.
 * @returns {*} The result of {@link t} if evaluation is allowed; otherwise, {@link n}.
 */
function vn(e,t,n){if(Q.config.allowEval){return t()}else{fe(e,"htmx:evalDisallowedError");return n}}/**
 * Retrieves the value of the `hx-vars` attribute from the specified element or its ancestors.
 *
 * @param {Element} e - The starting element for the search.
 * @param {Element} [t] - An optional ancestor element to limit the search scope.
 * @returns {string|null} The value of the `hx-vars` attribute if found, otherwise `null`.
 */
function wn(e,t){return bn(e,"hx-vars",true,t)}/**
 * Retrieves the value of the `hx-vals` attribute from the specified element.
 *
 * @param {Element} e - The element from which to retrieve the attribute.
 * @param {Element} [t] - An optional context element for attribute resolution.
 * @returns {string|null} The value of the `hx-vals` attribute, or `null` if not present.
 */
function Sn(e,t){return bn(e,"hx-vals",false,t)}/**
 * Serializes the values of a form or form-like element.
 *
 * @param {Element} e - The form or element whose values should be serialized.
 * @returns {Object} An object representing the serialized form values.
 */
function En(e){return ce(wn(e),Sn(e))}/**
 * Sets a request header on an XMLHttpRequest, automatically encoding the value if necessary.
 *
 * If setting the header fails (e.g., due to invalid characters), the value is URI-encoded and an additional header with the suffix "-URI-AutoEncoded" is set to "true".
 *
 * @param {XMLHttpRequest} t - The XMLHttpRequest instance.
 * @param {string} n - The name of the header to set.
 * @param {string|null} r - The value of the header. If null, the header is not set.
 */
function Cn(t,n,r){if(r!==null){try{t.setRequestHeader(n,r)}catch(e){t.setRequestHeader(n,encodeURIComponent(r));t.setRequestHeader(n+"-URI-AutoEncoded","true")}}}/**
 * Extracts the pathname and search components from an XMLHttpRequest's response URL.
 *
 * If the response URL is invalid, triggers the `htmx:badResponseUrl` event on the document body.
 *
 * @param {XMLHttpRequest} t - The XMLHttpRequest object containing the response URL.
 * @returns {string|undefined} The pathname and search string of the response URL, or `undefined` if unavailable.
 */
function On(t){if(t.responseURL&&typeof URL!=="undefined"){try{const e=new URL(t.responseURL);return e.pathname+e.search}catch(e){fe(ne().body,"htmx:badResponseUrl",{url:t.responseURL})}}}/**
 * Checks if the response headers of a given XMLHttpRequest match a specified regular expression.
 *
 * @param {XMLHttpRequest} e - The XMLHttpRequest object whose response headers are to be tested.
 * @param {RegExp} t - The regular expression to test against the response headers.
 * @returns {boolean} True if the response headers match the regular expression; otherwise, false.
 */
function R(e,t){return t.test(e.getAllResponseHeaders())}/**
 * Sends an AJAX request using the specified HTTP method and URL, with optional configuration for source, target, headers, values, and swap behavior.
 *
 * If a target or source element is provided, the request will be associated with that element; otherwise, a default element is used. Returns a Promise that resolves when the request completes.
 *
 * @param {string} t - The HTTP method to use (e.g., "GET", "POST").
 * @param {string} n - The URL to send the request to.
 * @param {Object|Element|string} [r] - Optional configuration object, target element, or selector string. If an object, may include `target`, `source`, `event`, `handler`, `headers`, `values`, `swap`, and `select`.
 * @returns {Promise} A Promise that resolves with the result of the AJAX request.
 */
function Rn(t,n,r){t=t.toLowerCase();if(r){if(r instanceof Element||typeof r==="string"){return de(t,n,null,null,{targetOverride:y(r)||ve,returnPromise:true})}else{let e=y(r.target);if(r.target&&!e||r.source&&!e&&!y(r.source)){e=ve}return de(t,n,y(r.source),r.event,{handler:r.handler,headers:r.headers,values:r.values,targetOverride:e,swapOverride:r.swap,select:r.select,returnPromise:true})}}else{return de(t,n,null,null,{returnPromise:true})}}/**
 * Returns an array of the given element and all its ancestor elements up to the root.
 *
 * @param {Element} e - The starting element.
 * @returns {Element[]} An array containing {@link e} and each of its ancestors, ordered from the closest ancestor to the farthest.
 */
function Hn(e){const t=[];while(e){t.push(e);e=e.parentElement}return t}/**
 * Validates a URL for use in an htmx request and triggers the `htmx:validateUrl` event.
 *
 * Determines if the provided URL is on the same origin as the current document and, if the `selfRequestsOnly` configuration is enabled, blocks requests to other origins. Dispatches the `htmx:validateUrl` event on the given element with details about the URL and its origin status.
 *
 * @param {Element} e - The element on which to dispatch the validation event.
 * @param {string} t - The URL to validate.
 * @param {Object} [n] - Additional event detail to merge into the event payload.
 * @returns {boolean} Returns `false` if the URL is not allowed by configuration; otherwise, returns the result of the event dispatch.
 */
function Tn(e,t,n){let r;let o;if(typeof URL==="function"){o=new URL(t,document.location.href);const i=document.location.origin;r=i===o.origin}else{o=t;r=l(t,document.location.origin)}if(Q.config.selfRequestsOnly){if(!r){return false}}return he(e,"htmx:validateUrl",ce({url:o,sameHost:r},n))}/**
 * Converts an object or array of values into a FormData instance.
 *
 * If the input is already a FormData object, it is returned as-is. For plain objects, array values are appended for each entry, objects (excluding Blob) are stringified, and other values are appended directly.
 *
 * @param {Object|FormData} e - The data to convert to FormData.
 * @returns {FormData} A FormData instance containing the input data.
 */
function qn(e){if(e instanceof FormData)return e;const t=new FormData;for(const n in e){if(e.hasOwnProperty(n)){if(e[n]&&typeof e[n].forEach==="function"){e[n].forEach(function(e){t.append(n,e)})}else if(typeof e[n]==="object"&&!(e[n]instanceof Blob)){t.append(n,JSON.stringify(e[n]))}else{t.append(n,e[n])}}}return t}/**
 * Wraps a FormData object with a Proxy to provide array-like access and automatic synchronization.
 *
 * The returned Proxy allows direct access to FormData entries by index, supports array methods, and ensures that any modifications to the underlying array are reflected in the FormData instance.
 *
 * @param {FormData} r - The FormData instance to synchronize with.
 * @param {string} o - The field name associated with the FormData entries.
 * @param {Array} e - The array of values to proxy.
 * @returns {Proxy} A Proxy that provides array-like access and keeps the FormData in sync with the array.
 */
function Ln(r,o,e){return new Proxy(e,{get:function(t,e){if(typeof e==="number")return t[e];if(e==="length")return t.length;if(e==="push"){return function(e){t.push(e);r.append(o,e)}}if(typeof t[e]==="function"){return function(){t[e].apply(t,arguments);r.delete(o);t.forEach(function(e){r.append(o,e)})}}if(t[e]&&t[e].length===1){return t[e][0]}else{return t[e]}},set:function(e,t,n){e[t]=n;r.delete(o);e.forEach(function(e){r.append(o,e)});return true}})}/**
 * Wraps a FormData object with a Proxy to provide convenient property-style access to its entries.
 *
 * Allows accessing form fields as properties, automatically handling multiple values and JSON serialization.
 *
 * @param {FormData} o - The FormData object to wrap.
 * @returns {Proxy} A Proxy that enables property-style access and manipulation of the FormData entries.
 *
 * @remark
 * - Accessing a property returns its value, an array of values if multiple exist, or `undefined` if not present.
 * - Setting a property serializes objects (except Blob) as JSON.
 * - The `toJSON` method returns a plain object representation of the FormData.
 */
function An(o){return new Proxy(o,{get:function(e,t){if(typeof t==="symbol"){const r=Reflect.get(e,t);if(typeof r==="function"){return function(){return r.apply(o,arguments)}}else{return r}}if(t==="toJSON"){return()=>Object.fromEntries(o)}if(t in e){if(typeof e[t]==="function"){return function(){return o[t].apply(o,arguments)}}else{return e[t]}}const n=o.getAll(t);if(n.length===0){return undefined}else if(n.length===1){return n[0]}else{return Ln(e,t,n)}},set:function(t,n,e){if(typeof n!=="string"){return false}t.delete(n);if(e&&typeof e.forEach==="function"){e.forEach(function(e){t.append(n,e)})}else if(typeof e==="object"&&!(e instanceof Blob)){t.append(n,JSON.stringify(e))}else{t.append(n,e)}return true},deleteProperty:function(e,t){if(typeof t==="string"){e.delete(t)}return true},ownKeys:function(e){return Reflect.ownKeys(Object.fromEntries(e))},getOwnPropertyDescriptor:function(e,t){return Reflect.getOwnPropertyDescriptor(Object.fromEntries(e),t)}})}/**
 * Sends an AJAX request based on the provided HTTP method, URL, source element, triggering event, and options, then processes the server response and updates the DOM accordingly.
 *
 * Handles request queuing, aborting, and synchronization via `hx-sync`, supports confirmation and prompt dialogs, manages form data serialization and validation, and dispatches lifecycle events for customization and error handling. Integrates with browser history and supports boosted navigation, custom headers, and extensions.
 *
 * @param {string} t - The HTTP method to use (e.g., "GET", "POST").
 * @param {string} n - The request URL.
 * @param {Element} r - The source element initiating the request.
 * @param {Event} [o] - The event that triggered the request, if any.
 * @param {Object} [i] - Additional options for the request, such as headers, credentials, timeout, and custom handlers.
 * @param {boolean} [D] - Internal flag for confirmation handling.
 * @returns {Promise|undefined} A Promise that resolves or rejects when `returnPromise` is set in options; otherwise, returns undefined.
 *
 * @throws {Error} If an error occurs during the onload handler after a successful response.
 *
 * @remark
 * If the request is blocked by validation errors, confirmation dialogs, prompt dialogs, or synchronization rules, the returned Promise (if any) will be rejected and no request will be sent.
 */
function de(t,n,r,o,i,D){let s=null;let l=null;i=i!=null?i:{};if(i.returnPromise&&typeof Promise!=="undefined"){var e=new Promise(function(e,t){s=e;l=t})}if(r==null){r=ne().body}const M=i.handler||Dn;const X=i.select||null;if(!le(r)){oe(s);return e}const c=i.targetOverride||ue(Ee(r));if(c==null||c==ve){fe(r,"htmx:targetError",{target:te(r,"hx-target")});oe(l);return e}let u=ie(r);const a=u.lastButtonClicked;if(a){const L=ee(a,"formaction");if(L!=null){n=L}const A=ee(a,"formmethod");if(A!=null){if(A.toLowerCase()!=="dialog"){t=A}}}const f=re(r,"hx-confirm");if(D===undefined){const K=function(e){return de(t,n,r,o,i,!!e)};const G={target:c,elt:r,path:n,verb:t,triggeringEvent:o,etc:i,issueRequest:K,question:f};if(he(r,"htmx:confirm",G)===false){oe(s);return e}}let h=r;let d=re(r,"hx-sync");let g=null;let F=false;if(d){const N=d.split(":");const I=N[0].trim();if(I==="this"){h=Se(r,"hx-sync")}else{h=ue(ae(r,I))}d=(N[1]||"drop").trim();u=ie(h);if(d==="drop"&&u.xhr&&u.abortable!==true){oe(s);return e}else if(d==="abort"){if(u.xhr){oe(s);return e}else{F=true}}else if(d==="replace"){he(h,"htmx:abort")}else if(d.indexOf("queue")===0){const W=d.split(" ");g=(W[1]||"last").trim()}}if(u.xhr){if(u.abortable){he(h,"htmx:abort")}else{if(g==null){if(o){const P=ie(o);if(P&&P.triggerSpec&&P.triggerSpec.queue){g=P.triggerSpec.queue}}if(g==null){g="last"}}if(u.queuedRequests==null){u.queuedRequests=[]}if(g==="first"&&u.queuedRequests.length===0){u.queuedRequests.push(function(){de(t,n,r,o,i)})}else if(g==="all"){u.queuedRequests.push(function(){de(t,n,r,o,i)})}else if(g==="last"){u.queuedRequests=[];u.queuedRequests.push(function(){de(t,n,r,o,i)})}oe(s);return e}}const p=new XMLHttpRequest;u.xhr=p;u.abortable=F;const m=function(){u.xhr=null;u.abortable=false;if(u.queuedRequests!=null&&u.queuedRequests.length>0){const e=u.queuedRequests.shift();e()}};const B=re(r,"hx-prompt");if(B){var x=prompt(B);if(x===null||!he(r,"htmx:prompt",{prompt:x,target:c})){oe(s);m();return e}}if(f&&!D){if(!confirm(f)){oe(s);m();return e}}let y=fn(r,c,x);if(t!=="get"&&!pn(r)){y["Content-Type"]="application/x-www-form-urlencoded"}if(i.headers){y=ce(y,i.headers)}const U=cn(r,t);let b=U.errors;const j=U.formData;if(i.values){ln(j,qn(i.values))}const V=qn(En(r));const v=ln(j,V);let w=hn(v,r);if(Q.config.getCacheBusterParam&&t==="get"){w.set("org.htmx.cache-buster",ee(c,"id")||"true")}if(n==null||n===""){n=ne().location.href}const S=bn(r,"hx-request");const _=ie(r).boosted;let E=Q.config.methodsThatUseUrlParams.indexOf(t)>=0;const C={boosted:_,useUrlParams:E,formData:w,parameters:An(w),unfilteredFormData:v,unfilteredParameters:An(v),headers:y,target:c,verb:t,errors:b,withCredentials:i.credentials||S.credentials||Q.config.withCredentials,timeout:i.timeout||S.timeout||Q.config.timeout,path:n,triggeringEvent:o};if(!he(r,"htmx:configRequest",C)){oe(s);m();return e}n=C.path;t=C.verb;y=C.headers;w=qn(C.parameters);b=C.errors;E=C.useUrlParams;if(b&&b.length>0){he(r,"htmx:validation:halted",C);oe(s);m();return e}const z=n.split("#");const $=z[0];const O=z[1];let R=n;if(E){R=$;const Z=!w.keys().next().done;if(Z){if(R.indexOf("?")<0){R+="?"}else{R+="&"}R+=an(w);if(O){R+="#"+O}}}if(!Tn(r,R,C)){fe(r,"htmx:invalidPath",C);oe(l);return e}p.open(t.toUpperCase(),R,true);p.overrideMimeType("text/html");p.withCredentials=C.withCredentials;p.timeout=C.timeout;if(S.noHeaders){}else{for(const k in y){if(y.hasOwnProperty(k)){const Y=y[k];Cn(p,k,Y)}}}const H={xhr:p,target:c,requestConfig:C,etc:i,boosted:_,select:X,pathInfo:{requestPath:n,finalRequestPath:R,responsePath:null,anchor:O}};p.onload=function(){try{const t=Hn(r);H.pathInfo.responsePath=On(p);M(r,H);if(H.keepIndicators!==true){Qt(T,q)}he(r,"htmx:afterRequest",H);he(r,"htmx:afterOnLoad",H);if(!le(r)){let e=null;while(t.length>0&&e==null){const n=t.shift();if(le(n)){e=n}}if(e){he(e,"htmx:afterRequest",H);he(e,"htmx:afterOnLoad",H)}}oe(s);m()}catch(e){fe(r,"htmx:onLoadError",ce({error:e},H));throw e}};p.onerror=function(){Qt(T,q);fe(r,"htmx:afterRequest",H);fe(r,"htmx:sendError",H);oe(l);m()};p.onabort=function(){Qt(T,q);fe(r,"htmx:afterRequest",H);fe(r,"htmx:sendAbort",H);oe(l);m()};p.ontimeout=function(){Qt(T,q);fe(r,"htmx:afterRequest",H);fe(r,"htmx:timeout",H);oe(l);m()};if(!he(r,"htmx:beforeRequest",H)){oe(s);m();return e}var T=Zt(r);var q=Yt(r);se(["loadstart","loadend","progress","abort"],function(t){se([p,p.upload],function(e){e.addEventListener(t,function(e){he(r,"htmx:xhr:"+t,{lengthComputable:e.lengthComputable,loaded:e.loaded,total:e.total})})})});he(r,"htmx:beforeSend",H);const J=E?null:mn(p,r,w);p.send(J);return e}/**
 * Determines the appropriate browser history update action and URL based on response headers and element attributes.
 *
 * Examines the XMLHttpRequest response headers (`HX-Push`, `HX-Push-Url`, `HX-Replace-Url`) and the triggering element's `hx-push-url` or `hx-replace-url` attributes to decide whether to push or replace a URL in the browser history. Returns an object specifying the action type (`push` or `replace`) and the target path, or an empty object if no history update is needed.
 *
 * @param {Element} e - The element that triggered the request.
 * @param {Object} t - The request context, containing the `xhr` object and `pathInfo`.
 * @returns {Object} An object with `type` (`"push"` or `"replace"`) and `path` properties if a history update is required, or an empty object otherwise.
 */
function Nn(e,t){const n=t.xhr;let r=null;let o=null;if(R(n,/HX-Push:/i)){r=n.getResponseHeader("HX-Push");o="push"}else if(R(n,/HX-Push-Url:/i)){r=n.getResponseHeader("HX-Push-Url");o="push"}else if(R(n,/HX-Replace-Url:/i)){r=n.getResponseHeader("HX-Replace-Url");o="replace"}if(r){if(r==="false"){return{}}else{return{type:o,path:r}}}const i=t.pathInfo.finalRequestPath;const s=t.pathInfo.responsePath;const l=re(e,"hx-push-url");const c=re(e,"hx-replace-url");const u=ie(e).boosted;let a=null;let f=null;if(l){a="push";f=l}else if(c){a="replace";f=c}else if(u){a="push";f=s||i}if(f){if(f==="false"){return{}}if(f==="true"){f=s||i}if(t.pathInfo.anchor&&f.indexOf("#")===-1){f=f+"#"+t.pathInfo.anchor}return{type:a,path:f}}else{return{}}}/**
 * Tests whether a given value matches a regular expression pattern defined by {@link e.code}.
 *
 * @param {Object} e - An object containing a `code` property representing a regular expression pattern.
 * @param {number|string} t - The value to test, which will be converted to a string.
 * @returns {boolean} True if the string representation of {@link t} matches the pattern; otherwise, false.
 */
function In(e,t){var n=new RegExp(e.code);return n.test(t.toString(10))}/**
 * Returns the response handling configuration matching the given HTTP status code.
 *
 * If no matching configuration is found, returns an object with `swap: false`.
 *
 * @param {Object} e - The XMLHttpRequest or response object containing a `status` property.
 * @returns {Object} The response handling configuration for the status code, or `{swap: false}` if none matches.
 */
function Pn(e){for(var t=0;t<Q.config.responseHandling.length;t++){var n=Q.config.responseHandling[t];if(In(n,e.status)){return n}}return{swap:false}}/**
 * Sets the document title to the specified value.
 *
 * If a <title> element exists, its content is updated; otherwise, the window's document title is set directly.
 *
 * @param {string} e - The new title for the document.
 */
function kn(e){if(e){const t=u("title");if(t){t.innerHTML=e}else{window.document.title=e}}}/**
 * Handles the processing of an AJAX response, including interpreting special HX-* headers, managing redirects, refreshes, retargeting, and performing DOM swaps.
 *
 * This function is responsible for the main response lifecycle after an XMLHttpRequest completes. It interprets server-sent HX-* headers to control client-side behavior such as location changes, redirects, refreshes, retargeting, and swap strategies. It triggers relevant htmx events, manages history state, and performs DOM updates or swaps as specified by the response and configuration.
 *
 * @param {Element} o - The source element that initiated the request.
 * @param {Object} i - The context object containing the XMLHttpRequest (`xhr`), target element, and additional request/response metadata.
 *
 * @remark
 * - May trigger a full page reload or redirect if instructed by HX-Refresh or HX-Redirect headers.
 * - Handles out-of-band swaps, custom swap strategies, and history updates as specified by the server response.
 */
function Dn(o,i){const s=i.xhr;let l=i.target;const e=i.etc;const c=i.select;if(!he(o,"htmx:beforeOnLoad",i))return;if(R(s,/HX-Trigger:/i)){Je(s,"HX-Trigger",o)}if(R(s,/HX-Location:/i)){zt();let e=s.getResponseHeader("HX-Location");var t;if(e.indexOf("{")===0){t=S(e);e=t.path;delete t.path}Rn("get",e,t).then(function(){$t(e)});return}const n=R(s,/HX-Refresh:/i)&&s.getResponseHeader("HX-Refresh")==="true";if(R(s,/HX-Redirect:/i)){i.keepIndicators=true;location.href=s.getResponseHeader("HX-Redirect");n&&location.reload();return}if(n){i.keepIndicators=true;location.reload();return}if(R(s,/HX-Retarget:/i)){if(s.getResponseHeader("HX-Retarget")==="this"){i.target=o}else{i.target=ue(ae(o,s.getResponseHeader("HX-Retarget")))}}const u=Nn(o,i);const r=Pn(s);const a=r.swap;let f=!!r.error;let h=Q.config.ignoreTitle||r.ignoreTitle;let d=r.select;if(r.target){i.target=ue(ae(o,r.target))}var g=e.swapOverride;if(g==null&&r.swapOverride){g=r.swapOverride}if(R(s,/HX-Retarget:/i)){if(s.getResponseHeader("HX-Retarget")==="this"){i.target=o}else{i.target=ue(ae(o,s.getResponseHeader("HX-Retarget")))}}if(R(s,/HX-Reswap:/i)){g=s.getResponseHeader("HX-Reswap")}var p=s.response;var m=ce({shouldSwap:a,serverResponse:p,isError:f,ignoreTitle:h,selectOverride:d,swapOverride:g},i);if(r.event&&!he(l,r.event,m))return;if(!he(l,"htmx:beforeSwap",m))return;l=m.target;p=m.serverResponse;f=m.isError;h=m.ignoreTitle;d=m.selectOverride;g=m.swapOverride;i.target=l;i.failed=f;i.successful=!f;if(m.shouldSwap){if(s.status===286){lt(o)}Ft(o,function(e){p=e.transformResponse(p,s,o)});if(u.type){zt()}var x=gn(o,g);if(!x.hasOwnProperty("ignoreTitle")){x.ignoreTitle=h}l.classList.add(Q.config.swappingClass);let n=null;let r=null;if(c){d=c}if(R(s,/HX-Reselect:/i)){d=s.getResponseHeader("HX-Reselect")}const y=re(o,"hx-select-oob");const b=re(o,"hx-select");let e=function(){try{if(u.type){he(ne().body,"htmx:beforeHistoryUpdate",ce({history:u},i));if(u.type==="push"){$t(u.path);he(ne().body,"htmx:pushedIntoHistory",{path:u.path})}else{Jt(u.path);he(ne().body,"htmx:replacedInHistory",{path:u.path})}}$e(l,p,x,{select:d||b,selectOOB:y,eventInfo:i,anchor:i.pathInfo.anchor,contextElement:o,afterSwapCallback:function(){if(R(s,/HX-Trigger-After-Swap:/i)){let e=o;if(!le(o)){e=ne().body}Je(s,"HX-Trigger-After-Swap",e)}},afterSettleCallback:function(){if(R(s,/HX-Trigger-After-Settle:/i)){let e=o;if(!le(o)){e=ne().body}Je(s,"HX-Trigger-After-Settle",e)}oe(n)}})}catch(e){fe(o,"htmx:swapError",i);oe(r);throw e}};let t=Q.config.globalViewTransitions;if(x.hasOwnProperty("transition")){t=x.transition}if(t&&he(o,"htmx:beforeTransition",i)&&typeof Promise!=="undefined"&&document.startViewTransition){const v=new Promise(function(e,t){n=e;r=t});const w=e;e=function(){document.startViewTransition(function(){w();return v})}}if(x.swapDelay>0){E().setTimeout(e,x.swapDelay)}else{e()}}if(f){fe(o,"htmx:responseError",ce({error:"Response Status Error Code "+s.status+" from "+i.pathInfo.requestPath},i))}}const Mn={};/**
 * Provides a default extension implementation with no-op behaviors for all extension hooks.
 *
 * This object can be used as a base or placeholder for extension lifecycle methods, ensuring that all required hooks are present with default behavior.
 *
 * @returns {object} An extension object with default implementations for all extension hooks.
 */
function Xn(){return{init:function(e){return null},getSelectors:function(){return null},onEvent:function(e,t){return true},transformResponse:function(e,t,n){return e},isInlineSwap:function(e){return false},handleSwap:function(e,t,n,r){return false},encodeParameters:function(e,t,n){return null}}}/**
 * Registers an extension under the specified name and initializes it if an `init` method is present.
 *
 * @param {string} e - The name of the extension.
 * @param {object} t - The extension object, which may include an `init` method.
 */
function Fn(e,t){if(t.init){t.init(n)}Mn[e]=ce(Xn(),t)}/**
 * Removes a previously defined extension by its name.
 *
 * @param {string} e - The name of the extension to remove.
 */
function Bn(e){delete Mn[e]}/**
 * Collects all applicable extension objects for an element and its ancestors.
 *
 * Traverses up the DOM tree from the given element, gathering extension objects specified by the `hx-ext` attribute, while skipping extensions marked with the `ignore:` prefix.
 *
 * @param {Element} e - The starting element for extension collection.
 * @returns {Array} An array of extension objects applied to the element and its ancestors.
 */
function Un(e,n,r){if(n==undefined){n=[]}if(e==undefined){return n}if(r==undefined){r=[]}const t=te(e,"hx-ext");if(t){se(t.split(","),function(e){e=e.replace(/ /g,"");if(e.slice(0,7)=="ignore:"){r.push(e.slice(7));return}if(r.indexOf(e)<0){const t=Mn[e];if(t&&n.indexOf(t)<0){n.push(t)}}})}return Un(ue(c(e)),n,r)}var jn=false;ne().addEventListener("DOMContentLoaded",function(){jn=true});/**
 * Executes a callback after the DOM is fully loaded.
 *
 * If the document is already loaded, the callback is invoked immediately; otherwise, it is scheduled to run on the `DOMContentLoaded` event.
 *
 * @param {Function} e - The callback function to execute when the DOM is ready.
 */
function Vn(e){if(jn||ne().readyState==="complete"){e()}else{ne().addEventListener("DOMContentLoaded",e)}}/**
 * Injects default indicator CSS styles into the document head if enabled in the configuration.
 *
 * Adds styles for the indicator and request classes used by htmx to visually indicate AJAX activity.
 * If a nonce is specified in the configuration, it is included on the style tag for CSP compliance.
 *
 * @remark No styles are injected if {@link Q.config.includeIndicatorStyles} is set to `false`.
 */
function _n(){if(Q.config.includeIndicatorStyles!==false){const e=Q.config.inlineStyleNonce?` nonce="${Q.config.inlineStyleNonce}"`:"";ne().head.insertAdjacentHTML("beforeend","<style"+e+">      ."+Q.config.indicatorClass+"{opacity:0}      ."+Q.config.requestClass+" ."+Q.config.indicatorClass+"{opacity:1; transition: opacity 200ms ease-in;}      ."+Q.config.requestClass+"."+Q.config.indicatorClass+"{opacity:1; transition: opacity 200ms ease-in;}      </style>")}}/**
 * Retrieves and parses the content of the first &lt;meta name="htmx-config"&gt; tag in the main document.
 *
 * @returns {object|null} The parsed configuration object if the meta tag exists, or {@code null} if not found.
 */
function zn(){const e=ne().querySelector('meta[name="htmx-config"]');if(e){return S(e.content)}else{return null}}/**
 * Loads persisted configuration settings and merges them into the current configuration.
 *
 * If stored configuration exists, it overrides the corresponding properties in {@link Q.config}.
 */
function $n(){const e=zn();if(e){Q.config=ce(Q.config,e)}}Vn(function(){$n();_n();let e=ne().body;kt(e);const t=ne().querySelectorAll("[hx-trigger='restored'],[data-hx-trigger='restored']");e.addEventListener("htmx:abort",function(e){const t=e.target;const n=ie(t);if(n&&n.xhr){n.xhr.abort()}});const n=window.onpopstate?window.onpopstate.bind(window):null;window.onpopstate=function(e){if(e.state&&e.state.htmx){Wt();se(t,function(e){he(e,"htmx:restored",{document:ne(),triggerEvent:he})})}else{if(n){n(e)}}};E().setTimeout(function(){he(e,"htmx:load",{});e=null},0)});return Q}();
---
title: Daedalus String (`dString_t`) Documentation
created: 2025-07-11
tags: 
  - C
  - strings
  - game development
  - Daedalus
---
# Daedalus String (`dString_t`) Documentation

This document will guide you through the core `dString_t` structure and its essential functions, providing quick examples to get you started.

---

## Core Structure and Initialization

The heart of the `dString_t` library is its main structure and the function used to create new instances.

### `dString_t` Structure

The `dString_t` structure encapsulates all the necessary information for a dynamic string:

```c
typedef struct {
    char* str;      /**< The actual string buffer */
    size_t  alloced;  /**< Total allocated memory in bytes for str */
    size_t  len;      /**< Current string length, excluding null terminator */
} dString_t;
```

{~ parameter_v1 name="str" type="char*" ~}
A pointer to the dynamically allocated character array that holds the string data.
{~~}

{~ parameter_v1 name="alloced" type="size_t" ~}
The total number of bytes currently allocated for the `str` buffer.
{~~}

{~ parameter_v1 name="len" type="size_t" ~}
The current length of the string stored in `str`, *excluding* the null terminator.
{~~}

* **`str`**: A pointer to the dynamically allocated character array that holds the string data.
* **`alloced`**: The total number of bytes currently allocated for the `str` buffer. This represents the capacity.
* **`len`**: The current length of the string stored in `str`, *excluding* the null terminator.

The library also defines a minimum initial size for the string buffer:

```c
static const size_t d_string_builder_min_size = 32;
```

### `d_InitString`

@brief Create a new string builder.

**Signature:**

```c
dString_t* d_InitString(void);
```

**Description:**
This function allocates and initializes a new `dString_t` structure and its internal character buffer. The initial capacity is `d_string_builder_min_size` (32 bytes), but it will automatically grow as needed. You *must* call `d_DestroyString` on the returned pointer when you are done with it to prevent memory leaks.

**Returns:**
A pointer to the newly created `dString_t` instance, or `NULL` if memory allocation fails.

**Example:**

```c
dString_t* my_string = d_InitString();
if (my_string == NULL) {
    // Handle error: memory allocation failed
    fprintf(stderr, "Failed to create dString_t!\n");
    return 1;
}
// ... use my_string ...
d_DestroyString(my_string); // Remember to free!
```

### `d_DestroyString`

@brief Destroy a string builder and free its memory.

**Signature:**

```c
void d_DestroyString(dString_t* sb);
```

**Description:**
This function deallocates all memory associated with a `dString_t` instance, including its internal character buffer and the `dString_t` struct itself. After calling this function, the `sb` pointer becomes invalid and should not be used. Calling with a `NULL` pointer is safe and does nothing.

**Parameters:**

* `sb`: Pointer to the `dString_t` to destroy.

**Example:**

```c
dString_t* my_string = d_InitString();
// ... use my_string ...
d_DestroyString(my_string); // Clean up allocated memory
my_string = NULL;          // Good practice to nullify pointer after freeing
```

---

## Appending Content

These functions allow you to add various types of data to the string builder.

### `d_AppendToString`

@brief Add a C string to the string builder.

**Signature:**

```c
void d_AppendToString(dString_t* sb, const char* str, size_t len);
```

**Description:**
Appends a C-style string (`str`) to the current content of the `dString_t`. If `len` is `0`, the function calculates the length of `str` using `strlen()`. If `len` is greater than `0`, exactly `len` characters from `str` are copied. This function handles automatic memory reallocation if the current buffer is too small. It's safe to append a string that overlaps with the builder's own internal buffer (self-append).

**Parameters:**

* `sb`: The string builder to append to.
* `str`: The source C-string to append. Must be null-terminated if `len` is `0`.
* `len`: The number of characters to append from `str`. Pass `0` to append the entire null-terminated string.

**Example:**

```c
dString_t* message = d_InitString();
d_AppendToString(message, "Hello, ", 0);
d_AppendToString(message, "world!", 0);
printf("%s\n", d_PeekString(message)); // Output: Hello, world!
d_DestroyString(message);
```

### `d_AppendToStringN`

@brief Append a C string to the string builder, up to a maximum length.

**Signature:**

```c
void d_AppendToStringN(dString_t* sb, const char* str, size_t max_len);
```

**Description:**
Appends characters from a C-style string (`str`) to the `dString_t`, but will copy at most `max_len` characters or until a null terminator is encountered in `str`, whichever comes first. This is useful for appending from buffers that might not be null-terminated or for copying only a prefix of a string.

**Parameters:**

* `sb`: The string builder to append to.
* `str`: The source C-string to append from.
* `max_len`: The maximum number of characters to copy from `str`.

**Example:**

```c
dString_t* prefix = d_InitString();
const char* long_text = "This is a very long sentence.";
d_AppendToStringN(prefix, long_text, 7); // Appends "This is"
printf("%s\n", d_PeekString(prefix)); // Output: This is
d_DestroyString(prefix);
```

### `d_AppendCharToString`

@brief Add a single character to the string builder.

**Signature:**

```c
void d_AppendCharToString(dString_t* sb, char c);
```

**Description:**
Appends a single character (`c`) to the end of the string builder's content. Automatic memory reallocation is handled if needed.

**Parameters:**

* `sb`: The string builder to append to.
* `c`: The character to append.

**Example:**

```c
dString_t* path = d_InitString();
d_AppendToString(path, "/usr", 0);
d_AppendCharToString(path, '/');
d_AppendToString(path, "local", 0);
printf("%s\n", d_PeekString(path)); // Output: /usr/local
d_DestroyString(path);
```

### `d_AppendIntToString`

@brief Add an integer to the string builder as a decimal string.

**Signature:**

```c
void d_AppendIntToString(dString_t* sb, int val);
```

**Description:**
Converts an integer value (`val`) to its decimal string representation and appends it to the `dString_t`. This function internally uses `snprintf` for safe conversion.

**Parameters:**

* `sb`: The string builder to append to.
* `val`: The integer value to append.

**Example:**

```c
dString_t* score_msg = d_InitString();
d_AppendToString(score_msg, "Score: ", 0);
d_AppendIntToString(score_msg, 12345);
printf("%s\n", d_PeekString(score_msg)); // Output: Score: 12345
d_DestroyString(score_msg);
```

### `d_AppendFloatToString`

@brief Add a floating-point number to the string builder.

**Signature:**

```c
void d_AppendFloatToString(dString_t* sb, float val, int decimals);
```

**Description:**
Converts a floating-point value (`val`) to its string representation and appends it to the `dString_t`. The `decimals` parameter controls the number of digits after the decimal point (clamped between 0 and 10 for safety).

**Parameters:**

* `sb`: The string builder to append to.
* `val`: The floating-point value to append.
* `decimals`: The number of decimal places to include in the string (e.g., `2` for `3.14`).

**Example:**

```c
dString_t* price_tag = d_InitString();
d_AppendToString(price_tag, "Price: $", 0);
d_AppendFloatToString(price_tag, 19.99f, 2);
printf("%s\n", d_PeekString(price_tag)); // Output: Price: $19.99
d_DestroyString(price_tag);
```

---

## String Manipulation

These functions allow you to modify the content of an existing `dString_t`.

### `d_SetString`

@brief Set the content of an existing `dString_t` to a new value.

**Signature:**

```c
int d_SetString(dString_t* string, const char* content, int flags);
```

**Description:**
Replaces the entire content of the `dString_t` with the provided `content` string. If `content` is `NULL`, the string builder is cleared. If the `content` is identical to the current string, no operation is performed. This function handles necessary memory reallocations. The `flags` parameter is currently unused but reserved for future extensions.

**Parameters:**

* `string`: Pointer to the `dString_t` structure to modify.
* `content`: The new C-string content to copy into the `dString_t`.
* `flags`: Optional flags (currently unused, pass `0`).

**Returns:**
`0` on success, `-1` on error (e.g., null `dString_t` pointer or memory allocation failure).

**Example:**

```c
dString_t* status = d_InitString();
d_SetString(status, "Loading...", 0);
printf("Status: %s\n", d_PeekString(status)); // Output: Status: Loading...
d_SetString(status, "Game Ready!", 0);
printf("Status: %s\n", d_PeekString(status)); // Output: Status: Game Ready!
d_DestroyString(status);
```

### `d_ClearString`

@brief Clear the string builder content.

**Signature:**

```c
void d_ClearString(dString_t* sb);
```

**Description:**
Resets the `dString_t` to an empty string (`""`). This operation sets the length to `0` and places a null terminator at the beginning of the buffer. It does *not* deallocate the internal memory, allowing for efficient reuse of the buffer.

**Parameters:**

* `sb`: The string builder to clear.

**Example:**

```c
dString_t* temp_log = d_InitString();
d_AppendToString(temp_log, "First entry.", 0);
printf("Temp Log: %s\n", d_PeekString(temp_log)); // Output: Temp Log: First entry.
d_ClearString(temp_log);
printf("Temp Log (cleared): '%s'\n", d_PeekString(temp_log)); // Output: Temp Log (cleared): ''
d_DestroyString(temp_log);
```

### `d_TruncateString`

@brief Truncate the string builder to a specific length.

**Signature:**

```c
void d_TruncateString(dString_t* sb, size_t len);
```

**Description:**
Shortens the string builder's content to the specified `len`. If `len` is less than the current length, the string is truncated, and a null terminator is placed at the new `len` position. If `len` is greater than or equal to the current length, no action is taken. This function does *not* free memory.

**Parameters:**

* `sb`: Pointer to the string builder.
* `len`: The new desired length. Must be less than or equal to the current length.

**Example:**

```c
dString_t* full_name = d_InitString();
d_AppendToString(full_name, "Mathew Storm", 0);
printf("Full Name: %s\n", d_PeekString(full_name)); // Output: Full Name: Mathew Storm
d_TruncateString(full_name, 6); // Truncate to "Mathew"
printf("Short Name: %s\n", d_PeekString(full_name)); // Output: Short Name: Mathew
d_DestroyString(full_name);
```

### `d_DropString`

@brief Remove characters from the beginning of the string builder.

**Signature:**

```c
void d_DropString(dString_t* sb, size_t len);
```

**Description:**
Removes `len` characters from the beginning of the string builder's content. The remaining characters are shifted to the start of the buffer. If `len` is greater than or equal to the current string length, the string builder is cleared entirely.

**Parameters:**

* `sb`: Pointer to the string builder.
* `len`: The number of characters to remove from the beginning.

**Example:**

```c
dString_t* log_entry = d_InitString();
d_AppendToString(log_entry, "[DEBUG] Initializing...", 0);
printf("Original: %s\n", d_PeekString(log_entry)); // Output: Original: [DEBUG] Initializing...
d_DropString(log_entry, 7); // Drop "[DEBUG]"
printf("Dropped: %s\n", d_PeekString(log_entry)); // Output: Dropped:  Initializing...
d_DestroyString(log_entry);
```

### `d_CloneString`

@brief Create a new string builder with the same content as another string.

**Signature:**

```c
dString_t* d_CloneString(const dString_t* source);
```

**Description:**
Creates a brand new `dString_t` instance and copies the content from the `source` `dString_t` into it. This results in an independent copy. The caller is responsible for destroying the returned `dString_t` using `d_DestroyString`.

**Parameters:**

* `source`: The `dString_t` to copy content from.

**Returns:**
A new `dString_t` with the cloned content, or `NULL` on error (e.g., null source or memory allocation failure).

**Example:**

```c
dString_t* original = d_InitString();
d_AppendToString(original, "Original Data", 0);
dString_t* cloned = d_CloneString(original);

if (cloned != NULL) {
    printf("Original: %s\n", d_PeekString(original)); // Output: Original: Original Data
    printf("Cloned: %s\n", d_PeekString(cloned));     // Output: Cloned: Original Data
    d_DestroyString(cloned); // Remember to free the clone!
}
d_DestroyString(original);
```

---

## Accessing String Content

These functions allow you to retrieve the content or properties of the `dString_t`.

### `d_GetLengthOfString`

@brief Get the current length of the string builder content.

**Signature:**

```c
size_t d_GetLengthOfString(const dString_t* sb);
```

**Description:**
Returns the current length of the string stored in the `dString_t`, excluding the null terminator. This is an efficient operation as the length is always tracked internally.

**Parameters:**

* `sb`: Pointer to the string builder.

**Returns:**
The current length in characters, or `0` if `sb` is `NULL`.

**Example:**

```c
dString_t* my_str = d_InitString();
d_AppendToString(my_str, "Hello", 0);
printf("Length: %zu\n", d_GetLengthOfString(my_str)); // Output: Length: 5
d_DestroyString(my_str);
```

### `d_PeekString`

@brief Get a read-only pointer to the string builder's content.

**Signature:**

```c
const char* d_PeekString(const dString_t* sb);
```

**Description:**
Returns a `const char*` pointer to the internal character buffer of the `dString_t`. This provides direct, read-only access to the string data without making a copy. The returned pointer is guaranteed to be null-terminated.

**Important Notes:**

* **Do not modify** the string content through this pointer.
* **Do not `free()`** the returned pointer.
* The pointer becomes **invalid** if any function that modifies the `dString_t` (e.g., `d_AppendToString`, `d_SetString`, `d_TruncateString`) is called, as these operations might reallocate the internal buffer. Use this for immediate, short-lived access.

**Parameters:**

* `sb`: Pointer to the string builder.

**Returns:**
A `const char*` pointer to the internal string, or `NULL` if `sb` is `NULL`.

**Example:**

```c
dString_t* greeting = d_InitString();
d_AppendToString(greeting, "Greetings!", 0);
const char* c_str_greeting = d_PeekString(greeting);
printf("Message: %s\n", c_str_greeting); // Safe to use for printing

// d_AppendToString(greeting, " from Daedalus", 0); // This would invalidate c_str_greeting!
// printf("New Message: %s\n", c_str_greeting); // DANGER: c_str_greeting might be a dangling pointer here!

d_DestroyString(greeting);
```

### `d_DumpString`

@brief Create a copy of the string builder's content.

**Signature:**

```c
char* d_DumpString(const dString_t* sb, size_t* len);
```

**Description:**
Creates a *newly allocated*, independent copy of the string builder's content on the heap. This is useful when you need a permanent copy of the string that will persist even if the original `dString_t` is modified or destroyed, or if you need a mutable C-string.

**Important Note:**

* The caller is **responsible for `free()`ing** the returned `char*` pointer to prevent memory leaks.

**Parameters:**

* `sb`: Pointer to the string builder.
* `len`: An optional pointer to a `size_t` variable. If provided (not `NULL`), the length of the returned string (excluding the null terminator) will be stored here.

**Returns:**
A newly allocated `char*` copy of the string, or `NULL` on error (e.g., null `sb` or memory allocation failure).

**Example:**

```c
dString_t* temp_str = d_InitString();
d_AppendToString(temp_str, "Ephemeral data.", 0);

size_t dumped_len;
char* persistent_copy = d_DumpString(temp_str, &dumped_len);

if (persistent_copy != NULL) {
    printf("Dumped String: %s (Length: %zu)\n", persistent_copy, dumped_len);
    free(persistent_copy); // IMPORTANT: Free the dumped string!
}
d_DestroyString(temp_str);
```

## Advanced String Operations

The `dString_t` builder's core functionality is now augmented with higher-level operations, allowing for more expressive and efficient code when dealing with dynamic text.

### Formatted Appending

These functions allow for `printf`-style formatting and repetitive character insertion directly into the string builder, with automatic memory management.

#### `d_FormatString`

@brief Append formatted text to the string builder using printf-style formatting.

**Signature:**

```c
void d_FormatString(dString_t* sb, const char* format, ...);
```

**Description:**
Appends formatted text to the `dString_t` using a `printf`-style format string and variable arguments. This function dynamically calculates the required buffer size and automatically grows the `dString_t`'s internal buffer as needed, preventing buffer overflows. It appends to the existing content, it does not replace it.

**Parameters:**

* `sb`: Pointer to the string builder.
* `format`: The `printf`-style format string (e.g., `"%s has %d health."`).
* `...`: Variable arguments corresponding to the format specifiers in `format`.

**Example:**

```c
dString_t* log_msg = d_InitString();
d_FormatString(log_msg, "Player %s entered the dungeon at level %d.", "Hero", 10);
printf("%s\n", d_PeekString(log_msg)); // Output: Player Hero entered the dungeon at level 10.
d_DestroyString(log_msg);
```

#### `d_RepeatString`

@brief Add repeated characters to the string builder.

**Signature:**

```c
void d_RepeatString(dString_t* sb, char character, int count);
```

**Description:**
Appends a specified `character` to the string builder `count` times. This is an efficient way to add multiple copies of the same character and is used internally by padding and progress bar functions.

**Parameters:**

* `sb`: Pointer to string builder.
* `character`: The character to repeat.
* `count`: The number of times to repeat the character.

**Example:**

```c
dString_t* separator = d_InitString();
d_RepeatString(separator, '-', 20);
printf("%s\n", d_PeekString(separator)); // Output: --------------------
d_DestroyString(separator);
```

### UI Building Blocks

These functions are specifically designed to help construct dynamic and visually aligned text-based user interfaces for console applications, leveraging the `dString_t`'s capabilities.

#### `d_AppendProgressBarToString`

@brief Add an ASCII progress bar to the string builder.

**Signature:**

```c
void d_AppendProgressBarToString(dString_t* sb, int current, int max, int width, char fill_char, char empty_char);
```

**Description:**
Appends an ASCII progress bar to the string builder. The bar's filled portion is determined by `current` and `max` values, and its total width is specified. The bar is enclosed in `[]` brackets.

**Parameters:**

* `sb`: Pointer to string builder.
* `current`: Current progress value.
* `max`: Maximum progress value.
* `width`: Width of the progress bar (excluding brackets).
* `fill_char`: Character to use for filled portions (e.g., `'#'`, `'█'`).
* `empty_char`: Character to use for empty portions (e.g., `'-'`, `' '`).

**Example:**

```c
dString_t* status = d_InitString();
d_AppendProgressBarToString(status, 60, 100, 15, '#', '-');
printf("Loading: %s\n", d_PeekString(status)); // Output: Loading: [#########------]
d_DestroyString(status);
```

#### `d_PadLeftString`

@brief Add text padded to the left with specified character to reach target width.

**Signature:**

```c
void d_PadLeftString(dString_t* sb, const char* text, int width, char pad_char);
```

**Description:**
Appends `text` to the string builder, padding it on the left with `pad_char` until it reaches the `width`. If `text` is already `width` or longer, no padding is added. Commonly used for right-aligned text in tables and menus.

**Parameters:**

* `sb`: Pointer to string builder.
* `text`: The null-terminated string to pad.
* `width`: The target total width including padding.
* `pad_char`: The character to use for padding.

**Example:**

```c
dString_t* menu_item = d_InitString();
d_PadLeftString(menu_item, "Exit", 10, '.');
printf("%s\n", d_PeekString(menu_item)); // Output: ......Exit
d_DestroyString(menu_item);
```

#### `d_PadRightString`

@brief Add text padded to the right with specified character to reach target width.

**Signature:**

```c
void d_PadRightString(dString_t* sb, const char* text, int width, char pad_char);
```

**Description:**
Appends `text` to the string builder, then pads it on the right with `pad_char` until it reaches the `width`. If `text` is already `width` or longer, no padding is added. Commonly used for left-aligned text in tables and menus.

**Parameters:**

* `sb`: Pointer to string builder.
* `text`: The null-terminated string to pad.
* `width`: The target total width including padding.
* `pad_char`: The character to use for padding.

**Example:**

```c
dString_t* menu_item = d_InitString();
d_PadRightString(menu_item, "Play", 10, '.');
printf("%s\n", d_PeekString(menu_item)); // Output: Play......
d_DestroyString(menu_item);
```

#### `d_PadCenterString`

@brief Add text centered with specified padding character to reach target width.

**Signature:**

```c
void d_PadCenterString(dString_t* sb, const char* text, int width, char pad_char);
```

**Description:**
Appends `text` to the string builder, centering it within the specified `width` by adding `pad_char` evenly to both sides. If padding cannot be evenly distributed, the left side receives one less character. Commonly used for centered headers and titles in ASCII interfaces.

**Parameters:**

* `sb`: Pointer to string builder.
* `text`: The null-terminated string to center.
* `width`: The target total width including padding.
* `pad_char`: The character to use for padding.

**Example:**

```c
dString_t* title = d_InitString();
d_PadCenterString(title, "GAME OVER", 20, '=');
printf("%s\n", d_PeekString(title)); // Output: =====GAME OVER=====
d_DestroyString(title);
```

### Intuitive String Manipulation (Pythonic Utilities)

These functions bring common, highly ergonomic string manipulation patterns from languages like Python directly into the C environment, making complex text processing more readable and efficient.

#### `d_ApplyTemplateToString`

@brief Add text with template substitution to the string builder.

**Signature:**

```c
void d_ApplyTemplateToString(dString_t* sb, const char* tmplt, const char** keys, const char** values, int count);
```

**Description:**
Parses a `tmplt` string, substituting placeholders in `{key}` format with corresponding `values` from the `keys` array. If a placeholder has no matching key, it is left unchanged. This is powerful for generating dynamic messages, dialogue, or configurable text.

**Parameters:**

* `sb`: Pointer to string builder.
* `tmplt`: Template string with placeholders in `{keyname}` format.
* `keys`: Array of C-string pointers representing the keys to match.
* `values`: Array of C-string pointers representing the replacement values.
* `count`: Number of key-value pairs in `keys` and `values` arrays.

**Example:**

```c
dString_t* message = d_InitString();
const char* tmpl = "Hello, {player}! You have {coins} coins.";
const char* k[] = {"player", "coins"};
const char* v[] = {"Alice", "100"};
d_ApplyTemplateToString(message, tmpl, k, v, 2);
printf("%s\n", d_PeekString(message)); // Output: Hello, Alice! You have 100 coins.
d_DestroyString(message);
```

#### `d_JoinStrings`

@brief Join an array of strings with a separator (like Python's `str.join()`).

**Signature:**

```c
void d_JoinStrings(dString_t* sb, const char** strings, int count, const char* separator);
```

**Description:**
Appends a sequence of `strings` from an array to the string builder, inserting a `separator` between each string. This is highly efficient for concatenating lists of items into a single string.

**Parameters:**

* `sb`: Pointer to string builder.
* `strings`: Array of C-string pointers to join.
* `count`: Number of strings in the `strings` array.
* `separator`: The C-string to insert between each element (can be `NULL` for no separation).

**Example:**

```c
dString_t* list = d_InitString();
const char* items[] = {"Sword", "Shield", "Potion"};
d_JoinStrings(list, items, 3, ", ");
printf("Inventory: %s\n", d_PeekString(list)); // Output: Inventory: Sword, Shield, Potion
d_DestroyString(list);
```

#### `d_SliceString`

@brief Extract a substring using Python-style slice notation (like `str[start:end]`).

**Signature:**

```c
void d_SliceString(dString_t* sb, const char* text, int start, int end);
```

**Description:**
Extracts a substring from `text` based on `start` and `end` indices and appends it to the string builder. Supports Python-style negative indexing (e.g., `-1` for the last character). Indices are clamped to valid string bounds.

**Parameters:**

* `sb`: Pointer to string builder.
* `text`: The source null-terminated string to slice.
* `start`: Starting index (inclusive). Negative values count from the end of the string.
* `end`: Ending index (exclusive). Negative values count from the end. A special value of `-1` means to slice to the very end of the string.

**Example:**

```c
dString_t* sub = d_InitString();
d_SliceString(sub, "Programming", 3, 7);
printf("Slice 1: %s\n", d_PeekString(sub)); // Output: Slice 1: gram
d_ClearString(sub);
d_SliceString(sub, "Pythonic", -4, -1); // Slice from 4th last to 1st last (exclusive)
printf("Slice 2: %s\n", d_PeekString(sub)); // Output: Slice 2: honi
d_DestroyString(sub);
```

#### `d_CompareStrings`

@brief Compare two `dString_t` objects lexicographically.

**Signature:**

```c
int d_CompareStrings(const dString_t* str1, const dString_t* str2);
```

**Description:**
Compares the content of two `dString_t` objects lexicographically. It returns an integer indicating their relative order, similar to `strcmp`. This function handles cases where `dString_t` pointers or their internal buffers are `NULL` gracefully, providing a consistent comparison result.

**Parameters:**

* `str1`: The first `dString_t` to compare.
* `str2`: The second `dString_t` to compare.

**Returns:**

* An integer less than 0 if `str1` is lexicographically less than `str2`.
* 0 if `str1` is lexicographically equal to `str2`.
* An integer greater than 0 if `str1` is lexicographically greater than `str2`.

**Example:**

```c
dString_t* s1 = d_InitString(); d_AppendToString(s1, "apple", 0);
dString_t* s2 = d_InitString(); d_AppendToString(s2, "banana", 0);
dString_t* s3 = d_InitString(); d_AppendToString(s3, "apple", 0);

printf("Compare 'apple' vs 'banana': %d (expected <0)\n", d_CompareStrings(s1, s2));
printf("Compare 'apple' vs 'apple': %d (expected 0)\n", d_CompareStrings(s1, s3));
printf("Compare 'banana' vs 'apple': %d (expected >0)\n", d_CompareStrings(s2, s1));

d_DestroyString(s1);
d_DestroyString(s2);
d_DestroyString(s3);
```

#### `d_CompareStringToCString`

@brief Compare a `dString_t` with a standard C-string lexicographically.

**Signature:**

```c
int d_CompareStringToCString(const dString_t* d_str, const char* c_str);
```

**Description:**
Compares the content of a `dString_t` object with a standard null-terminated C-string lexicographically. It returns an integer indicating their relative order. This function handles cases where either string is `NULL` or empty gracefully, providing consistent comparison results.

**Parameters:**

* `d_str`: The `dString_t` to compare.
* `c_str`: The standard null-terminated C-string to compare.

**Returns:**

* An integer less than 0 if `d_str` is lexicographically less than `c_str`.
* 0 if `d_str` is lexicographically equal to `c_str`.
* An integer greater than 0 if `d_str` is lexicographically greater than `c_str`.

**Example:**

```c
dString_t* my_d_string = d_InitString();
d_AppendToString(my_d_string, "hello", 0);

printf("Compare 'hello' (dString) vs 'world' (C-string): %d (expected <0)\n", d_CompareStringToCString(my_d_string, "world"));
printf("Compare 'hello' (dString) vs 'hello' (C-string): %d (expected 0)\n", d_CompareStringToCString(my_d_string, "hello"));
printf("Compare 'hello' (dString) vs 'abc' (C-string): %d (expected >0)\n", d_CompareStringToCString(my_d_string, "abc"));

d_DestroyString(my_d_string);
```
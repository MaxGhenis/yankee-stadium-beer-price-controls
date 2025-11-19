# Documentation Files

This directory contains the source Markdown files for the Jupyter Book documentation.

**WARNING: Some Markdown files in this directory contain `{{}}` placeholders that are automatically filled by the `scripts/update_docs_values.py` script.**

**DO NOT DIRECTLY EDIT THESE FILES ONCE THE PLACEHOLDERS HAVE BEEN REPLACED BY ACTUAL VALUES.**

If you need to update the content of a file that uses placeholders:
1.  **Restore Placeholders**: Manually revert the values back to their `{{ placeholder_name }}` form.
2.  **Edit Template**: Modify the text around the placeholders.
3.  **Run Update Script**: Execute `uv run scripts/update_docs_values.py` to regenerate the file with the latest model values.

Alternatively, for a more robust workflow, consider converting such files into templates (e.g., `filename.md.tpl` in a `docs/templates` subdirectory) and updating `scripts/update_docs_values.py` to read from the template and write to the final Markdown file.
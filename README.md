# Code Snippet Manager

Code Snippet Manager is a desktop application built with Python and PySide6 that allows developers to easily store, organize, and retrieve code snippets. It features syntax highlighting, search functionality, and import/export capabilities.

## Features

- Create, edit, and delete code snippets
- Syntax highlighting for various programming languages
- Search functionality to quickly find snippets
- Import and export snippets (individual or all)
- Language selection for proper syntax highlighting
- Resizable interface for comfortable viewing and editing
- File menu for easy access to import/export features
- About section with version information

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository or download the source code:

   \`\`\`
   git clone https://github.com/yourusername/code-snippet-manager.git
   cd code-snippet-manager
   \`\`\`

2. Install the required dependencies:

   \`\`\`
   pip install PySide6 Pygments
   \`\`\`

## Usage

To run the Code Snippet Manager, execute the following command in the project directory:

\`\`\`
python code_snippet_manager.py
\`\`\`

### Main Interface

- **Left Panel**: Displays a list of all saved snippets and a search bar.
- **Right Panel**: Shows the code editor and language selection dropdown.

### Adding a Snippet

1. Click the "Add Snippet" button.
2. Enter a name for your snippet.
3. Select the appropriate language from the dropdown.
4. Enter or paste your code in the editor.
5. Click "Save Changes" to store the snippet.

### Editing a Snippet

1. Select the snippet from the list on the left panel.
2. Modify the code in the editor.
3. Change the language if necessary.
4. Click "Save Changes" to update the snippet.

### Deleting a Snippet

1. Select the snippet from the list.
2. Click the "Delete Snippet" button.
3. Confirm the deletion in the popup dialog.

### Searching Snippets

Use the search bar above the snippet list to filter snippets by name or content.

### Importing and Exporting Snippets

- To import snippets, go to File > Import Snippets and select a JSON file.
- To export all snippets, go to File > Export All Snippets and choose a save location.
- To export a single snippet, select it and click the "Export Snippet" button.

## Contributing

Contributions to the Code Snippet Manager are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PySide6](https://wiki.qt.io/Qt_for_Python) for the GUI framework
- [Pygments](https://pygments.org/) for syntax highlighting

## Contact

If you have any questions, feel free to reach out to [Your Name] at [your.email@example.com].

# Hockey Canada Rules Reference

A streamlined app for quick reference of Hockey Canada's official rulebook.

![Canada Hockey](https://www.hockeycanada.ca/themes/custom/hc2016/img/logo-header-2016.png)

## Features

- **Quick Search**: Find rules by keyword or rule number
- **Section Filtering**: Filter rules by specific section
- **Proper Rule Numbering**: Rules are organized in numerical order (1.1, 1.2, 1.3, etc.)
- **Visual Organization**: Section icons help with navigation
- **Responsive Interface**: Works on all devices

## Demo

![App Screenshot](screenshot.png)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/hockey-canada-rules.git
cd hockey-canada-rules
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## Usage

- **Search**: Enter keywords in the search box to filter rules
- **Section Selection**: Use the checkboxes to show/hide specific sections
- **Clear Search**: Use the "Clear Search" button to reset your search
- **Expand/Collapse**: Click on any section to expand or collapse its rules

## Data

The app uses `hockey_rules.csv` which contains structured data from the Hockey Canada rulebook.

## Requirements

The app requires:
- Python 3.7+
- Streamlit
- Pandas

## Deployment

This app can be deployed to Streamlit Cloud or any other Python-compatible hosting platform.

## Credits

- Hockey Canada for the rulebook information
- Created by Patrick A. Mikkelsen

## License

This project is available for personal and educational use. 
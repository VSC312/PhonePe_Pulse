# PhonePe_Pulse
This project is a data visualization tool for analyzing PhonePe transaction and user data using Streamlit. Features include top charts for transactions and users, detailed state and district data visualization with choropleth maps and pie charts, and interactive exploration of various insights using Plotly and Pandas.
PhonePe Pulse Data Visualization

This project visualizes the top charts and trends based on PhonePe transaction and user data using Streamlit.

Table of Contents

Features

Setup

Usage

Dependencies

Screenshots

Contributing

License



Features


Visualize top states, districts, and pincodes by transaction count and amount.

Display top states, districts, and pincodes by registered user count.

Show top mobile brands used by PhonePe users.

Interactive year and quarter selection.

Clean and user-friendly UI with Streamlit.

Setup
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/phonepe-pulse-visualization.git
cd phonepe-pulse-visualization
Create and activate a virtual environment (optional but recommended):

bash

Copy code

python -m venv env

source env/bin/activate  # On Windows, use `env\Scripts\activate`

Install the dependencies:


bash

Copy code

pip install -r requirements.txt

Ensure you have your SQLite database set up and configured as required.


Usage

Run the Streamlit application:


bash

Copy code

streamlit run app.py

Open your web browser and navigate to http://localhost:8501.


Dependencies

pandas

plotly

streamlit

sqlite3

You can install all dependencies using:

bash
Copy code

pip install -r requirements.txt



 
License
This project is licensed under the MIT License - see the LICENSE file for details.


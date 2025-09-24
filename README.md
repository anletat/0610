
# game-tool

A small Streamlit web app to analyze Crash game history, detect "gray" (low-crash) and "green" (high-crash) trends,
and provide betting suggestions for small bankrolls (example: $10).

## Files
- `crash_tool.py` - main Streamlit app
- `requirements.txt` - Python dependencies
- `sample_data.txt` - sample history to test

## How to run locally
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Run the app:
```
streamlit run crash_tool.py
```
3. Open `http://localhost:8501` in your browser.

## How to deploy on Streamlit Cloud
1. Create a GitHub repository and push these files.
2. Go to https://share.streamlit.io and "New app".
3. Select your repository, branch (`main`) and the file `crash_tool.py`.
4. Deploy and open the provided link.


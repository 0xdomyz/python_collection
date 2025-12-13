# UI Approaches for Python Plotting

## 1. Script (.py)
- Interactivity: 🔴 None
- Exploration: 🔴 Limited, requires full re-run
- Iteration Speed: 🔴 Slow, full script execution
- Storage: 🔴 Manual (e.g., `savefig()`), disconnected from code
- Debugging: 🔴 Harder to trace and inspect environment at error point
- **Code Management: 🟢 Excellent for long/complex code, with modules and import system**
- Tool stability: 🟢 Very stable

## 1.5. vscode interactive window (.py)
- Interactivity: 🟡 Good
- Exploration: 🟢 Excellent, can inspect and experiment in new cell
- Iteration Speed: 🟡 Good, cell-by-cell execution, slower if need multiple cells
- Storage: 🟡 Moderate, allow knitting
- Debugging: 🟢 Easy, cell-by-cell
- Code Management: 🟡 Moderate
- Tool stability: 🟡 Moderate, some kernel issues

## 2. Jupyter Notebooks (.ipynb)
- Interactivity: 🟡 Good, optional widgets
- Exploration: 🟢 Excellent, can inspect and experiment in new cell
- Iteration Speed: 🟡 Good, cell-by-cell execution, slower if need multiple cells
- **Storage: 🟢 Excellent, Built-in output storage, no need knitting, no risk of misalignment**
- Debugging: 🟡 Good, cell-by-cell, long error message is disorientating
- Code Management: 🔴 Unwieldy if long/complex, scrolling around is disorientating
- Tool stability: 🔴 Not as stable, many kernel and display issues

## 3. Streamlit App
- **Interactivity: 🟢 Excellent, easy parameter cycling**
- Exploration: 🔴 Slow to add entirrely new items
- **Iteration Speed: 🟢 Excellent, auto refresh**
- Storage: 🔴 None
- Debugging: 🟡 Moderate, less capacity to inspect arbitrary stuff
- Code Management: 🟡 Moderate, intermingled with st stuff
- Tool stability: 🟡 Moderate, need to work with tool limitations

## Independent point on storing medium data for excel analysis
- Save to csv/excel
    - Script: manual save to csv/excel
    - Notebook: expose data in cell and use UI. But still need manual for reliable saving.
    - Streamlit: expose data via st.dataframe and use UI. But still need manual for reliable saving.
- Quick manual pivot in excel allowing the data to be manually refreshed to support deep dive.

# conclusion

- Use interactive window / notebook for initial exploration and prototyping.
- Expose and store data to csv/excel for deep dive analysis.
- Move to Streamlit once chart becomes complex or need to cycle some parameters.
- Once logic is stablised, move to script/module for better code management.
# Dashboards Notes

## Current demos
- `dash_tute.py`: Minimal Dash bar chart app (plotly + Dash). Run with `python dash_tute.py` then open http://127.0.0.1:8050/.
- `streamlit_tute/basic_elements.py`: Widgets (slider, selectbox, checkbox) with matplotlib bar chart.
- `streamlit_tute/df_cache.py`: `st.cache_data` demo with cache clear button, sliders for shape, simulated slow load.
- `streamlit_tute/progress.py`: Progress bar/placeholder example.
- `streamlit_tute/update_csv.py`: Simple CSV updater using text/number inputs and session log.
- `streamlit_tute/alt_chart_eg.py`: Altair area chart with multiselect and remote CSV data.
- `streamlit_tute/intro_example_202511.py`: Streamlit Uber pickups example with caching and map/bar chart.
- `streamlit_tute/sidebar_input.py`: Sidebar selectbox + slider driving a random DataFrame.
- `streamlit_tute/page_example/`: Multipage starter (main + two pages + shared utils).

## Gaps / improvements
1) Add a small theming/layout example: use `st.set_page_config`, `st.columns`, `st.tabs`, and `st.container` with a consistent palette.
2) Add data-loading patterns: `st.cache_data` + `st.cache_resource` for DB/client objects, with error handling and status messages.
3) Add file upload + validation example (CSV upload -> schema check -> chart/table preview).
4) Add background tasks / polling example (e.g., show progress while waiting on a long API call using `st.spinner` + `st.status`).
5) Testing guidance: add a short doc or example using `streamlit.testing.v1` for widget interactions.
6) For Dash, add a callback example with multiple inputs/outputs and `dcc.Interval` for live updates.

## Quick tips
- Keep expensive work behind `st.cache_data` or `st.cache_resource`; expose a "refresh" button to clear caches.
- Avoid unbounded reruns; prefer explicit actions (button press) for mutations.
- Use `st.session_state` to persist UI state between interactions.
- For remote data, show a minimal status text/placeholder while loading and handle failures gracefully.

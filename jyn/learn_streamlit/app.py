# 若同一台机器上有其它的 app 运行，streamlit 会自动选择一个新的端口，不需要手动指定端口
#               streamlit run app.py
import time

import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data
import numpy as np
from datetime import time as dt
from streamlit_extras.mandatory_date_range import date_range_picker

#################################
# date_picke
#################################

with st.sidebar:
    with st.form(key='my_form_replay'):
        col1, col2 = st.columns([1, 1])
        symbol = col1.selectbox("选择交易标的：", ("Email", "Home phone", "Mobile phone"), index=0)
        bar_sdt = col2.date_input(label='行情开始日期：', value=pd.to_datetime('2018-01-01'))
        sdt, edt = date_range_picker("回放起止日期", default_start=pd.to_datetime('2019-01-01'),
                                     default_end=pd.to_datetime('2022-01-01'))
        submitted = st.form_submit_button(label='设置回放参数')

#################################
# status
#################################

st.success('This is a success message!', icon="✅")
st.info('This is a purely informational message', icon="ℹ️")
st.warning('This is a warning', icon="⚠️")
st.error('This is an error', icon="🚨")
e = RuntimeError("This is an exception of type RuntimeError")
st.exception(e)

# progress_text = "Operation in progress. Please wait."
# my_bar = st.progress(0, text=progress_text)
# for percent_complete in range(100):
#     time.sleep(0.01)
#     my_bar.progress(percent_complete + 1, text=progress_text)
# time.sleep(0.1)
# my_bar.empty()
# st.button("Rerun")
#
# with st.spinner('Wait for it...'):
#     time.sleep(1)
# st.success("Done!")

# with st.status("Downloading data..."):
#     st.write("Searching for data...")
#     time.sleep(10)
#     st.write("Found URL.")
#     time.sleep(10)
#     st.write("Downloading data...")
#     time.sleep(10)
#     progress_text = "Operation in progress. Please wait."
#     my_bar = st.progress(0, text=progress_text)
#     for percent_complete in range(100):
#         time.sleep(0.01)
#         my_bar.progress(percent_complete + 1, text=progress_text)
#     time.sleep(0.1)
#     my_bar.empty()
#     st.write("Downloading done")
# st.button("Rerun")

if st.button('Three cheers'):
    st.toast('Hip 1!')
    time.sleep(2)
    st.toast('Hip 2!')
    time.sleep(2)
    st.toast('Hooray!', icon='🎉')
    time.sleep(2)
    st.balloons()
    time.sleep(2)
    st.snow()



#################################
# elements
#################################

st.title("This is a title")
st.title("_Streamlit_ is :blue[cool] :sunglasses:")
st.header("_Streamlit_ is :blue[cool] :sunglasses:")
st.header("This is a header with a divider", divider="gray")
st.header("These headers have rotating dividers", divider=True)
st.header("One", divider=True)
st.header("Two", divider=True)
st.header("Three", divider=True)
st.header("Four", divider=True)
# st.header("One", divider=True)
# st.header("Two", divider=True)
# st.header("Three", divider=True)
# st.header("Four", divider=True)
# st.header("One", divider=True)
# st.header("Two", divider=True)
# st.header("Three", divider=True)
# st.header("Four", divider=True)
# st.header("One", divider=True)
# st.header("Two", divider=True)
# st.header("Three", divider=True)
# st.header("Four", divider=True)

# markdown
st.markdown("*Streamlit* is **really** ***cool***.")
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
st.markdown("Here's a bouquet &mdash;\
            :tulip: :cherry_blossom::rose::hibiscus::sunflower::blossom:")

multi = '''If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
'''
st.markdown(multi)

appointment = st.slider(
    "Schedule your appointment:", value=(time(11, 30), time(12, 45))
)
st.write("You're scheduled for:", appointment)

st.divider()

#################################
# st.write_stream
#################################

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""

def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.01)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Stream data"):
    st.write_stream(stream_data)

st.divider()

#################################
# st.write 可以写几乎任何对象，包括chart
#################################

st.write(1234)
st.write(
    pd.DataFrame(
        {
            "first column": [1, 2, 3, 4],
            "second column": [10, 20, 30, 40],
        }
    )
)

st.divider()

#################################
# 1. build data layer
#################################

@st.cache_data
def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source

stock_data = get_data()

hover = alt.selection_single(
    fields=["date"],
    nearest=True,
    on="mouseover",
    empty="none",
)

lines = (
    alt.Chart(stock_data, title="Evolution of stock prices")
    .mark_line()
    .encode(
        x="date",
        y="price",
        color="symbol",
    )
)

points = lines.transform_filter(hover).mark_circle(size=65)

tooltips = (
    alt.Chart(stock_data)
    .mark_rule()
    .encode(
        x="yearmonthdate(date)",
        y="price",
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("date", title="Date"),
            alt.Tooltip("price", title="Price (USD)"),
        ],
    )
    .add_selection(hover)
)

data_layer = lines + points + tooltips

# st.altair_chart(data_layer, use_container_width=True)

#################################
# 2. build annotation layer
#################################

ANNOTATIONS = [
    ("Sep 01, 2007", 450, "🙂", "Something's going well for GOOG & AAPL."),
    ("Nov 01, 2008", 220, "🙂", "The market is recovering."),
    ("Dec 01, 2007", 750, "😱", "Something's going wrong for GOOG & AAPL."),
    ("Dec 01, 2009", 680, "😱", "A hiccup for GOOG."),
]
annotations_df = pd.DataFrame(
    ANNOTATIONS, columns=["date", "price", "marker", "description"]
)
annotations_df.date = pd.to_datetime(annotations_df.date)

annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=20, dx=-10, dy=0, align="left")
    .encode(x="date:T", y=alt.Y("price:Q"), text="marker", tooltip="description")
)

combined_chart = data_layer + annotation_layer

st.altair_chart(combined_chart, use_container_width=True)

st.divider()

#################################
# column
#################################

col1, col2, col3 = st.columns(3)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")


st.divider()
#################################
# container
#################################

@st.cache_data
def load_container_data():
    return np.random.randn(50, 3)

with st.container():
    st.write("This is inside the container")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(load_container_data())

st.write("This is outside the container")

st.divider()
#################################
# dialog
#################################

@st.dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
    if st.button("C"):
        vote("C")
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

st.divider()
#################################
# sidebar
#################################

with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

st.divider()
#################################
# tab
#################################

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

st.divider()
#################################
# popover 弹窗
#################################

with st.popover("Open popover"):
    st.markdown("Hello World 👋")
    name = st.text_input("What's your name?")

st.write("Your name:", name)
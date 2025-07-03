import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

st.title(" Streamlit visualization")

data = pd.DataFrame(
    np.random.randn(100,5),
    columns=['A', 'B', 'C', 'D', 'E']
)

#st.write(data)

#st.line_chart(data)
#st.line_chart(data, x='A')
#st.line_chart(data, x='A', y='B') 
#
#st.area_chart(data) 
#st.area_chart(data, x='A')
#st.area_chart(data, x='A', y='B')
#
#st.bar_chart(data)
#st.bar_chart(data, x='A')
#st.bar_chart(data, x='A', y='B')
#
#st.metric(label="Temperature", value="20 °C", delta="1 °C")
#st.metric(label="Humidity", value="60%", delta="-5%")   
#st.metric(label="Wind Speed", value="15 km/h", delta="2 km/h")
#
#st.dataframe(data, use_container_width=True)
#st.dataframe(data, use_container_width=True, height=300)
#
#st.table(data.head())
#
#st.json({"name": "John", "age": 30, "city": "New York"})
#
#st.code("""
#def hello_world():
#    print("Hello, world!")
#hello_world()
#""", language='python')
#
#st.latex(r"""
#\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
#""")    
#
#st.image("https://via.placeholder.com/150", caption="Placeholder Image")
#
#
#st.video("https://www.w3schools.com/html/mov_bbb.mp4", format="video/mp4")
#
#st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")   
#
#st.sidebar.title("Sidebar Title")
#st.sidebar.write("This is a sidebar")
#st.sidebar.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])      
#st.sidebar.slider("Select a range", 0, 100, (25, 75))
#st.sidebar.checkbox("Check me")
#
#st.sidebar.radio("Choose one", ["Radio 1", "Radio 2", "Radio 3"])
#st.sidebar.multiselect("Select multiple", ["Option A", "Option B", "Option C"])
#st.sidebar.text_input("Enter text")
#
#st.sidebar.text_area("Enter more text")
#st.sidebar.date_input("Select a date")  
#st.sidebar.time_input("Select a time")
#st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx"])
#st.sidebar.color_picker("Pick a color", "#00f900")

#fig,ax = plt.subplots()
#ax.scatter(data['A'], data['B']) 
#st.pyplot(fig)


#chart = alt.Chart(data).mark_circle().encode(x ='A', y='B')
#st.altair_chart(chart, use_container_width=True)
#
#st.graphviz_chart("""
#digraph G {
#    A -> B;
#    B -> C;
#    C -> D;
#}
#""")

data = pd.DataFrame({
    'latitude': [37.7749, 34.0522, 40.7128],
    'longitude': [-122.4194, -118.2437, -74.0060]
})

st.map(data)

a = st.camera_input("Take a picture")
if a:
    st.image(a, caption="Captured Image", use_column_width=True)

    
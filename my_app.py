# IMPORTING REQUIRED LIBRARIES
import pandas as pd
import plotly.express as px
import streamlit as st 
import io

# Setting page configuration
st.set_page_config(page_title="Analytics Hub", page_icon="📈")

# Custom CSS to position the footer at the bottom
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #00b4d8;
        color: #FFF;
        text-align: center;
        padding: 10px;
        font-size: medium;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# Using markdown with inline HTML to add color and center the main heading
st.markdown("<h1 style='color: #00b4d8; text-align: center;'>Data Insights Junction</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #ff8fab; text-align: center;'>Find Your Data Insights</h2>", unsafe_allow_html=True)

# File uploader for CSV or Excel files
file = st.file_uploader("Drop CSV or Excel File", type=["csv", "xlsx"])

if file is not None:
    # Reading the file
    if file.name.endswith("csv"):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    # Displaying the dataframe
    st.dataframe(data)
    st.info("Uploaded Successfully", icon="🚨")

    # Basic Information of Dataset Section
    st.markdown("<h3 style='color: #ffd60a;'>Basic Information of Dataset</h3>", unsafe_allow_html=True)
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Top and Bottom Rows", "Data Types", "Columns"])

    with tab1:
        # Displaying the number of rows and columns
        st.write(f"There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.")
        
        # Displaying the number of missing values
        missing_values = data.isnull().sum().sum()
        st.write(f"There are a total of {missing_values} missing values in the dataset.")

        # Statistical Summary Section
        st.markdown("<h4 style='color: #4682B4;'>Statistical Summary of Dataset</h4>", unsafe_allow_html=True)
        st.dataframe(data.describe())

        # Filling Missing Values Section
        st.markdown("<h4 style='color: #4682B4;'>Filling Missing Values</h4>", unsafe_allow_html=True)
        fill_option = st.selectbox("Choose an option to fill missing values:", ["Zero", "None", "Mean", "Median", "Custom"])
        
        custom_value = None
        if fill_option == "Custom":
            custom_value = st.text_input("Enter your custom value:")

        if st.button("Fill Missing Values"):
            if fill_option == "Zero":
                data.fillna(0, inplace=True)
            elif fill_option == "None":
                data.fillna('', inplace=True)
            elif fill_option == "Mean":
                data.fillna(data.mean(), inplace=True)
            elif fill_option == "Median":
                data.fillna(data.median(), inplace=True)
            elif fill_option == "Custom" and custom_value:
                data.fillna(custom_value, inplace=True)
            st.success("Missing values filled successfully!")

    with tab2:
        # Top and Bottom Rows Section
        st.markdown("<h4 style='color: #4682B4;'>Top Rows</h4>", unsafe_allow_html=True)
        toprows = st.slider("Number of rows you want", 1, data.shape[0], key="Top slider")
        st.dataframe(data.head(toprows))
        
        st.markdown("<h4 style='color: #4682B4;'>Bottom Rows</h4>", unsafe_allow_html=True)
        bottomrows = st.slider("Number of rows you want", 1, data.shape[0], key="Bottom Slider")
        st.dataframe(data.tail(bottomrows))

    with tab3:
        # Data Types Section
        st.markdown("<h4 style='color: #4682B4;'>Data Types of Columns</h4>", unsafe_allow_html=True)
        st.dataframe(data.dtypes)

    with tab4:
        # Columns Information Section
        st.markdown("<h4 style='color: #4682B4;'>Columns Information</h4>", unsafe_allow_html=True)
        st.write(list(data.columns))

    # Download Dataset Button
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    st.download_button(
        "Download Dataset as CSV",
        convert_df(data),
        "dataset.csv",
        "text/csv",
        key='download-csv'
    )

    # Column Value Count Section
    st.markdown("<h3 style='color: #ffd60a;'>Columns Values To Count</h3>", unsafe_allow_html=True)
    st.divider()
    with st.expander("Value Count"):
        col1, col2 = st.columns(2)
        with col1:
            col = st.selectbox("Choose Column Name", options=list(data.columns))
        with col2:
            top_row = st.number_input("Choose Number of Top Rows", min_value=1, step=1)

        count = st.button("Count")
        if count:
            result = data[col].value_counts().reset_index()
            result.columns = [col, 'count']
            result = result.head(top_row)
            st.dataframe(result)
            st.markdown("<h4 style='color: #ffd60a;'>Visualization</h4>", unsafe_allow_html=True)
            st.divider()
            
            # Bar chart visualization
            fig = px.bar(data_frame=result, x=col, y="count", text="count")
            st.plotly_chart(fig)
            # Download Chart
            if st.button("Download Chart"):
                chart_buffer = io.BytesIO()
                fig.write_image(chart_buffer, format='png')
                chart_buffer.seek(0)
                st.download_button(
                    "Download Chart as PNG",
                    chart_buffer,
                    "chart.png",
                    "image/png",
                    key='download-chart'
                )
            
            # Line chart visualization
            fig = px.line(data_frame=result, x=col, y="count", text="count")
            st.plotly_chart(fig)
            if st.button("Download Line Chart"):
                chart_buffer = io.BytesIO()
                fig.write_image(chart_buffer, format='png')
                chart_buffer.seek(0)
                st.download_button(
                    "Download Line Chart as PNG",
                    chart_buffer,
                    "line_chart.png",
                    "image/png",
                    key='download-line-chart'
                )
            
            # Pie chart visualization
            fig = px.pie(data_frame=result, names=col, values="count")
            st.plotly_chart(fig)
            if st.button("Download Pie Chart"):
                chart_buffer = io.BytesIO()
                fig.write_image(chart_buffer, format='png')
                chart_buffer.seek(0)
                st.download_button(
                    "Download Pie Chart as PNG",
                    chart_buffer,
                    "pie_chart.png",
                    "image/png",
                    key='download-pie-chart'
                )

    # Groupby Insights Section
    st.markdown("<h3 style='color: #e7c6ff;'>Get Insights Through Groupby</h3>", unsafe_allow_html=True)
    st.divider()
    
    with st.expander("Groupby Insights"):
        col1, col2, col3 = st.columns(3)
        with col1:
            group_by_cols = st.multiselect("Choose Desired Columns", options=list(data.columns))
        with col2:
            op_col = st.selectbox("Choose Operations Column", options=list(data.columns))
        with col3:
            op = st.selectbox("Choose Operation", options=["max", "sum", "min", "mean", "median", "count"])

        if group_by_cols:
            result = data.groupby(group_by_cols).agg(new_col=(op_col, op)).reset_index()
            st.dataframe(result)

            st.markdown("<h3 style='color: #DC143C;'>Data Visualization</h3>", unsafe_allow_html=True)
            st.divider()

            # Graph selection
            graphs = st.selectbox("Choose Your Graph", options=["line", "bar", "sunburst", "scatter", "pie"])
            if graphs == 'line':
                x_axis = st.selectbox("Define X-axis", options=list(result.columns))
                y_axis = st.selectbox("Define Y-axis", options=list(result.columns))
                color = st.selectbox("Choose Color info", options=[None] + list(result.columns))
                fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers=True)
                st.plotly_chart(fig)
                if st.button("Download Line Graph"):
                    chart_buffer = io.BytesIO()
                    fig.write_image(chart_buffer, format='png')
                    chart_buffer.seek(0)
                    st.download_button(
                        "Download Line Graph as PNG",
                        chart_buffer,
                        "line_graph.png",
                        "image/png",
                        key='download-line-graph'
                    )
            elif graphs == "bar":
                x_axis = st.selectbox("Define X-axis", options=list(result.columns))
                y_axis = st.selectbox("Define Y-axis", options=list(result.columns))
                color = st.selectbox("Choose Color info", options=[None] + list(result.columns))
                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color)
                st.plotly_chart(fig)
                if st.button("Download Bar Chart"):
                    chart_buffer = io.BytesIO()
                    fig.write_image(chart_buffer, format='png')
                    chart_buffer.seek(0)
                    st.download_button(
                        "Download Bar Chart as PNG",
                        chart_buffer,
                        "bar_chart.png",
                        "image/png",
                        key='download-bar-chart'
                    )
            elif graphs == "scatter":
                x_axis = st.selectbox("Define X-axis", options=list(result.columns))
                y_axis = st.selectbox("Define Y-axis", options=list(result.columns))
                color = st.selectbox("Choose Color info", options=[None] + list(result.columns))
                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color)
                st.plotly_chart(fig)
                if st.button("Download Scatter Chart"):
                    chart_buffer = io.BytesIO()
                    fig.write_image(chart_buffer, format='png')
                    chart_buffer.seek(0)
                    st.download_button(
                        "Download Scatter Chart as PNG",
                        chart_buffer,
                        "scatter_chart.png",
                        "image/png",
                        key='download-scatter-chart'
                    )
            elif graphs == "pie":
                names = st.selectbox("Define Names", options=list(result.columns))
                values = st.selectbox("Define Values", options=list(result.columns))
                fig = px.pie(data_frame=result, names=names, values=values)
                st.plotly_chart(fig)
                if st.button("Download Pie Chart"):
                    chart_buffer = io.BytesIO()
                    fig.write_image(chart_buffer, format='png')
                    chart_buffer.seek(0)
                    st.download_button(
                        "Download Pie Chart as PNG",
                        chart_buffer,
                        "pie_chart.png",
                        "image/png",
                        key='download-pie-chart'
                    )
            elif graphs == "sunburst":
                path = st.multiselect("Choose Path", options=list(result.columns))
                values = st.selectbox("Define Values", options=list(result.columns))
                fig = px.sunburst(data_frame=result, path=path, values=values)
                st.plotly_chart(fig)
                if st.button("Download Sunburst Chart"):
                    chart_buffer = io.BytesIO()
                    fig.write_image(chart_buffer, format='png')
                    chart_buffer.seek(0)
                    st.download_button(
                        "Download Sunburst Chart as PNG",
                        chart_buffer,
                        "sunburst_chart.png",
                        "image/png",
                        key='download-sunburst-chart'
                    )

# Footer Section
st.markdown("<div class='footer'>Built with ❤️ by Harshita Bhardwaj</div>", unsafe_allow_html=True)

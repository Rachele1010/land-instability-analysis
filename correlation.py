import streamlit as st
import pandas as pd
import hydralit_components as hc
from plotting import create_and_render_plot
from filter import dynamic_filter_and_operations
from load import load_and_display_file
import io

def map_combined_datasets(df1, df2):
    """
    Funzione per mappare i dataset combinati con colonne di latitudine e longitudine.
    """
    if df1 is not None:
        lat_col_1 = [col for col in df1.columns if "lat" in col.lower()]
        lon_col_1 = [col for col in df1.columns if "lon" in col.lower()]
        if lat_col_1 and lon_col_1:
            df1 = df1.rename(columns={lat_col_1[0]: 'lat', lon_col_1[0]: 'lon'})
        else:
            df1 = None

    if df2 is not None:
        lat_col_2 = [col for col in df2.columns if "lat" in col.lower()]
        lon_col_2 = [col for col in df2.columns if "lon" in col.lower()]
        if lat_col_2 and lon_col_2:
            df2 = df2.rename(columns={lat_col_2[0]: 'lat', lon_col_2[0]: 'lon'})
        else:
            df2 = None

    if df1 is not None and df2 is not None:
        combined_df = pd.concat([df1[['lat', 'lon']], df2[['lat', 'lon']]], ignore_index=True).dropna()
    elif df1 is not None:
        combined_df = df1[['lat', 'lon']].dropna()
    elif df2 is not None:
        combined_df = df2[['lat', 'lon']].dropna()
    else:
        combined_df = None

    if combined_df is not None and not combined_df.empty:
        st.map(combined_df)
    else:
        st.warning("No valid latitude or longitude data available for map display.")

def correlation():
    """Dashboard per la gestione dei file con Drag & Drop."""
    st.header("Data Analysis and Plotting")

    uploaded_files = st.file_uploader("Drag & Drop your CSV files here", type=["csv"], accept_multiple_files=True)
    
    df_list = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
            df_list.append(df)
            st.write(f"### {uploaded_file.name}")
            st.dataframe(df)
    
    if len(df_list) >= 1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            x_axis1 = st.selectbox("Select X axis for Dataset 1", df_list[0].columns.tolist(), key="x_axis1")
            y_axis1 = st.selectbox("Select Y axis for Dataset 1", df_list[0].columns.tolist(), key="y_axis1")
            plot_type1 = st.selectbox("Select plot type for Dataset 1", [
                "Basic Scatter", "Basic Bar", "Basic Line", "Mixed Line and Bar", "Calendar Heatmap", "DataZoom"
            ], key="plot_type_1")
            create_and_render_plot(df_list[0], x_axis1, y_axis1, plot_type1)
        
        if len(df_list) >= 2:
            with col2:
                x_axis2 = st.selectbox("Select X axis for Dataset 2", df_list[1].columns.tolist(), key="x_axis2")
                y_axis2 = st.selectbox("Select Y axis for Dataset 2", df_list[1].columns.tolist(), key="y_axis2")
                plot_type2 = st.selectbox("Select plot type for Dataset 2", [
                    "Basic Scatter", "Basic Bar", "Basic Line", "Mixed Line and Bar", "Calendar Heatmap", "DataZoom"
                ], key="plot_type_2")
                create_and_render_plot(df_list[1], x_axis2, y_axis2, plot_type2)
                
        map_combined_datasets(df_list[0], df_list[1] if len(df_list) > 1 else None)

    else:
        st.info("No files uploaded yet.")

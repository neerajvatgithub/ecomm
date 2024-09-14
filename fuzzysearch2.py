import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import io
import chardet
import os


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def find_best_match(item, mapping_dict):
    if item in mapping_dict:
        return mapping_dict[item], 100  # Exact match
    else:
        best_match, score = process.extractOne(item, mapping_dict.keys())
        return mapping_dict[best_match], score


def process_items(mapping_df, new_items_df, threshold):
    mapping_dict = dict(zip(mapping_df['Item'], mapping_df['Category']))

    total_items = len(new_items_df)
    progress_bar = st.progress(0)
    progress_text = st.empty()

    results = []
    for index, row in new_items_df.iterrows():
        item = row['Item']
        matched_category, score = find_best_match(item, mapping_dict)

        if score >= threshold:
            final_category = matched_category
        else:
            final_category = 'Unmatched'

        results.append({
            'Item': item,
            'Matched_Category': matched_category,
            'Match_Score': score,
            'Final_Category': final_category
        })

        # Update progress
        progress = (index + 1) / total_items
        progress_bar.progress(progress)
        progress_text.text(f"Processing: {index + 1}/{total_items}")

    return pd.DataFrame(results)


st.title("E-commerce Item Category Mapper")

# Instructions and Custom CSS for green slider
st.markdown("""
# Instructions
1. Upload a Mapping File (CSV) containing 'Item' and 'Category' columns.
2. Upload a New Items File (CSV) containing an 'Item' column.
3. Adjust the Matching Threshold if needed.
4. Click 'Process Files' to start the mapping process.
5. Once processing is complete, you can view the results preview and download the full results as CSV or Excel file.

<style>
    /* Targeting the slider track */
    # .stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] {
    #     background: #4CAF50;
    # }
    
    /* Targeting the slider handle */
    .stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
        background-color: #4CAF50 !important;
    }

    /* Targeting the filled part of the slider */
    .stSlider > div[data-baseweb="slider"] > div > div > div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# File upload section
st.header("File Upload")

# Mapping file upload
mapping_file = st.file_uploader("Upload Mapping File (CSV)", type="csv", key="mapping_file")
if mapping_file:
    st.success(f"Mapping file '{mapping_file.name}' uploaded successfully!")
    try:
        # Save the uploaded file temporarily
        with open("temp_mapping.csv", "wb") as f:
            f.write(mapping_file.getbuffer())

        # Detect encoding
        encoding = detect_encoding("temp_mapping.csv")
        st.info(f"Detected encoding for mapping file: {encoding}")

        # Read the file with the detected encoding
        mapping_df = pd.read_csv("temp_mapping.csv", encoding=encoding)
        st.write(f"Mapping file preview (first 5 rows):")
        st.write(mapping_df.head())
    except Exception as e:
        st.error(f"Error reading mapping file: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists("temp_mapping.csv"):
            os.remove("temp_mapping.csv")

# New items file upload
new_items_file = st.file_uploader("Upload New Items File (CSV)", type="csv", key="new_items_file")
if new_items_file:
    st.success(f"New items file '{new_items_file.name}' uploaded successfully!")
    try:
        # Save the uploaded file temporarily
        with open("temp_new_items.csv", "wb") as f:
            f.write(new_items_file.getbuffer())

        # Detect encoding
        encoding = detect_encoding("temp_new_items.csv")
        st.info(f"Detected encoding for new items file: {encoding}")

        # Read the file with the detected encoding
        new_items_df = pd.read_csv("temp_new_items.csv", encoding=encoding)
        st.write(f"New items file preview (first 5 rows):")
        st.write(new_items_df.head())
    except Exception as e:
        st.error(f"Error reading new items file: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists("temp_new_items.csv"):
            os.remove("temp_new_items.csv")

# Threshold slider
threshold = st.slider("Matching Threshold", min_value=0, max_value=100, value=80)

if mapping_file and new_items_file:
    if st.button("Process Files"):
        try:
            with st.spinner("Processing..."):
                result_df = process_items(mapping_df, new_items_df, threshold)

            st.success("Processing complete!")

            # Display results
            st.write("Results preview (first 10 rows):")
            st.write(result_df.head(10))

            # Provide download buttons
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="mapped_items.csv",
                mime="text/csv"
            )

            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                result_df.to_excel(writer, index=False, sheet_name='Mapped Items')
            excel_data = excel_buffer.getvalue()
            st.download_button(
                label="Download Results as Excel",
                data=excel_data,
                file_name="mapped_items.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")
else:
    st.info("Please upload both the Mapping File and New Items File to proceed.")
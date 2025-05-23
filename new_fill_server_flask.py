# import streamlit as st
# from PIL import Image, ImageDraw, ImageFont
# import io

# # Set page configuration for wide layout
# st.set_page_config(
#     page_title="Sales Team Image Generator",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Streamlit app title with styling
# st.markdown("""
#     <p style='text-align: center; color: #566573; margin-bottom: 30px;'>
#         Create professional sales performance images with ease
#     </p>
# """, unsafe_allow_html=True)

# # Font loader with specified size
# def load_font(size):
#     try:
#         return ImageFont.truetype("Anton-Regular.ttf", size)
#     except:
#         try:
#             return ImageFont.truetype("arialbd.ttf", size)
#         except:
#             return ImageFont.load_default()

# # Function to format numbers with commas (Indian style: 12,30,56,789)
# def format_indian_number(number_str):
#     try:
#         num = int(float(number_str.replace(",", "")))
#         num_str = str(num)
#         if len(num_str) <= 3:
#             return num_str
#         result = num_str[-3:]
#         remaining = num_str[:-3]
#         while remaining:
#             result = remaining[-2:] + "," + result
#             remaining = remaining[:-2]
#         return result
#     except (ValueError, AttributeError):
#         return number_str

# # Function to calculate percentage
# def calculate_percentage(achieved, target):
#     try:
#         achieved = float(achieved.replace(",", ""))
#         target = float(target.replace(",", ""))
#         if target == 0:
#             return "0"
#         return f"{(achieved / target * 100):.2f}"
#     except (ValueError, AttributeError):
#         return ""

# # Coordinates for Till Time image (ACTUAL_REGION_REVENUE_blank.jpg) - unchanged
# positions_till_time = {
#     "row1": {
#         "total": (550, 768, 40),
#         "target": (759, 768, 44),
#         "cases": (1010, 768, 40),
#         "till_date_ach": (1232, 768, 44),
#         "percent": (1460, 778, 32)
#     },
#     "row2": {
#         "total": (550, 1000, 40),
#         "target": (759, 1000, 44),
#         "cases": (1010, 1000, 40),
#         "till_date_ach": (1232, 1000, 44),
#         "percent": (1460, 1000, 32)
#     },
#     "total": {
#         "total": (550, 1155, 40),
#         "target": (759, 1155, 44),
#         "cases": (1010, 1155, 40),
#         "till_date_ach": (1232, 1155, 44),
#         "percent": (1460, 1155, 32)
#     }
# }

# # New coordinates for Today image (today.jpg) with 4 columns: today_target, cases, revenue, percent
# positions_today = {
#     "row1": {
#         "today_target": (660, 768, 44),
#         "cases": (945, 768, 40),
#         "revenue": (1185, 768, 44),
#         "percent": (1452, 768, 32)
#     },
#     "row2": {
#         "today_target": (660, 1000, 44),
#         "cases": (945, 1000, 40),
#         "revenue": (1185, 1000, 44),
#         "percent": (1452, 1000, 32)
#     },
#     "total": {
#         "today_target": (660, 1160, 44),
#         "cases": (945, 1160, 40),
#         "revenue": (1185, 1160, 44),
#         "percent": (1452, 1160, 32)
#     }
# }

# # Region positions (before the total column, only for row1 and row2)
# region_positions = {
#     "row1": (-185, 700, 46),
#     "row2": (-185, 935, 46)
# }

# # Initialize session state
# if "data" not in st.session_state:
#     st.session_state.data = {
#         "row1": {
#             "region_image": "None", "total": "", "target": "", "today_target": "", "cases": "", "till_date_ach": "", "revenue": "", "percent": ""
#         },
#         "row2": {
#             "region_image": "None", "total": "", "target": "", "today_target": "", "cases": "", "till_date_ach": "", "revenue": "", "percent": ""
#         },
#         "total": {
#             "total": "", "target": "", "today_target": "", "cases": "", "till_date_ach": "", "revenue": "", "percent": ""
#         }
#     }

# # Function to resize image with contain style (maintain aspect ratio, no cropping)
# def resize_image_contain(image, target_size):
#     target_width, target_height = target_size
#     img_width, img_height = image.size
#     aspect_ratio = img_width / img_height
#     target_aspect = target_width / target_height

#     # Scale to fit within target dimensions
#     if aspect_ratio > target_aspect:
#         # Image is wider, scale by width
#         new_width = target_width
#         new_height = int(new_width / aspect_ratio)
#     else:
#         # Image is taller, scale by height
#         new_height = target_height
#         new_width = int(new_height * aspect_ratio)

#     # Resize image
#     image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

#     # Create a new image with transparent background
#     new_image = Image.new("RGBA", target_size, (0, 0, 0, 0))
#     # Paste the resized image in the center
#     paste_x = (target_width - new_width) // 2
#     paste_y = (target_height - new_height) // 2
#     new_image.paste(image, (paste_x, paste_y))

#     return new_image

# # Function to generate the image
# def generate_image(image_type, data):
#     # Load the base image
#     image = Image.open("ACTUAL_REGION_REVENUE_blank.jpg" if image_type == "Till Time" else "today.jpg")
#     draw = ImageDraw.Draw(image)

#     # Paste region images for row1 and row2
#     for row, (x, y, font_size) in region_positions.items():
#         region_image_path = data[row]["region_image"]
#         if region_image_path != "None":
#             try:
#                 region_img = Image.open(region_image_path)
#                 # Resize with contain style to a smaller size (1200x250)
#                 region_img = resize_image_contain(region_img, (1200, 250))
#                 # Center the image at the specified coordinates
#                 paste_x = x - 75  # Half of target width (150/2)
#                 paste_y = y - 20  # Half of target height (40/2)
#                 image.paste(region_img, (paste_x, paste_y), region_img if region_img.mode == "RGBA" else None)
#             except:
#                 st.warning(f"Failed to load region image for {row}. Proceeding without it.")

#     positions = positions_till_time if image_type == "Till Time" else positions_today

#     # Draw the values with centered text and fixed color
#     text_color = (245, 254, 220)  # RGB color for all text
#     for row, cols in positions.items():
#         for key, (x, y, font_size) in cols.items():
#             font = load_font(font_size)
#             # Format the text with prefix/suffix and commas where applicable
#             if key in ["target", "today_target", "till_date_ach", "revenue"]:
#                 formatted_value = format_indian_number(data[row][key])
#                 text = f"₹{formatted_value}" if data[row][key] else ""
#             elif key == "percent":
#                 text = f"{data[row][key]}%" if data[row][key] else ""
#             else:
#                 text = data[row][key]

#             if not text:
#                 continue

#             # Get text bounding box to calculate width for centering
#             try:
#                 text_bbox = draw.textbbox((0, 0), text, font=font)
#                 text_width = text_bbox[2] - text_bbox[0]
#             except AttributeError:
#                 text_width = draw.textsize(text, font=font)[0]

#             centered_x = x - (text_width // 2)
#             draw.text((centered_x, y), text, fill=text_color, font=font)

#     return image

# # Main container for layout
# with st.container():
#     # Create two columns for inputs and preview
#     col1, col2 = st.columns([2, 1], gap="large")

#     with col1:
#         # Image type selection with styling
#         st.markdown("#### Select Image Type")
#         image_type = st.selectbox(
#             "",
#             ["Till Time", "Today"],
#             key="image_type",
#             help="Choose whether to generate a Till Time or Today image"
#         )
#         st.markdown("---")

#         # Create input forms for each row
#         for row in ["row1", "row2", "total"]:
#             st.markdown(f"#### Enter Data for {row.capitalize()}")
#             # Use container for input fields to control width
#             with st.container():
#                 # Create columns for input fields with adjusted widths
#                 cols = st.columns([2, 2, 2, 2, 2])
#                 with cols[0]:
#                     # Region image selection only for row1 and row2
#                     if row in ["row1", "row2"]:
#                         st.session_state.data[row]["region_image"] = st.selectbox(
#                             f"Region Image ({row})",
#                             ["None", "SRIRAM JOSHI.png", "BHAVIK GANATRA.png"],
#                             index=["None", "SRIRAM JOSHI.png", "BHAVIK GANATRA.png"].index(st.session_state.data[row]["region_image"]),
#                             key=f"region_image_{row}",
#                             help="Select an image for the region"
#                         )
#                 with cols[1]:
#                     if image_type == "Till Time":
#                         st.session_state.data[row]["total"] = st.text_input(
#                             f"Total ({row})",
#                             value=st.session_state.data[row]["total"],
#                             placeholder="Enter Total",
#                             key=f"total_{row}"
#                         )
#                     else:
#                         # For "Today", we don't need Total, so hide this field
#                         st.session_state.data[row]["total"] = ""
#                 with cols[2]:
#                     if image_type == "Till Time":
#                         target_input = st.text_input(
#                             f"Target ({row})",
#                             value=st.session_state.data[row]["target"],
#                             placeholder="₹ Enter Target",
#                             key=f"target_{row}"
#                         )
#                         st.session_state.data[row]["target"] = target_input
#                         st.session_state.data[row]["today_target"] = ""
#                     else:
#                         today_target_input = st.text_input(
#                             f"Today's Target ({row})",
#                             value=st.session_state.data[row]["today_target"],
#                             placeholder="₹ Enter Today Target",
#                             key=f"today_target_{row}"
#                         )
#                         st.session_state.data[row]["today_target"] = today_target_input
#                         st.session_state.data[row]["target"] = ""
#                 with cols[3]:
#                     st.session_state.data[row]["cases"] = st.text_input(
#                         f"Count ({row})",
#                         value=st.session_state.data[row]["cases"],
#                         placeholder="Enter Count",
#                         key=f"cases_{row}"
#                     )
#                 with cols[4]:
#                     if image_type == "Till Time":
#                         till_date_ach_input = st.text_input(
#                             f"Till Date Ach ({row})",
#                             value=st.session_state.data[row]["till_date_ach"],
#                             placeholder="₹ Enter Till Date Ach",
#                             key=f"till_date_ach_{row}"
#                         )
#                         st.session_state.data[row]["till_date_ach"] = till_date_ach_input
#                         st.session_state.data[row]["revenue"] = ""
#                     else:
#                         revenue_input = st.text_input(
#                             f"Revenue ({row})",
#                             value=st.session_state.data[row]["revenue"],
#                             placeholder="₹ Enter Revenue",
#                             key=f"revenue_{row}"
#                         )
#                         st.session_state.data[row]["revenue"] = revenue_input
#                         st.session_state.data[row]["till_date_ach"] = ""
                
#                 # Calculate percentage for all rows
#                 if image_type == "Till Time":
#                     st.session_state.data[row]["percent"] = calculate_percentage(st.session_state.data[row]["till_date_ach"], st.session_state.data[row]["target"])
#                 else:
#                     st.session_state.data[row]["percent"] = calculate_percentage(st.session_state.data[row]["revenue"], st.session_state.data[row]["today_target"])
                
#                 # Display calculated percentage (non-editable)
#                 st.markdown(f"**Percent ({row})**: {st.session_state.data[row]['percent']}%")

#                 # Auto-calculate for total row
#                 if row == "total":
#                     try:
#                         if image_type == "Till Time":
#                             st.session_state.data["total"]["total"] = str(int(float(st.session_state.data["row1"]["total"].replace(",", "")) + float(st.session_state.data["row2"]["total"].replace(",", ""))))
#                         else:
#                             st.session_state.data["total"]["total"] = ""
#                     except (ValueError, AttributeError):
#                         st.session_state.data["total"]["total"] = ""
#                     try:
#                         if image_type == "Till Time":
#                             st.session_state.data["total"]["target"] = str(int(float(st.session_state.data["row1"]["target"].replace(",", "")) + float(st.session_state.data["row2"]["target"].replace(",", ""))))
#                         else:
#                             st.session_state.data["total"]["today_target"] = str(int(float(st.session_state.data["row1"]["today_target"].replace(",", "")) + float(st.session_state.data["row2"]["today_target"].replace(",", ""))))
#                     except (ValueError, AttributeError):
#                         st.session_state.data["total"]["target"] = ""
#                         st.session_state.data["total"]["today_target"] = ""
#                     try:
#                         st.session_state.data["total"]["cases"] = str(int(float(st.session_state.data["row1"]["cases"].replace(",", "")) + float(st.session_state.data["row2"]["cases"].replace(",", ""))))
#                     except (ValueError, AttributeError):
#                         st.session_state.data["total"]["cases"] = ""
#                     try:
#                         if image_type == "Till Time":
#                             st.session_state.data["total"]["till_date_ach"] = str(int(float(st.session_state.data["row1"]["till_date_ach"].replace(",", "")) + float(st.session_state.data["row2"]["till_date_ach"].replace(",", ""))))
#                         else:
#                             st.session_state.data["total"]["revenue"] = str(int(float(st.session_state.data["row1"]["revenue"].replace(",", "")) + float(st.session_state.data["row2"]["revenue"].replace(",", ""))))
#                     except (ValueError, AttributeError):
#                         st.session_state.data["total"]["till_date_ach"] = ""
#                         st.session_state.data["total"]["revenue"] = ""
#             st.markdown("---")

#         # Download button with styling
#         if st.button(
#             "Generate and Download Image",
#             key="download_button",
#             help="Generate and download the filled image",
#             use_container_width=True
#         ):
#             all_filled = True
#             required_keys = ["cases"]
#             if image_type == "Till Time":
#                 required_keys.extend(["total", "target", "till_date_ach"])
#             else:
#                 required_keys.extend(["today_target", "revenue"])
#             for row in st.session_state.data.values():
#                 for key in required_keys:
#                     if not row[key]:
#                         all_filled = False
#                         break
#             if not all_filled:
#                 st.error("Please fill in all required fields before generating the image.")
#             else:
#                 filled_image = generate_image(image_type, st.session_state.data)
#                 img_byte_arr = io.BytesIO()
#                 filled_image.save(img_byte_arr, format='JPEG')
#                 img_byte_arr = img_byte_arr.getvalue()
#                 st.download_button(
#                     label="Download Filled Image",
#                     data=img_byte_arr,
#                     file_name=f"sales_team_{image_type.lower().replace(' ', '_')}_filled.jpg",
#                     mime="image/jpeg",
#                     key="download_image_button",
#                     use_container_width=True
#                 )
#                 st.success("Image generated! Click the button above to download.")

#     with col2:
#         st.markdown("#### Image Preview")
#         # Generate and display preview
#         try:
#             preview_image = generate_image(image_type, st.session_state.data)
#             st.image(preview_image, caption=f"Preview of {image_type} Image", use_container_width =True)
#         except Exception as e:
#             st.warning("Unable to generate preview. Please ensure all images are available.")
#         st.markdown("---")
#         st.markdown(
#             "<p style='text-align: center; color: #566573;'>Preview updates automatically as you enter data</p>",
#             unsafe_allow_html=True
#         )

# # Footer
# st.markdown("""
#     <hr style='margin-top: 50px;'>
#     <p style='text-align: center; color: #566573;'>
#         Powered by Streamlit | Created for Sales Team Performance Tracking
#     </p>
# """, unsafe_allow_html=True)


import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Set page configuration for wide layout
st.set_page_config(
    page_title="Sales Team Image Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit app title with styling
st.markdown("""
    <h1 style='text-align: center; color: #2E4053; margin-bottom: 10px;'>
        Sales Team Target vs Achievement Image Generator
    </h1>
    <p style='text-align: center; color: #566573; margin-bottom: 30px;'>
        Create professional sales performance images with ease
    </p>
""", unsafe_allow_html=True)

# Font loader with specified size
# Font loader with specified size
def load_font(size):
    try:
        return ImageFont.truetype("fonts/RobotoCondensed-Bold.ttf", size)
    except:
        try:
            return ImageFont.truetype("fonts/DejaVuSans-Bold.ttf", size)
        except:
            return ImageFont.load_default()

# Function to format numbers with commas (Indian style: 12,30,56,789)
def format_indian_number(number_str):
    try:
        num = int(float(number_str.replace(",", "")))
        num_str = str(num)
        if len(num_str) <= 3:
            return num_str
        result = num_str[-3:]
        remaining = num_str[:-3]
        while remaining:
            result = remaining[-2:] + "," + result
            remaining = remaining[:-2]
        return result
    except (ValueError, AttributeError):
        return number_str

# Function to calculate percentage
def calculate_percentage(achieved, target):
    try:
        achieved = float(achieved.replace(",", ""))
        target = float(target.replace(",", ""))
        if target == 0:
            return "0"
        return f"{(achieved / target * 100):.2f}"
    except (ValueError, AttributeError):
        return ""

# Coordinates for Till Time image (ACTUAL_REGION_REVENUE_blank.jpg) - unchanged
positions_till_time = {
    "row1": {
        "total": (550, 768, 40),
        "target": (759, 768, 44),
        "cases": (1010, 768, 40),
        "till_date_ach": (1232, 768, 44),
        "percent": (1460, 778, 32)
    },
    "row2": {
        "total": (550, 1000, 40),
        "target": (759, 1000, 44),
        "cases": (1010, 1000, 40),
        "till_date_ach": (1232, 1000, 44),
        "percent": (1460, 1000, 32)
    },
    "total": {
        "total": (550, 1155, 40),
        "target": (759, 1155, 44),
        "cases": (1010, 1155, 40),
        "till_date_ach": (1232, 1155, 44),
        "percent": (1460, 1155, 32)
    }
}

# Coordinates for Today image (today.jpg) with 4 columns: today_target, cases, revenue, percent
positions_today = {
    "row1": {
        "today_target": (650, 768, 44),
        "cases": (900, 768, 40),
        "revenue": (1150, 768, 44),
        "percent": (1400, 768, 32)
    },
    "row2": {
        "today_target": (650, 1000, 44),
        "cases": (900, 1000, 40),
        "revenue": (1150, 1000, 44),
        "percent": (1400, 1000, 32)
    },
    "total": {
        "today_target": (650, 1155, 44),
        "cases": (900, 1155, 40),
        "revenue": (1150, 1155, 44),
        "percent": (1400, 1155, 32)
    }
}

# Region positions (before the total column, only for row1 and row2)
region_positions = {
    "row1": (-185, 700, 46),
    "row2": (-185, 935, 46)
}

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = {
        "row1": {
            "region_image": "None", "total": "", "target": "", "today_target": "", "cases": "", "till_date_ach": "", "revenue": "", "percent": ""
        },
        "row2": {
            "region_image": "None", "total": "", "target": "", "today_target": "", "cases": "", "till_date_ach": "", "revenue": "", "percent": ""
        },
        "total": {
            "total": "", "target": "", "today_target": "", "cases": "", "till_date_ach": "", "revenue": "", "percent": ""
        }
    }

# Function to resize image with contain style (maintain aspect ratio, no cropping)
def resize_image_contain(image, target_size):
    target_width, target_height = target_size
    img_width, img_height = image.size
    aspect_ratio = img_width / img_height
    target_aspect = target_width / target_height

    # Scale to fit within target dimensions
    if aspect_ratio > target_aspect:
        # Image is wider, scale by width
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
    else:
        # Image is taller, scale by height
        new_height = target_height
        new_width = int(new_height * aspect_ratio)

    # Resize image
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a new image with transparent background
    new_image = Image.new("RGBA", target_size, (0, 0, 0, 0))
    # Paste the resized image in the center
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    new_image.paste(image, (paste_x, paste_y))

    return new_image

# Function to generate the image
def generate_image(image_type, data):
    # Load the base image
    image = Image.open("ACTUAL_REGION_REVENUE_blank.jpg" if image_type == "Till Time" else "today.jpg")
    draw = ImageDraw.Draw(image)

    # Paste region images for row1 and row2
    for row, (x, y, font_size) in region_positions.items():
        region_image_path = data[row]["region_image"]
        if region_image_path != "None":
            try:
                region_img = Image.open(region_image_path)
                # Resize with contain style to a smaller size (1200x250)
                region_img = resize_image_contain(region_img, (1200, 250))
                # Center the image at the specified coordinates
                paste_x = x - 75  # Half of target width (150/2)
                paste_y = y - 20  # Half of target height (40/2)
                image.paste(region_img, (paste_x, paste_y), region_img if region_img.mode == "RGBA" else None)
            except:
                st.warning(f"Failed to load region image for {row}. Proceeding without it.")

    positions = positions_till_time if image_type == "Till Time" else positions_today

    # Draw the values with centered text and fixed color
    text_color = (245, 254, 220)  # RGB color for all text
    for row, cols in positions.items():
        for key, (x, y, font_size) in cols.items():
            font = load_font(font_size)
            # Format the text with prefix/suffix and commas where applicable
            if key in ["target", "today_target", "till_date_ach", "revenue"]:
                formatted_value = format_indian_number(data[row][key])
                text = f"₹{formatted_value}" if data[row][key] else ""
            elif key == "percent":
                text = f"{data[row][key]}%" if data[row][key] else ""
            else:
                text = data[row][key]

            if not text:
                continue

            # Get text bounding box to calculate width for centering
            try:
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
            except AttributeError:
                text_width = draw.textsize(text, font=font)[0]

            centered_x = x - (text_width // 2)
            draw.text((centered_x, y), text, fill=text_color, font=font)

    return image

# Main container for layout
with st.container():
    # Create two columns for inputs and preview
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        # Image type selection with styling
        st.markdown("#### Select Image Type")
        image_type = st.selectbox(
            "",
            ["Till Time", "Today"],
            key="image_type",
            help="Choose whether to generate a Till Time or Today image"
        )
        st.markdown("---")

        # Create input forms for each row
        for row in ["row1", "row2", "total"]:
            st.markdown(f"#### Enter Data for {row.capitalize()}")
            # Use container for input fields to control width
            with st.container():
                # Create columns for input fields with adjusted widths
                cols = st.columns([2, 2, 2, 2, 2])
                with cols[0]:
                    # Region image selection only for row1 and row2
                    if row in ["row1", "row2"]:
                        st.session_state.data[row]["region_image"] = st.selectbox(
                            f"Region Image ({row})",
                            ["None", "SRIRAM JOSHI.png", "BHAVIK GANATRA.png"],
                            index=["None", "SRIRAM JOSHI.png", "BHAVIK GANATRA.png"].index(st.session_state.data[row]["region_image"]),
                            key=f"region_image_{row}",
                            help="Select an image for the region"
                        )
                with cols[1]:
                    if image_type == "Till Time":
                        st.session_state.data[row]["total"] = st.text_input(
                            f"Total ({row})",
                            value=st.session_state.data[row]["total"],
                            placeholder="Enter Total",
                            key=f"total_{row}"
                        )
                    else:
                        # For "Today", we don't need Total, so hide this field
                        st.session_state.data[row]["total"] = ""
                with cols[2]:
                    if image_type == "Till Time":
                        target_input = st.text_input(
                            f"Target ({row})",
                            value=st.session_state.data[row]["target"],
                            placeholder="₹ Enter Target",
                            key=f"target_{row}"
                        )
                        st.session_state.data[row]["target"] = target_input
                        st.session_state.data[row]["today_target"] = ""
                    else:
                        today_target_input = st.text_input(
                            f"Today's Target ({row})",
                            value=st.session_state.data[row]["today_target"],
                            placeholder="₹ Enter Today Target",
                            key=f"today_target_{row}"
                        )
                        st.session_state.data[row]["today_target"] = today_target_input
                        st.session_state.data[row]["target"] = ""
                with cols[3]:
                    st.session_state.data[row]["cases"] = st.text_input(
                        f"Count ({row})",
                        value=st.session_state.data[row]["cases"],
                        placeholder="Enter Count",
                        key=f"cases_{row}"
                    )
                with cols[4]:
                    if image_type == "Till Time":
                        till_date_ach_input = st.text_input(
                            f"Till Date Ach ({row})",
                            value=st.session_state.data[row]["till_date_ach"],
                            placeholder="₹ Enter Till Date Ach",
                            key=f"till_date_ach_{row}"
                        )
                        st.session_state.data[row]["till_date_ach"] = till_date_ach_input
                        st.session_state.data[row]["revenue"] = ""
                    else:
                        revenue_input = st.text_input(
                            f"Revenue ({row})",
                            value=st.session_state.data[row]["revenue"],
                            placeholder="₹ Enter Revenue",
                            key=f"revenue_{row}"
                        )
                        st.session_state.data[row]["revenue"] = revenue_input
                        st.session_state.data[row]["till_date_ach"] = ""
                
                # Calculate percentage for all rows
                if image_type == "Till Time":
                    st.session_state.data[row]["percent"] = calculate_percentage(st.session_state.data[row]["till_date_ach"], st.session_state.data[row]["target"])
                else:
                    st.session_state.data[row]["percent"] = calculate_percentage(st.session_state.data[row]["revenue"], st.session_state.data[row]["today_target"])
                
                # Display calculated percentage (non-editable)
                st.markdown(f"**Percent ({row})**: {st.session_state.data[row]['percent']}%")

                # Auto-calculate for total row
                if row == "total":
                    try:
                        if image_type == "Till Time":
                            st.session_state.data["total"]["total"] = str(int(float(st.session_state.data["row1"]["total"].replace(",", "")) + float(st.session_state.data["row2"]["total"].replace(",", ""))))
                        else:
                            st.session_state.data["total"]["total"] = ""
                    except (ValueError, AttributeError):
                        st.session_state.data["total"]["total"] = ""
                    try:
                        if image_type == "Till Time":
                            st.session_state.data["total"]["target"] = str(int(float(st.session_state.data["row1"]["target"].replace(",", "")) + float(st.session_state.data["row2"]["target"].replace(",", ""))))
                        else:
                            st.session_state.data["total"]["today_target"] = str(int(float(st.session_state.data["row1"]["today_target"].replace(",", "")) + float(st.session_state.data["row2"]["today_target"].replace(",", ""))))
                    except (ValueError, AttributeError):
                        st.session_state.data["total"]["target"] = ""
                        st.session_state.data["total"]["today_target"] = ""
                    try:
                        st.session_state.data["total"]["cases"] = str(int(float(st.session_state.data["row1"]["cases"].replace(",", "")) + float(st.session_state.data["row2"]["cases"].replace(",", ""))))
                    except (ValueError, AttributeError):
                        st.session_state.data["total"]["cases"] = ""
                    try:
                        if image_type == "Till Time":
                            st.session_state.data["total"]["till_date_ach"] = str(int(float(st.session_state.data["row1"]["till_date_ach"].replace(",", "")) + float(st.session_state.data["row2"]["till_date_ach"].replace(",", ""))))
                        else:
                            st.session_state.data["total"]["revenue"] = str(int(float(st.session_state.data["row1"]["revenue"].replace(",", "")) + float(st.session_state.data["row2"]["revenue"].replace(",", ""))))
                    except (ValueError, AttributeError):
                        st.session_state.data["total"]["till_date_ach"] = ""
                        st.session_state.data["total"]["revenue"] = ""
            st.markdown("---")

        # Download button with styling
        if st.button(
            "Generate and Download Image",
            key="download_button",
            help="Generate and download the filled image",
            use_container_width=True
        ):
            all_filled = True
            required_keys = ["cases"]
            if image_type == "Till Time":
                required_keys.extend(["total", "target", "till_date_ach"])
            else:
                required_keys.extend(["today_target", "revenue"])
            for row in st.session_state.data.values():
                for key in required_keys:
                    if not row[key]:
                        all_filled = False
                        break
            if not all_filled:
                st.error("Please fill in all required fields before generating the image.")
            else:
                filled_image = generate_image(image_type, st.session_state.data)
                img_byte_arr = io.BytesIO()
                filled_image.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                st.download_button(
                    label="Download Filled Image",
                    data=img_byte_arr,
                    file_name=f"sales_team_{image_type.lower().replace(' ', '_')}_filled.jpg",
                    mime="image/jpeg",
                    key="download_image_button",
                    use_container_width=True
                )
                st.success("Image generated! Click the button above to download.")

    with col2:
        st.markdown("#### Image Preview")
        # Generate and display preview
        try:
            preview_image = generate_image(image_type, st.session_state.data)
            st.image(preview_image, caption=f"Preview of {image_type} Image", use_column_width=True)
        except Exception as e:
            st.warning("Unable to generate preview. Please ensure all images are available.")
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: #566573;'>Preview updates automatically as you enter data</p>",
            unsafe_allow_html=True
        )

# Footer
st.markdown("""
    <hr style='margin-top: 50px;'>
    <p style='text-align: center; color: #566573;'>
        Powered by Streamlit | Created for Sales Team Performance Tracking
    </p>
""", unsafe_allow_html=True)
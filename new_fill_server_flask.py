import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Sales Team Image Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- App Title and Description ---
st.markdown("""
    <h1 style='text-align: center; color: #2E4053; margin-bottom: 10px;'>
        Sales Team Target vs Achievement Image Generator
    </h1>
    <p style='text-align: center; color: #566573; margin-bottom: 30px;'>
        Create professional sales performance images with ease
    </p>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def load_font(size):
    """Load a sharp font (Roboto Condensed Bold) with fallbacks."""
    try:
        return ImageFont.truetype("fonts/RobotoCondensed-Bold.ttf", size)
    except:
        try:
            return ImageFont.truetype("fonts/DejaVuSans-Bold.ttf", size)
        except:
            return ImageFont.load_default()

def format_indian_number(number_str):
    """Format numbers in Indian style (e.g., 12,34,56,789)."""
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

def calculate_percentage(achieved, target):
    """Calculate percentage of achieved vs target."""
    try:
        # Strip currency symbol (₹), commas, and whitespace
        achieved_cleaned = achieved.replace("₹", "").replace(",", "").strip()
        target_cleaned = target.replace("₹", "").replace(",", "").strip()
        achieved_num = float(achieved_cleaned)
        target_num = float(target_cleaned)
        return "0" if target_num == 0 else f"{(achieved_num / target_num * 100):.2f}"
    except (ValueError, AttributeError):
        return ""
    
def resize_image_contain(image, target_size):
    """Resize image while maintaining aspect ratio (contain style)."""
    target_width, target_height = target_size
    img_width, img_height = image.size
    aspect_ratio = img_width / img_height
    target_aspect = target_width / target_height

    if aspect_ratio > target_aspect:
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)

    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    new_image = Image.new("RGBA", target_size, (0, 0, 0, 0))
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    new_image.paste(image, (paste_x, paste_y))
    return new_image

def generate_image(image_type, data):
    """Generate the filled image based on user inputs."""
    image = Image.open("ACTUAL_REGION_REVENUE_blank.jpg" if image_type == "Till Time" else "today.jpg")
    draw = ImageDraw.Draw(image)

    # Paste region images for row1 and row2
    for row, (x, y, font_size) in region_positions.items():
        region_image_path = data[row]["region_image"]
        if region_image_path != "None":
            try:
                region_img = Image.open(region_image_path)
                region_img = resize_image_contain(region_img, (1200, 250))
                paste_x = x - 75
                paste_y = y - 20
                image.paste(region_img, (paste_x, paste_y), region_img if region_img.mode == "RGBA" else None)
            except:
                st.warning(f"Failed to load region image for {row}. Proceeding without it.")

    positions = positions_till_time if image_type == "Till Time" else positions_today
    text_color = (245, 254, 220)  # RGB color for all text

    for row, cols in positions.items():
        for key, (x, y, font_size) in cols.items():
            font = load_font(font_size)
            if key in ["target", "today_target", "till_date_ach", "revenue"]:
                raw_value = data[row][key]
                if not raw_value:
                    text = ""
                else:
                    # Strip currency symbol (₹) and commas if present
                    cleaned_value = raw_value.replace("₹", "").replace(",", "").strip()
                    # Format the number in Indian style
                    formatted_value = format_indian_number(cleaned_value)
                    # Always add the ₹ symbol, whether user included it or not
                    text = f"₹{formatted_value}" if formatted_value else ""
            elif key == "percent":
                text = f"{data[row][key]}%" if data[row][key] else ""
            else:
                text = data[row][key]

            if not text:
                continue

            try:
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
            except AttributeError:
                text_width = draw.textsize(text, font=font)[0]

            centered_x = x - (text_width // 2)
            draw.text((centered_x, y), text, fill=text_color, font=font)

    return image

# --- Coordinates for Image Text Placement ---
positions_till_time = {
    "row1": {
        "total": (550, 768, 34),
        "target": (759, 768, 36),
        "cases": (1010, 768, 34),
        "till_date_ach": (1232, 768, 36),
        "percent": (1460, 773, 32)
    },
    "row2": {
        "total": (550, 1000, 34),
        "target": (759, 1000, 36),
        "cases": (1010, 1000, 34),
        "till_date_ach": (1232, 1000, 36),
        "percent": (1460, 1005, 32)
    },
    "total": {
        "total": (550, 1166, 34),
        "target": (759, 1166, 36),
        "cases": (1010, 1166, 34),
        "till_date_ach": (1232, 1166, 36),
        "percent": (1460, 1169, 32)
    }
}

positions_today = {
    "row1": {
        "today_target": (650, 771, 40),
        "cases": (940, 771, 36),
        "revenue": (1190, 771, 40),
        "percent": (1460, 776, 30)
    },
    "row2": {
        "today_target": (650, 1000, 40),
        "cases": (940, 1000, 36),
        "revenue": (1190, 1000, 40),
        "percent": (1460, 1007, 30)
    },
    "total": {
        "today_target": (650, 1160, 40),
        "cases": (940, 1160, 36),
        "revenue": (1190, 1160, 40),
        "percent": (1460, 1163, 30)
    }
}

region_positions = {
    "row1": (-185, 700, 46),
    "row2": (-185, 935, 46)
}

# --- Initialize Session State ---
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

# --- Main Layout ---
with st.container():
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        # Image Type Selection
        st.markdown("#### Select Image Type")
        image_type = st.selectbox(
            "",
            ["Till Time", "Today"],
            key="image_type",
            help="Choose whether to generate a Till Time or Today image"
        )
        st.markdown("---")

        # Input Forms for Each Row
        rows = ["row1", "row2", "total"]
        is_till_time = image_type == "Till Time"

        for row in rows:
            st.markdown(f"#### Enter Data for {row.capitalize()}")
            with st.container():
                cols = st.columns([2, 2, 2, 2, 2])

                # Region Image (for row1 and row2 only)
                if row in ["row1", "row2"]:
                    with cols[0]:
                        st.session_state.data[row]["region_image"] = st.selectbox(
                            f"Region Image ({row})",
                            ["None", "SRIRAM JOSHI.png", "BHAVIK GANATRA.png"],
                            index=["None", "SRIRAM JOSHI.png", "BHAVIK GANATRA.png"].index(st.session_state.data[row]["region_image"]),
                            key=f"region_image_{row}",
                            help="Select an image for the region"
                        )

                # Total (only for Till Time)
                with cols[1]:
                    if is_till_time and row != "total":
                        st.session_state.data[row]["total"] = st.text_input(
                            f"Total ({row})",
                            value=st.session_state.data[row]["total"],
                            placeholder="Enter Total",
                            key=f"total_{row}"
                        )
                    else:
                        st.session_state.data[row]["total"] = ""

                # Target or Today's Target
                with cols[2]:
                    if is_till_time:
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

                # Cases (Count)
                with cols[3]:
                    st.session_state.data[row]["cases"] = st.text_input(
                        f"Count ({row})",
                        value=st.session_state.data[row]["cases"],
                        placeholder="Enter Count",
                        key=f"cases_{row}"
                    )

                # Till Date Ach or Revenue
                with cols[4]:
                    if is_till_time:
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

                # Calculate percentage for row1 and row2
                if row in ["row1", "row2"]:
                    if is_till_time:
                        st.session_state.data[row]["percent"] = calculate_percentage(
                            st.session_state.data[row]["till_date_ach"],
                            st.session_state.data[row]["target"]
                        )
                    else:
                        st.session_state.data[row]["percent"] = calculate_percentage(
                            st.session_state.data[row]["revenue"],
                            st.session_state.data[row]["today_target"]
                        )

                # Display percentage
                st.markdown(f"**Percent ({row})**: {st.session_state.data[row]['percent']}%")

            st.markdown("---")

        # Auto-calculate totals for the "Total" row
        # Auto-calculate totals for the "Total" row
        try:
            if is_till_time:
                # Clean inputs by removing ₹ and commas
                total1 = float(st.session_state.data["row1"]["total"].replace("₹", "").replace(",", "").strip())
                total2 = float(st.session_state.data["row2"]["total"].replace("₹", "").replace(",", "").strip())
                target1 = float(st.session_state.data["row1"]["target"].replace("₹", "").replace(",", "").strip())
                target2 = float(st.session_state.data["row2"]["target"].replace("₹", "").replace(",", "").strip())
                till_date_ach1 = float(st.session_state.data["row1"]["till_date_ach"].replace("₹", "").replace(",", "").strip())
                till_date_ach2 = float(st.session_state.data["row2"]["till_date_ach"].replace("₹", "").replace(",", "").strip())
        
                total_total = int(total1 + total2)
                total_target = int(target1 + target2)
                total_till_date_ach = int(till_date_ach1 + till_date_ach2)
        
                st.session_state.data["total"]["total"] = str(total_total)
                st.session_state.data["total"]["target"] = str(total_target)
                st.session_state.data["total"]["today_target"] = ""
                st.session_state.data["total"]["till_date_ach"] = str(total_till_date_ach)
                st.session_state.data["total"]["revenue"] = ""
                # Calculate total percentage for Till Time
                st.session_state.data["total"]["percent"] = calculate_percentage(
                    str(total_till_date_ach),  # Pass as string since calculate_percentage expects string input
                    str(total_target)
                )
            else:
                # Clean inputs by removing ₹ and commas
                today_target1 = float(st.session_state.data["row1"]["today_target"].replace("₹", "").replace(",", "").strip())
                today_target2 = float(st.session_state.data["row2"]["today_target"].replace("₹", "").replace(",", "").strip())
                revenue1 = float(st.session_state.data["row1"]["revenue"].replace("₹", "").replace(",", "").strip())
                revenue2 = float(st.session_state.data["row2"]["revenue"].replace("₹", "").replace(",", "").strip())
        
                total_today_target = int(today_target1 + today_target2)
                total_revenue = int(revenue1 + revenue2)
        
                st.session_state.data["total"]["total"] = ""
                st.session_state.data["total"]["target"] = ""
                st.session_state.data["total"]["today_target"] = str(total_today_target)
                st.session_state.data["total"]["till_date_ach"] = ""
                st.session_state.data["total"]["revenue"] = str(total_revenue)
                # Calculate total percentage for Today
                st.session_state.data["total"]["percent"] = calculate_percentage(
                    str(total_revenue),  # Pass as string since calculate_percentage expects string input
                    str(total_today_target)
                )
        except (ValueError, AttributeError):
            # Reset total row if calculations fail
            st.session_state.data["total"]["total"] = ""
            st.session_state.data["total"]["target"] = ""
            st.session_state.data["total"]["today_target"] = ""
            st.session_state.data["total"]["till_date_ach"] = ""
            st.session_state.data["total"]["revenue"] = ""
            st.session_state.data["total"]["percent"] = ""
        
        # Update total row cases
        try:
            cases1 = float(st.session_state.data["row1"]["cases"].replace("₹", "").replace(",", "").strip())
            cases2 = float(st.session_state.data["row2"]["cases"].replace("₹", "").replace(",", "").strip())
            total_cases = int(cases1 + cases2)
            st.session_state.data["total"]["cases"] = str(total_cases)
        except (ValueError, AttributeError):
            st.session_state.data["total"]["cases"] = ""

        # Download Button
        # Download Button
        if st.button(
            "Generate and Download Image",
            key="download_button",
            help="Generate and download the filled image",
            use_container_width=True
        ):
            required_keys = ["cases"]
            if is_till_time:
                required_keys.extend(["total", "target", "till_date_ach"])
            else:
                required_keys.extend(["today_target", "revenue"])       

            all_filled = all(
                st.session_state.data[row][key]
                for row in st.session_state.data.keys()  # Changed from .values() to .keys()
                for key in required_keys
            )       

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
        try:
            preview_image = generate_image(image_type, st.session_state.data)
            st.image(preview_image, caption=f"Preview of {image_type} Image", use_container_width=True)
        except Exception as e:
            st.warning("Unable to generate preview. Please ensure all images are available.")
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: #566573;'>Preview updates automatically as you enter data</p>",
            unsafe_allow_html=True
        )

# --- Footer ---
st.markdown("""
    <hr style='margin-top: 50px;'>
    <p style='text-align: center; color: #566573;'>
        Powered by Streamlit | Created for Sales Team Performance Tracking
    </p>
""", unsafe_allow_html=True)
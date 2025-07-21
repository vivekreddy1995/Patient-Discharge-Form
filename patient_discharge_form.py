import streamlit as st
from datetime import date
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage

# Set custom range
min_date = date(1900, 1, 1)
max_date = date(2100, 12, 31)

@st.cache_resource
def initialize_only_once():
    dict = {}
    return dict, "Resource Initialized"

def add_dict():
    dict["Patients Name"] = st.session_state.user_input
    dict["Date of Birth"] = st.session_state.user_input1.strftime("%d-%m-%Y") 
    dict["Medical Record Number"] = st.session_state.user_input2
    dict["Date of Admission"] = st.session_state.user_input3.strftime("%d-%m-%Y")
    dict["Date of Discharge"] = st.session_state.user_input4.strftime("%d-%m-%Y")
    dict["Reason for Admission"] = st.session_state.user_input5
    dict["Procedures Performed"] = st.session_state.user_input6
    dict["Medications Prescribed"] =st.session_state.user_input7
    dict["Patient's Condition at Discharge"] = st.session_state.user_input8
    dict["Follow-up care instructions"] = st.session_state.user_input9
    dict["Summary of hospital stay"] = st.session_state.user_input10

def clear_inputs():
    st.session_state.user_input = ""
    st.session_state.user_input1 = date.today()
    st.session_state.user_input2 = ""
    st.session_state.user_input3 = date.today()
    st.session_state.user_input4 = date.today()
    st.session_state.user_input5 = ""
    st.session_state.user_input6 = ""
    st.session_state.user_input7 = ""
    st.session_state.user_input8 = ""
    st.session_state.user_input9 = ""
    st.session_state.user_input10 = ""

def add_row(pdf, label, value):
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, f"{label}:", ln=0)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, value)

def create_pdf(dict):
    # Define the fields to collect and display in the table
    fields = [
        "Patients Name", "Date of Birth", "Medical Record Number",
        "Date of Admission", "Date of Discharge",
        "Reason for Admission", "Procedures Performed", "Medications Prescribed",
        "Patient's Condition at Discharge", "Follow-up care instructions", "Summary of hospital stay"
    ]

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

    # Upload logo file (PNG, JPG)
    
    logo_file = "logo.jpg"

    with PILImage.open(logo_file) as img:
        img_width, img_height = img.size

    # Target width (full width minus margins)
    target_width = 532  # adjust based on your margins
    aspect_ratio = img_height / img_width
    target_height = target_width * aspect_ratio


    styles = getSampleStyleSheet()
    content = []

    if logo_file is not None:
        logo = Image(logo_file, width=target_width, height=target_height)
        logo.hAlign = "RIGHT"
        content.append(logo)
        content.append(Spacer(1, 10))
    else:
        st.warning("Logo not found at path: {}".format(logo_file))

    # Add PDF heading
    content.append(Paragraph("<b><font size=18>Ramesh Hospitals</font></b>", styles["Title"]))
    content.append(Paragraph("<b><font size=14>Discharge Summary Form</font></b>", styles["Title"]))
    content.append(Spacer(1, 20))

    # Prepare table data (2-column: label | value)
    table_data = [[f, dict[f]] for f in fields]

    # Create table
    table = Table(table_data, colWidths=[150, 350])
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))

    content.append(table)

    # Build PDF
    doc.build(content)
    buffer.seek(0)
    return buffer


dict, result = initialize_only_once()

st.title("Patient Discharge Summary")
name = st.text_input("Enter Patients Name ", key="user_input", on_change =add_dict)
date_of_birth = st.date_input("Date of Birth ", value = date.today(), min_value=min_date, max_value=max_date, key="user_input1", on_change =add_dict)
patient_medical_number= st.text_input("Medical Record Number ", key="user_input2", on_change =add_dict)

date_of_admission = st.date_input("Date of Admission ", value = date.today(),  min_value=min_date, max_value=max_date, key="user_input3", on_change =add_dict)
date_of_discharge = st.date_input("Date of Discharge ", value = date.today(), min_value=min_date, max_value=max_date, key="user_input4", on_change =add_dict)

reason_for_admission = st.text_area("Reason for Admission ", height=200, key="user_input5", on_change =add_dict)
procedures_performed = st.text_area("Procedures Performed ",height=200, key="user_input6", on_change =add_dict)

medications_prescribed = st.text_area("Medications Prescribed ",height=200, key="user_input7", on_change =add_dict)
patients_condition_at_discharge= st.text_area("Patient's Condition at Discharge ",height=200, key="user_input8", on_change =add_dict)

follow_up_care_instructions = st.text_area("Follow-up care instructions ", height = 200, key = "user_input9", on_change=add_dict)
summary_of_hospital_stay = st.text_area("Summary of hospital stay ", height=200, key="user_input10", on_change=add_dict)

if st.button("Save to PDF", on_click=clear_inputs):
    print(dict)
    pdf_data = create_pdf(dict)
    st.download_button(
        label="📄 Download PDF",
        data=pdf_data,
        file_name="{}_{}_discharge_summary.pdf".format(dict["Patients Name"], dict["Medical Record Number"]),
        mime="application/pdf"
    )
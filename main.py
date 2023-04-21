import os
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gmail account information
GMAIL_USERNAME = 'medsken6@gmail.com'
GMAIL_PASSWORD = 'rinseqnfkekfjepn'

# Path to the folder where the PDF files are located
PDF_FOLDER_PATH = 'C:\\Users\\PC\\Downloads\\osiguranja20042023'

# Function to send email with attachment


def send_email(subject, body, to, pdf_path):
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USERNAME
        msg['To'] = to
        msg['Subject'] = subject

        # Attach PDF file to email
        with open(pdf_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
            attach.add_header('Content-Disposition', 'attachment',
                              filename=str(pdf_path.split("/")[-1]))
            msg.attach(attach)

        # Add body to email
        msg.attach(MIMEText(body, 'plain'))

        # Send email using Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USERNAME, to, msg.as_string())
        server.close()

        # Move PDF file to "poslata osiguranja" folder
        new_path = os.path.join(os.path.dirname(
            pdf_path), "poslata osiguranja", os.path.basename(pdf_path))
        os.rename(pdf_path, new_path)

        return "poslato"

    except Exception as e:
        return "greška: " + str(e)


# Get list of PDF files in folder
pdf_files = [f for f in os.listdir(PDF_FOLDER_PATH) if f.endswith('.pdf')]

# Process each PDF file
log = []
for pdf_file in pdf_files:
    pdf_path = os.path.join(PDF_FOLDER_PATH, pdf_file)

    # Get file name parts
    file_parts = pdf_file[:-4].split('_')
    osiguranje = file_parts[0]
    surname = file_parts[1]
    name = file_parts[2]
    mbr = file_parts[3]

    # Set email subject based on file name
    if osiguranje == "dd":
        subject = mbr + " - dokumentacija"
    elif osiguranje == "df":
        subject = mbr + " - faktura"
    else:
        subject = surname + " " + name

    # Send email with PDF attachment

    to = 'recipient-email@example.com'
    body = "Хвала на сарадњи"
    status = send_email(subject, body, to, pdf_path)

    # Add log entry
    log.append((pdf_file, osiguranje, status))

# Print log
print("name\tosiguranje\tstatus")
for entry in log:
    print(entry[0] + "\t" + entry[1] + "\t" + entry[2])

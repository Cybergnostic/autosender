import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE

# Set up dictionary of emails
email_dict = {
    'dd': 'jovan.veljkovic@poliklinikahuman.rs',
    'df': 'jovan.veljkovic@poliklinikahuman.rs',
    'default': 'zuperman018@gmail.com'
}

# Set up folder paths
src_folder = 'C:\\Users\\PC\\Downloads\\osiguranja20042023'
dst_folder = 'C:\\Users\\PC\\Downloads\\osiguranja20042023_poslato'
log_file = 'C:\\Users\\PC\\Downloads\\osiguranja20042023_log.txt'


# Get list of PDFs in source folder
pdfs = [f for f in os.listdir(src_folder) if f.endswith('.pdf')]

# Loop over PDFs and send email for each one
with open(log_file, 'w') as f:
    for pdf in pdfs:
        # Extract information from filename
        parts = pdf.split('_')
        osig = parts[0]
        surname = parts[1]
        name = parts[2]
        mbr = parts[3]
        rbr = parts[4].replace('.pdf', '')

        # Determine email address to send to
        email_to = email_dict.get(osig)

        # Set up message
        msg = MIMEMultipart()
        msg['From'] = 'medsken6@gmail.com'
        msg['To'] = email_to

        # Set subject based on osig
        if osig == 'dd':
            subject = f'{mbr} - dokumentacija'
        elif osig == 'df':
            subject = f'{mbr} - faktura'
        else:
            subject = f'{surname.capitalize()} {name.capitalize()}'
        msg['Subject'] = subject

        # Attach PDF file
        with open(os.path.join(src_folder, pdf), 'rb') as f:
            attach = MIMEApplication(f.read(), _subtype='pdf')
            attach.add_header('Content-Disposition',
                              'attachment', filename=pdf)
            msg.attach(attach)

        # Send email
        try:
            smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.login('medsken6@gmail.com', 'rinseqnfkekfjepn')
            smtp_obj.sendmail('medsken6@gmail.com', email_to, msg.as_string())
            smtp_obj.quit()
            status = 'poslato'

            # Move PDF to destination folder
            os.rename(os.path.join(src_folder, pdf),
                      os.path.join(dst_folder, pdf))
        except Exception as e:
            status = f'greška: {str(e)}'

    # Log status
    log_entry = f'{pdf}\t{osig}\t{status}'
    f.write(log_entry + '\n')

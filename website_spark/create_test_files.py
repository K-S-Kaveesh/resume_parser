from fpdf import FPDF

# Create a simple resume PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'John Doe - Software Engineer', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Create resume
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "Skills:", 0, 1)
pdf.cell(0, 10, "- Python, Java, JavaScript", 0, 1)
pdf.cell(0, 10, "- Flask, Django, React", 0, 1)
pdf.cell(0, 10, "- AWS, Docker", 0, 1)
pdf.cell(0, 10, "- SQL, MongoDB", 0, 1)
pdf.output("test_resume.pdf")

# Create job description
pdf2 = PDF()
pdf2.add_page()
pdf2.set_font("Arial", size=12)
pdf2.cell(0, 10, "Job Requirements:", 0, 1)
pdf2.cell(0, 10, "- Python and Java experience", 0, 1)
pdf2.cell(0, 10, "- Flask and Django frameworks", 0, 1)
pdf2.cell(0, 10, "- AWS experience required", 0, 1)
pdf2.cell(0, 10, "- Docker knowledge preferred", 0, 1)
pdf2.cell(0, 10, "- SQL database experience", 0, 1)
pdf2.output("test_jd.pdf")

print("Test PDF files created successfully!")
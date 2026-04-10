import PyPDF2

pdf_path = r'C:\Users\pere\Documents\programming\mas_assignments\control\TH_problem.pdf'
pdf = PyPDF2.PdfReader(pdf_path)
text = ''.join([page.extract_text() for page in pdf.pages])
print(text)

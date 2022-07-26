from pylatex import Document, Section, Subsection, Command, Package, NewPage, Tabular
from pylatex.utils import italic, NoEscape


if __name__ == '__main__':
    #geometry_options = {"margin": "0.5in"}
    doc = Document('data_dict', 
        # geometry_options=geometry_options,
    )

    doc.packages.append(Package('geometry',options=["margin=0.5in"]))
    # doc.append(NoEscape(r'\addtolength{\oddsidemargin}{-.875in}'))
    # doc.append(NoEscape(r'\addtolength{\evensidemargin}{-.875in}'))
    # doc.append(NoEscape(r'\addtolength{\textwidth}{1.75in}'))
    # doc.append(NoEscape(r'\addtolength{\topmargin}{-.875in}'))
    # doc.append(NoEscape(r'\addtolength{\textheight}{1.75in}'))
    

    doc.packages.append(Package('fontspec'))
    doc.packages.append(Package('xunicode'))
    doc.packages.append(Package('xltxtra'))
    
    doc.append(NoEscape(r'\XeTeXlinebreaklocale "th_TH"'))
    doc.append(NoEscape(r'\XeTeXlinebreakskip = 0pt plus 1pt'))
    doc.append(NoEscape(r'\defaultfontfeatures{Scale=1.23}'))
    doc.append(NoEscape(r'\setmainfont[Mapping=tex-text]{TH SarabunPSK}'))

    #doc.packages.append(Package('xcolor', options=['table']))
    doc.packages.append(Package('color'))
    doc.packages.append(Package('hyperref'))
    doc.append(NoEscape(r'''
        \hypersetup{
            colorlinks=true,
            linktoc=all,
            linkcolor=blue,
            hidelinks
        }
    '''))
    ##end of package

    doc.preamble.append(Command('title', 'Data Dictionary'))
    doc.preamble.append(Command('author', 'Storemesh'))
    doc.preamble.append(Command('date', NoEscape(r'\today\\version 1.0')))

    doc.append(NoEscape(r'\maketitle'))
    doc.append(NewPage())
    
    doc.append(NoEscape(r'\setcounter{secnumdepth}{0}'))
    doc.append(NoEscape(r'\setcounter{tocdepth}{1}'))
    doc.append(NoEscape(r'\tableofcontents'))
    #doc.append(NoEscape('\\tableofcontents'))
    doc.append(NoEscape(r'\newpage'))

    # Add stuff to the document
    d={
        'title':'ชื่อชุดข้อมูล',
        'id': '007',
        'path':'/My Dataset/My Folder/My File',
        'description':'''
            ชุดข้อมูลอาจจะมีเพียงหนึ่งตารางหรือมากกว่านั้น โดยที่ทุกคอลัมน์ของตารางแสดงถึงตัวแปรเฉพาะ ข้อมูลของทุก ๆ แถวจะสอดคล้องกับเอกสารที่กำหนดรายละเอียดของชุดข้อมูล โดยชุดข้อมูลแสดงรายการตามค่าของตัวแปรแต่ละตัว เช่น ความสูงและน้ำหนักของคุณสมบัติสมาชิกของชุดข้อมูลแต่ละตัว นอกจากนั้น ชุดข้อมูลยังสามารถประกอบด้วยชุดของเอกสารหรือไฟล์
            '''
    }
    for i in range(1,4):
        with doc.create(Section('{} {}'.format(d['title'],i))):
            with doc.create(Subsection('Metadata')): 
                with doc.create(Tabular('ll')) as table:
                        #table.add_hline()
                        table.add_row(('DataNode:', d['title']))
                        table.add_row(('ID:', d['id']))
                        table.add_row(('Path:', d['path']))
            
            with doc.create(Subsection('Description')):        
                doc.append(NoEscape(r'''
                    \par{}                
                    '''.format( d['description']) ))

            with doc.create(Subsection('Data Dictionary')):
                    with doc.create(Tabular('c|c|p{3cm}|c|c|p{3cm}')) as table:
                        table.add_hline()
                        table.add_row(('Display Name','Column Name','Description','Relations','Is _Required','Example Data'))
                        table.add_hline()
                        #table.add_row(('Column01','Name',d['description'],'PK','True','1 = Dataset is my data\n2 = Dataset is important\n3 = Dataset is for everyone'))
                        table.add_row(('Column01','Name','Description','PK','True','1 = Dataset is my data\n2 = Dataset is important\n3 = Dataset is for everyone'))
                        table.add_row(('Column01','Name','Description','PK','True','1 = Dataset is my data\n2 = Dataset is important\n3 = Dataset is for everyone'))
            doc.append(NoEscape(r'\newpage'))

    doc.generate_pdf(
            clean=False, 
            compiler='xelatex'
        )
    tex = doc.dumps()  # The document as string in LaTeX syntax

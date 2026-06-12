import camelot
import pymupdf

pdf_path = "data/Housing-Drinking-Water/source.pdf"
i_page = 1

doc = pymupdf.open(pdf_path)
page = doc[0]
width = page.rect.width
height = page.rect.height
words = page.get_text("words")
max_y = max(w[3] for w in words) if words else height
pdf_y_min = height - max_y - 10
table_areas = [f"0,{pdf_y_min},{width},{height}"]
doc.close()

tables = camelot.read_pdf(
    pdf_path,
    pages=str(i_page),
    flavor="stream",
    edge_tol=500,
    row_tol=2,
    strip_text="\n",
    table_areas=table_areas,
)

for table in tables:
    df = table.df
    for idx in range(len(df)):
        row = df.iloc[idx].tolist()
        if any("Pettah" in str(c) for c in row):
            print("ncols:", len(row))
            for j, c in enumerate(row):
                print(j, repr(c))

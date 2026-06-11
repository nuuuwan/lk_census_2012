import camelot
import pandas as pd
import pymupdf

from utils_future import Log

log = Log("oneoff_analyze_pdf")


def main(pdf_path, i_page):

    doc = pymupdf.open(pdf_path)

    dfs = []

    page = doc[i_page - 1]
    width = page.rect.width
    height = page.rect.height

    # Find the actual bottom of content (pymupdf y increases downward)
    words = page.get_text("words")
    if words:
        max_y = max(w[3] for w in words)  # w[3] = y1 of word bbox
    else:
        max_y = height

    # Convert to PDF coordinate space (bottom-left origin)
    # pdf_y = height - pymupdf_y, so bottom of content = height - max_y
    pdf_y_min = height - max_y - 10  # 10pt padding
    table_areas = [f"0,{pdf_y_min},{width},{height}"]

    try:
        tables = camelot.read_pdf(
            pdf_path,
            pages=str(i_page),
            flavor="stream",
            edge_tol=500,
            row_tol=10,
            strip_text="\n",
            table_areas=table_areas,
        )
        for table in tables:
            dfs.append(table.df)
    except Exception as e:
        log.warning(f"Skipping page {i_page}: {e}")

    doc.close()

    if not dfs:
        log.warning(f"No tables found in {pdf_path}")
        return

    df = pd.concat(dfs, ignore_index=True)

    for _, row in df.iterrows():
        line = " | ".join(row.astype(str).tolist())
        log.debug(line)


if __name__ == "__main__":
    main("data/Population-Educational-Attainment/source.pdf", 156)

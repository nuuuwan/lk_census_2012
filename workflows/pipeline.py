from census import PDFSourceFile
from gig_future import Ent


def main():
    Ent.load_hack_cache()
    PDFSourceFile.build_all()
    Ent.store_hack_cache()


if __name__ == "__main__":
    main()

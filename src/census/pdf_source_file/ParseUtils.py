class ParseUtils:

    @staticmethod
    def parse_int(x):
        x = str(x)
        x = x.replace(",", "")
        return int(x)

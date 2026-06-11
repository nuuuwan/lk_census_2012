class ParseUtils:

    @staticmethod
    def parse_int(x):
        x = str(x)
        x = x.replace(",", "")
        if x == "" or x == "-":
            return 0
        return int(x)

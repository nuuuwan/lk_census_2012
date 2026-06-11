class ParseUtils:

    @staticmethod
    def parse_int(x):
        x = str(x)
        x = x.replace(",", "")
        x = x.replace("etc", "")
        if x == "" or x == "-":
            return 0
        x = x.replace(" ", "")
        return int(x)

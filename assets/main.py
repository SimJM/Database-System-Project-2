

def converttbldatatocsvformat(filename, header):
 csv = open("".join(["", filename, ".csv"]), "w+")
 csv.write(header + "\n")
 tbl = open("".join(["", filename, ".tbl"]), "r")
 lines = tbl.readlines()
 for line in lines:
    length = len(line)
    line = line[:length - 2] + line[length-1:]
    line = line.replace(",","N")
    line = line.replace("|",",")
    if line.endswith("|"):
        line = line[:-1]  # Remove the last character
    csv.write(line)
 tbl.close()
 csv.close()



if __name__ == '__main__':
    converttbldatatocsvformat("customer", "customer")
    converttbldatatocsvformat("lineitem","lineitem")
    converttbldatatocsvformat("nation", "nation")
    converttbldatatocsvformat("orders", "orders")
    converttbldatatocsvformat("part", "part")
    converttbldatatocsvformat("partsupp", "partsupp")
    converttbldatatocsvformat("region", "region")
    converttbldatatocsvformat("supplier", "supplier")
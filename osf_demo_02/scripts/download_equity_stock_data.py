import intailize_database_and_Tables as db_setUP
import reintialize_mysql_tables as Update_Tables
import urllib.request



DATABASE_NOT_CREATED=True
def main():
# today = datetime.datetime.now().strftime("%y%m%d%H%M%S")

# Nasdaq Markets
    nasdaq_traded_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt"
    psx_traded_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/psxtraded.txt"
    bx_traded_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/bxtraded.txt"

    # nasdaq_traded_filename = "../../data/nasdaqtraded.txt"
    # psx_traded_filename = "../../data/psxtraded.txt"
    # bx_traded_filename = "../../data/bxtraded.txt"
    dataPath = "/Users/conradscomputer/Desktop/Fintech/osfutils_dev/osf_demo_02/data"
    nasdaq_traded_filename = f"{dataPath}/nasdaqtraded.txt"
    psx_traded_filename = f"{dataPath}/psxtraded.txt"
    bx_traded_filename = f"{dataPath}/bxtraded.txt"

    try:
        urllib.request.urlretrieve(nasdaq_traded_url, nasdaq_traded_filename)
        urllib.request.urlretrieve(psx_traded_url, psx_traded_filename)
        urllib.request.urlretrieve(bx_traded_url, bx_traded_filename)
        print("All market files downloaded successfully.")
    except urllib.error.URLError as e:
        print("Error downloading Nasdaq market files: " + str( e))

    if DATABASE_NOT_CREATED :
        db_setUP.main()

    Update_Tables.main( nasdaq_traded_filename, "nasdaq")
    Update_Tables.main(bx_traded_filename, "BX")
    Update_Tables.main(psx_traded_filename,"PHLX")

if __name__ == "__main__":
    main()
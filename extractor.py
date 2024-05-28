from banks.hdfc import HDFCstatementExtractor
from banks.kotak import KotakstatementExtractor

switch = {
    'HDFC' : HDFCstatementExtractor,
    'Kotak' : KotakstatementExtractor
}

def statementExtractor(bank, filePath):
    if bank in switch:
        return switch[bank](filePath)
    else:
        return "Bank not found"

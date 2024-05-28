from extractor import statementExtractor
from identifier import bankIdentifier

filePath = "samples/Statement April-Aug 2021.pdf"

bank = bankIdentifier(filePath)

statement = statementExtractor(bank, filePath)

print(statement)

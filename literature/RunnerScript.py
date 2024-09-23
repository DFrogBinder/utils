from DuplicateRemover import Parser
from PaperCounter import *

Parser = Parser('Data')
Parser.LoadData()
Parser.FilterTitle(save_data=True)

import os
from ofxstatement.plugins.hypeMovementsPdfParser import HypeMovementsPdfStatementParser

from ofxstatement.plugin import Plugin

class HypePlugin(Plugin):
    """Hype"""

    def get_parser(self, filename: str):
        extension = os.path.splitext(filename)[1]

        if extension == '.pdf':
            required_columns = [
                "Data Operazione",
                "Data Contabile",
                "Tipologia",
                "Nome",
                "Descrizione",
                "Importo"
            ]
                    
            parser = HypeMovementsPdfStatementParser(filename)
            parser.columns = {col: required_columns.index(col) for col in required_columns}
            if 'account' in self.settings:
                parser.statement.account_id = self.settings['account']
            else:
                parser.statement.account_id = 'Hype'

            if 'currency' in self.settings:
                parser.statement.currency = self.settings.get('currency', 'EUR')

            if 'date_format' in self.settings:
                parser.date_format = self.settings['date_format']
            
            parser.statement.bank_id = self.settings.get('bank', 'Hype')
            return parser
        else:
            print('Unsupported file type')
    
        
from ast import Dict
import logging
from typing import Optional, Any, List
from decimal import Decimal, InvalidOperation
import pandas
import tabula
import PyPDF2

from ofxstatement.parser import StatementParser
from ofxstatement.statement import StatementLine, Currency, Statement
from ofxstatement.plugins.hypeTransaction import HypeTransaction, TransactionType

DESCRIPTION_TYPE_MAP = {
    "BONIFICO ORDINARIO": TransactionType.BONIFICO,
    "BONIFICO ESTERO": TransactionType.BONIFICO,
    "BONIFICO ISTANTANEO": TransactionType.BONIFICO,
    "PAGAMENTO": TransactionType.PAGAMENTO,
    "ADDEBITO DIRETTO": TransactionType.ADDEBITO_DIRETTO,
    "RIMBORSO": TransactionType.RIMBORSO,
    "COMMISSIONE": TransactionType.COMMISSIONE,
    "BOLLO": TransactionType.BOLLO,
    "DENARO RICEVUTO": TransactionType.BONIFICO,
    "DENARO INVIATO": TransactionType.BONIFICO,
    "ALTRO": TransactionType.OTHER,
    "CANONE": TransactionType.OTHER,
    "RICARICA CARTA": TransactionType.RICARICA_CARTA,
}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Hype')
GITHUB_URL = "https://github.com/lorenzogiudici5/ofxstatement-hype"

class HypeMovementsPdfStatementParser(StatementParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
    
    date_format = "%d/%m/%Y"

    def parse_currency(self, value: Optional[str]) -> Currency:
        return Currency(symbol=value)
    
    def parse_amount(self, value: str) -> Decimal:
        try:
            # if value is Float or Integer, return it
            if isinstance(value, float) or isinstance(value, int):
                return Decimal(value)
            
            result = Decimal(value.replace(" ", "").replace(".", "").replace(",", "."))
            if result.is_nan():
                return Decimal(0)
            else:
                return result
        except (InvalidOperation, TypeError):
            return Decimal(0)

    def parse_value(self, value: Optional[str], field: str) -> Any:
        value = value.strip() if value else value

        if field == "date":
            # check if value is a date in the format dd/mm/yy
            if value and len(value) == 10 and value[2] == "/" and value[5] == "/":
                return super().parse_value(value, field)
            else:
                return None

        if field == "amount":
            return self.parse_amount(value)

        if field == "currency":
            return self.parse_currency(value)

        return super().parse_value(value, field)
    
    def split_records(self) -> List[Dict]:
        dataFrame = tabula.read_pdf(self.filename, multiple_tables=False, pages="all", stream=True, pandas_options={'header': None, 'names': self.columns})
        
        if(len(dataFrame) == 0):
            logger.error("Error: no data found in pdf file")
            return []
        
        df = pandas.concat(dataFrame)
        df = df.astype(str)
             
        # Create a new DataFrame to store the result
        dfresult = pandas.DataFrame(columns=self.columns)

        # Iterate over the rows of the DataFrame
        i = 0
        while i < len(df):
            row = df.iloc[i]

            data = row["Data Operazione"]
            valuta = row["Data Contabile"]
            #if data is not a date in the format dd/mm/yy, it is not a transaction
            if data is None or len(data) != 10 or data[2] != "/" or data[5] != "/":
                i += 1
                continue
        
            type = row["Tipologia"]
            amount = row["Importo"]
            if(amount.startswith("-")):
                addebiti = amount[1:-1]
                accrediti = 0

            if(amount.startswith("+")):
                accrediti = amount[1:-1]
                addebiti = 0

            name = row["Nome"]
            memo = row["Descrizione"]

            j = 1
            if amount == "nan":
                while df.iloc[i+j]["Data Contabile"] == "nan":
                    if df.iloc[i+j]["Tipologia"] != "nan":
                        type = type + " " + df.iloc[i+j]["Tipologia"]
                    if df.iloc[i+j]["Descrizione"] != "nan":
                        memo = memo + " " + df.iloc[i+j]["Descrizione"]
                    if df.iloc[i+j]["Nome"] != "nan":
                        name = name + " " + df.iloc[i+j]["Nome"]
                    if df.iloc[i+j]["Importo"] != "nan":
                        amount = df.iloc[i+j]["Importo"]
                        if(amount.startswith("-")):
                            addebiti = amount[1:-1]
                            accrediti = 0
                        if(amount.startswith("+")):
                            accrediti = amount[1:-1]
                            addebiti = 0
                    j += 1
                    # if it's the end of the df stop the loop
                    if i+j >= len(df):
                        break
            
            description = name + " - " + memo
            
            # Add the row to the result DataFrame
            dfresult = pandas.concat(
                [
                    dfresult,
                    pandas.DataFrame(
                        {
                            "Data Operazione": [data],
                            "Data Contabile": [valuta],
                            "Addebiti": [addebiti],
                            "Accrediti": [accrediti],
                            "Descrizione": [description],
                            "Type" : [type]
                        }
                    ),
                ],
                ignore_index=True,
            )

            i += 1
    
        result = dfresult.to_dict(orient='records')
        return result
  
    def create_transaction(self, type, description, date, settlement_date, amount, currency):
        return HypeTransaction(date, settlement_date, amount, description, type, currency)

    def parse_record(self, line: Dict) -> Optional[StatementLine]:
        date = self.parse_value(line["Data Operazione"], "date")
        settlementDate = self.parse_value(line["Data Contabile"], "date")
        if(settlementDate is None):
            logging.warning(f"'Data Contabile' is null for operation in date: '{date.strftime('%d/%m/%Y')}'. Ignoring this transaction")
            return None
    
        income = self.parse_value(line["Accrediti"], "amount")
        outcome = self.parse_value(line["Addebiti"], "amount")

        amount = income - outcome
        currency = self.parse_value("EUR", "currency")

        description = line["Descrizione"]

        type = "UNKNOWN"
        for key, value in DESCRIPTION_TYPE_MAP.items():
            if line["Type"].upper().startswith(key):
                type = value
                break

        if(type == "UNKNOWN"):
            logging.warning(
                f"Unknown transaction type: '" + line["Type"] + "'. Assigning default transaction type'\n"
                f"PLEASE open an issue on GitHub '{GITHUB_URL}' in order to help us fix it"
            )
        
        transaction = self.create_transaction(type, description, date, settlementDate, amount, currency)
        stmt_line = transaction.to_statement_line()

        return stmt_line

    # noinspection PyUnresolvedReferences
    def parse(self) -> Statement:
        statement = super().parse()
        return statement

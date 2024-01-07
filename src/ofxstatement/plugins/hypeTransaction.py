from enum import Enum
from ofxstatement.statement import StatementLine, generate_transaction_id

class TransactionType(Enum):
    BONIFICO = "BONIFICO"
    PAGAMENTO = "PAGAMENTO"
    RIMBORSO = "RIMBORSO"
    ADDEBITO_DIRETTO = "ADDEBITO DIRETTO"
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    COMMISSIONE = "COMMISSIONE"
    BOLLO = "IMPOSTA DI BOLLO",
    OTHER = "OTHER",
    CANONE = "CANONE",
    RICARICA_CARTA = "RICARICA CARTA"

# Possible values for the trntype property of a StatementLine object:
# - CREDIT: Generic credit.
# - DEBIT: Generic debit.
# - INT: Interest earned or paid (Note: Depends on signage of amount).
# - DIV: Dividend.
# - FEE: FI fee.
# - SRVCHG: Service charge.
# - DEP: Deposit.
# - ATM: ATM debit or credit (Note: Depends on signage of amount).
# - POS: Point of sale debit or credit (Note: Depends on signage of amount).
# - XFER: Transfer.
# - CHECK: Check.
# - PAYMENT: Electronic payment.
# - CASH: Cash withdrawal.
# - DIRECTDEP: Direct deposit.
# - DIRECTDEBIT: Merchant initiated debit.
# - REPEATPMT: Repeating payment/standing order.
# - OTHER: Other.

TRANSACTION_TYPES = {
    TransactionType.BONIFICO: "XFER",
    TransactionType.PAGAMENTO: "PAYMENT",
    TransactionType.ADDEBITO_DIRETTO: "DIRECTDEBIT",
    TransactionType.CREDIT: "CREDIT",
    TransactionType.DEBIT: "DEBIT",
    TransactionType.RIMBORSO: "CREDIT",
    TransactionType.COMMISSIONE: "SRVCHG",
    TransactionType.BOLLO: "FEE",
    TransactionType.CANONE: "SRVCHG",
    TransactionType.OTHER: "OTHER",
    TransactionType.RICARICA_CARTA: "XFER",
}


class HypeTransaction:
    def __init__(self, date, settlement_date, amount, description, type, currency):
        self.date = date
        self.settlement_date = settlement_date
        self.amount = amount
        self.currency = currency
        self.type = type
        self.description = description
        self.payee = description
        
    def extract_type(self, type):
        if type in TRANSACTION_TYPES:
            return TRANSACTION_TYPES[type]
        else:
            if self.amount < 0:
                return TransactionType.DEBIT.value
            else:
                return TransactionType.CREDIT.value

    def to_statement_line(self):
        statement_line = StatementLine()
        statement_line.date = self.settlement_date
        statement_line.amount = self.amount
        statement_line.trntype = self.extract_type(self.type)
        statement_line.memo = self.description
        statement_line.payee = self.payee
        statement_line.currency = self.currency
        statement_line.id = generate_transaction_id(statement_line)
        return statement_line
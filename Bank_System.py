class Bank:
    def __init__(self,name):
        self.__name = name
        self.__users = []
        self.__atm_machines = []

    def add_user(self,user):
        self.__users.append(user)

    def add_atm_machine(self,atm_info):
        self.__atm_machines.append(atm_info)

    def get_atm_by_id(self,atm_id):
        for atm in self.__atm_machines:
            if atm.atm_id == atm_id:
                return atm 
        return None
    
    def search_account_from_atm (self,atm_card_id):
        for user in self.__users:
            for account in user.accounts:
                card_id = account.atm_card
                if card_id and card_id.card_id == atm_card_id:
                    return account
        return None
    @property
    def users(self):
        return self.__users
    @property
    def atm_machines(self):
        return self.__atm_machines

class User:
    def __init__(self,user_id,user_name):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__accounts =[]

    def add_account(self,user_account):
        self.__accounts.append(user_account)

    @property
    def accounts(self):
        return self.__accounts
    
class Account:
    withdraw_day_max = 40000
    annual_fee = 150
    def __init__(self,account_no,account_user_instance,amount):
        self.__account_no = account_no
        self.__account_user_instnce = account_user_instance
        self.__amount = amount
        self.__atm_card = None
        self.__transaction = []
        self.__daily_used = 0

    def add_atm_card(self,atm_card):
        self.__atm_card = atm_card
        atm_card.bind_account(self)

    @property
    def account_no(self):
        return self.__account_no
    
    @property
    def amount(self):
        return self.__amount
    
    @amount.setter
    def amount(self, value):
        self.__amount = value


    @property
    def atm_card(self):
        return self.__atm_card


    def create_transaction(self, t_type, atm_id, amount, target=None):
        t = Transaction(t_type,atm_id,amount,self.amount,target)
        self.__transaction.append(t)

    def pay_annual_fee(self):

        if self.__amount < Account.annual_fee:
            raise Exception("Insufficient balance for annual fee")
        
        self.__amount -= Account.annual_fee
        self.create_transaction("ANNUAL FEE", Account.annual_fee)
    
    def reset_dialy_used(self):
        self.__daily_used = 0

    def validate_atm(self, atm_mac):
        if atm_mac.status_card is None:
            raise ValueError("No ATM card inserted")
        
        if atm_mac.status_card is not self.__atm_card:
            raise ValueError("ATM card does not match account")
        
        return True
    
    @property
    def transaction(self):
        return self.__transaction
    
    def print_transactions(self):
        for i in self.__transaction:
            print(i)

class ATM_Card:
    def __init__(self,atm_card_id,atm_card_account,atm_card_password):
        self.__card_id = atm_card_id
        self.__card_account = atm_card_account
        self.__card_password = atm_card_password

    @property
    def card_id(self):
        return  self.__card_id
    
    @property
    def card_account(self):
        return self.__card_account
    
    @property
    def card_password(self):
        return self.__card_password
    
    def bind_account(self,account):
        self.__card_account = account
    
    def validate_password(self,password):
        return self.__card_password == password
    # def validate_account(self,account):
    #     return self.__card_account == account

class ATM_machine:
    def __init__(self,atm_id,atm_cash):
        self.__atm_id = atm_id
        self.__atm_cash = atm_cash
        self.__status_card = None

    @property
    def status_card(self):
        return self.__status_card

    def insert_card(self,atm_card,password):
        if not atm_card.validate_password(password):
            return False
        self.__status_card = atm_card
        # print(atm_card)
        return True
    
    def check_card(self):
        if self.__status_card is None:
            raise ValueError("No card inserted")
        
    def eject_card(self):
        self.__status_card = None

    @property
    def atm_id(self):
        return self.__atm_id
    
    @property
    def atm_cash(self):
        return self.__atm_cash
    
    @property
    def cash(self):
        return self.__atm_cash

    def add_cash(self,cash):
        self.__atm_cash += cash

    def reduce_cash(self,cash):
        if cash > self.__atm_cash:
            raise Exception("ATM has insufficient cash")
        self.__atm_cash -= cash

class Transaction:
    def __init__(self,type,atm_id,amount,balance,target):
        self.__type = type
        self.__atm_id = atm_id
        self.__amount = amount
        self.__balance = balance
        self.__target = target
    def __str__(self):
        return f"{self.__type}-ATM:{self.__atm_id}-{self.__amount}-{self.__balance}-{self.__target}"
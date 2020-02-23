class Account():

    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance


    def __str__(self):
        return  (f"Account owner: {self.owner}\n"
                 f"Account balance: {self.balance}"
                )

    
    def depositMoney(self, amount):
        self.balance = (self.balance + amount)
        print("Deposit of amount ${} accepted".format(amount))
        print("Your new balance is: " + "$" + str(self.balance))


    def withdrawMoney(self, amount):
        if amount >= self.balance:
            print("Funds Unavailable! Withdraw amount exeeds available funds.")
        else:
            self.balance = (self.balance - amount)
            print("Successfuly withdrew amount ${}.".format(amount))
            print("Your new balance is: " + "$" + str(self.balance))



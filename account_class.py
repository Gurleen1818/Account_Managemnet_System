import pickle

from database_management import create_new_partition_in_db, passbook_append_for_credit, passbook_append_for_debit, \
    passbook_append_for_transfer


def transfer(chosen_account):
    # Menu for transfer
    print("Choose a partition to transfer from\n")
    chosen_account.view_partitions()
    choice5 = int(input()) - 1
    from_partition = chosen_account.partitions_list[choice5]
    print("choose a partition to transfer to\n")
    chosen_account.view_partitions()
    choice6 = int(input()) - 1
    amount = int(input("Enter the amount to be transferred\n"))
    to_partition = chosen_account.partitions_list[choice6]
    from_partition.transfer_between(to_partition, amount)
    chosen_account.view_partitions()
    passbook_append_for_transfer(chosen_account, from_partition, to_partition, amount)


def transaction(chosen_account):
    # Menu for transaction
    print("Choose a partition to which transaction is to be added\n")
    chosen_account.view_partitions()
    choice7 = int(input()) - 1
    transaction_partition = chosen_account.partitions_list[choice7]
    transaction_type = input("Enter transaction type. Debit or credit\n").lower()
    transaction_amount = int(input("Enter transaction amount.\n"))
    transaction_name = input("Enter name of the transaction\n")
    if transaction_type == "credit":
        chosen_account.credit(transaction_amount)
        transaction_partition.credit(transaction_amount)
        passbook_append_for_credit(chosen_account, transaction_amount, transaction_name, transaction_partition)

    elif transaction_type == "debit":
        while transaction_amount > transaction_partition.partition_balance:
            choice8 = input("Insufficient Funds in partition.\n Would you like to transfer between partitions. "
                            "Type yes or no.\n").lower()
            if choice8 == "yes":
                print(f"Minimum amount required is {transaction_amount - transaction_partition.partition_balance}")
                transfer(chosen_account)

            else:
                print("Transaction not added.\n")

        chosen_account.debit(transaction_amount)
        transaction_partition.debit(transaction_amount)
        passbook_append_for_debit(chosen_account, transaction_amount, transaction_name, transaction_partition)
        print("Transaction added.\n")
        chosen_account.get_account_information()
        chosen_account.view_partitions()


class MainAccount:
    def __init__(self, m_name="", m_balance=0):
        self.name = m_name
        self.balance = m_balance
        self.balance_for_partition = m_balance
        self.partition = self.Partition
        self.partitions_list = []

    def credit(self, amount):
        self.balance += amount

    def debit(self, amount):
        self.balance -= amount

    def show_main_balance(self):
        return self.balance

    def get_account_information(self):
        # shows balance and name of the account
        print(f"Name: {self.name}\n"
              f"Balance: {self.balance}\n")

    def view_partitions(self):
        # view all the partitions under the given account
        print(f"You have following partitions added under account {self.name}")
        for i in range(0, len(self.partitions_list)):
            print(f"{i + 1}. Name: {self.partitions_list[i].partition_name}\n"
                  f"Balance: {self.partitions_list[i].partition_balance}\n")

    def create_partition(self):
        # create a new partition under the given account
        p_name = input("Enter a name for the partition\n")
        p_balance = int(input("Enter the amount that is to be allotted to this partition.\n"))

        if p_balance <= self.partitions_list[0].partition_balance:
            partition = self.partition(p_name)
            self.partitions_list[0].transfer_between(partition, p_balance)
            self.partitions_list.append(partition)

            create_new_partition_in_db(self, partition, p_balance)

            print(f"Partition Created under account {self.name}.\n"
                  f"Name = {partition.partition_name}\n"
                  f"Balance = {partition.partition_balance}\n")

        else:
            print("Amount provided for creating the partition is more than amount available for partition\n"
                  f"Amount available for partition is {self.balance_for_partition}")
            self.create_partition()

        choice = input("Would you like to add another partition to this account? Type Yes or No.\n").lower()

        if choice == "yes":
            self.create_partition()
        else:
            return False

    def pickle(self):
        # pickle partitions under main account
        file_object = open(f'{self.name}_partitions.pkl', 'wb')
        pickle.dump(self.partitions_list, file_object)
        file_object.close()

    def unpickle(self):
        # unpickle partitions under main account
        file_object = open(f'{self.name}_partitions.pkl', 'rb')
        partition_list = pickle.load(file_object)
        file_object.close()
        self.partitions_list = partition_list

    class Partition:
        # Partition subclass under main account
        def __init__(self, p_name="", p_balance=0):  # constructor
            self.partition_name = p_name
            self.partition_balance = p_balance

        def transfer_between(self, other, amount):  # transfer between partitions
            self.partition_balance -= amount
            other.partition_balance += amount

        def credit(self, amount):  # add credit to partition
            self.partition_balance += amount

        def debit(self, amount):  # add debit to partition
            self.partition_balance -= amount


def pickling_for_main_accounts(a_list):
    # pickle function for main account objects.
    file_object = open("main_accounts.pkl", "wb")
    pickle.dump(a_list, file_object)
    file_object.close()


def unpickle_for_main_accounts():
    # unpickle function for main account objects.
    file_object = open("main_accounts.pkl", "rb")
    main_account_list = pickle.load(file_object)
    file_object.close()
    return main_account_list


def pickle_everything(main_account_list):
    # pickle the main account objects and their respective partitions
    pickling_for_main_accounts(main_account_list)
    for x in main_account_list:
        x.pickle()


def unpickle_everything():
    # unpickle the main account objects and their respective partitions
    main_accounts = unpickle_for_main_accounts()
    for x in main_accounts:
        x.unpickle()
    return main_accounts

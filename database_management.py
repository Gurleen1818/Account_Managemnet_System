import mysql.connector
from prettytable import from_db_cursor

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd="Password123",
                               database="Account_Management_System")

my_cursor = mydb.cursor()


def create_new_account_in_db(account, none):
    main_account_append(account)
    create_passbook(account)
    create_partition_table(account)
    passbook_append_for_new_account(account, none)


def create_new_partition_in_db(account, partition, transaction_amount):
    add_partition_column(account, partition)
    passbook_append_for_partition_created(account, partition, transaction_amount)


def main_account_append(account):
    # Insert newly created account in Main Accounts Table in database
    query1 = "INSERT into main_accounts values (%s, %s)"
    data1 = (account.name, account.balance)
    my_cursor.execute(query1, data1)
    mydb.commit()


def create_passbook(account):
    # Create the passbook
    query = f"Create Table {account.name} (Transaction_Name VARCHAR(255), " \
            f"{account.partitions_list[0].partition_name} int," \
            f"Main_Account_Credit int,Main_Account_Debit int, Main_Account_Balance int)"
    my_cursor.execute(query)
    mydb.commit()


def create_partition_table(account):
    # Create Table that holds all the partition and their balance
    query = f"Create Table {account.name}_Partitions (Partition_Name VARCHAR(255), Partition_Balance int)"
    my_cursor.execute(query)
    mydb.commit()


def passbook_append_for_new_account(account, none):
    # Insert into passbook the account creation entry
    query = f"INSERT into {account.name} (Transaction_name, Main_Account_Balance) values (%s, %s)"
    data = ('Account Created', account.balance)
    my_cursor.execute(query, data)
    mydb.commit()

    # None partition entry
    query = f"INSERT into {account.name} (Transaction_name, None, Main_Account_Balance) " \
            f"values (%s, %s, %s)"
    data = (f'{none.partition_name} Partition created', none.partition_balance, account.balance)
    my_cursor.execute(query, data)
    mydb.commit()
    update_partition_table(account)


def add_partition_column(account, partition):
    # Add a column after the previous partition into the table
    number_of_partitions = len(account.partitions_list)
    last_partition = account.partitions_list[number_of_partitions - 2]
    query = f"ALTER TABLE {account.name} ADD column {partition.partition_name} int AFTER " \
            f"{last_partition.partition_name}"
    my_cursor.execute(query)
    mydb.commit()


def passbook_append_for_partition_created(account, partition, transaction_amount):
    # Add the entry into passbook about the partition created
    none = account.partitions_list[0]
    passbook_append_for_transfer(account, none, partition, transaction_amount)
    update_partition_table(account)


def passbook_append_for_credit(account, amount, transaction_name, partition):
    # Add the entry into passbook about the credit transaction
    query = f"INSERT into {account.name} (Transaction_name, {partition.partition_name}, Main_Account_Credit, " \
            f"Main_Account_Balance) values (%s, %s, %s, %s)"
    data = (f'{transaction_name}', + amount, amount, account.balance)

    my_cursor.execute(query, data)
    mydb.commit()
    update_partition_table(account)


def passbook_append_for_debit(account, amount, transaction_name, partition):
    # Add the entry into passbook about the debit transaction
    query = f"INSERT into {account.name} (Transaction_name, {partition.partition_name}, Main_Account_Debit, " \
            f"Main_Account_Balance) values (%s, %s, %s, %s)"
    data = (f'{transaction_name}', - amount, amount, account.balance)

    my_cursor.execute(query, data)
    mydb.commit()
    update_partition_table(account)


def passbook_append_for_transfer(account, from_partition, to_partition, amount):
    # Add the entry into passbook about the transfer between partitions
    query1 = f"INSERT into {account.name} (Transaction_name, {from_partition.partition_name}, " \
             f"{to_partition.partition_name}, Main_Account_Balance) values (%s, %s, %s, %s)"
    data1 = (f'Transfer from {from_partition.partition_name} to {to_partition.partition_name}', - amount, + amount,
             account.balance)
    my_cursor.execute(query1, data1)
    mydb.commit()
    update_partition_table(account)


def view_passbook(account):
    # View the passbook
    query = f"Select * from {account.name}"
    my_cursor.execute(query)
    passbook = from_db_cursor(my_cursor)
    print(passbook)


def update_partition_table(account):
    # Everytime a transaction related to a partition happens it deletes the previous table that holds the partitions
    # and create a new table that holds partitions under that account and its balance
    query1 = f"Drop Table {account.name}_Partitions"
    my_cursor.execute(query1)
    mydb.commit()
    query = f"Create Table {account.name}_Partitions (Partition_Name VARCHAR(255), Partition_Balance int)"
    my_cursor.execute(query)
    mydb.commit()
    for x in account.partitions_list:
        query2 = f"INSERT into {account.name}_Partitions values (%s, %s)"
        data2 = (x.partition_name, x.partition_balance)
        my_cursor.execute(query2, data2)
        mydb.commit()


def view_partitions_table(account):
    query = f"Select * from {account.name}_Partitions"
    my_cursor.execute(query)
    partition_table = from_db_cursor(my_cursor)
    print(partition_table)
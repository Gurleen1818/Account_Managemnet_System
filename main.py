from account_class import MainAccount, transfer, transaction, pickle_everything, unpickle_everything
from database_management import create_new_account_in_db, view_passbook, view_partitions_table

# uncomment the line below if using for the first time
# main_accounts = []
main_accounts = unpickle_everything()  # comment this line if using for the first time


def account_menu(chosen_account):
    print(f"You have logged into account named {chosen_account.name}")
    choice4 = int(input("Choose what would you like to do? Enter the numbers\n"
                        "1. Get Account Information\n"
                        "2. View Partitions\n"
                        "3. Add a new Partition.\n"
                        "4. Add a transaction. \n"
                        "5. Transfer between Partitions.\n"
                        "6. View Passbook.\n"
                        "7. Return to main menu.\n"))
    if choice4 == 1:
        chosen_account.get_account_information()
        account_menu(chosen_account)

    elif choice4 == 2:
        view_partitions_table(chosen_account)
        account_menu(chosen_account)

    elif choice4 == 3:
        if not chosen_account.create_partition():
            account_menu(chosen_account)

    elif choice4 == 4:
        transaction(chosen_account)
        account_menu(chosen_account)

    elif choice4 == 5:
        transfer(chosen_account)
        account_menu(chosen_account)

    elif choice4 == 6:
        view_passbook(chosen_account)
        account_menu(chosen_account)

    elif choice4 == 7:
        main_menu()


def main_menu():
    print("Welcome to Account Management System Application")
    choice1 = int(input("Choose what would you like to do? Enter the number."
                        "\n1. View my main accounts"
                        "\n2. Add a new main account."
                        "\n3. Exit.\n"))

    if choice1 == 1:
        if len(main_accounts) == 0:
            print("No main account added yet. Kindly add a main account\n")
            main_menu()

        else:
            print("You have following accounts added.")
            for i in range(0, len(main_accounts)):
                print(f"{i + 1}. {main_accounts[i].name}")
            choice3 = int(input("Choose the account you want to view\n")) - 1
            chosen_account = main_accounts[choice3]
            account_menu(chosen_account)

    elif choice1 == 2:
        m_name = input("Enter a name for your new account\n")
        m_balance = int(input("Enter the current balance in the account.\n"))
        account = MainAccount(m_name, m_balance)

        none = account.partition("None", m_balance)
        account.partitions_list.append(none)

        print(f"Your Account has been created.\n"
              f"Name: {account.name}\n"
              f"Current Balance: {account.balance}")
        create_new_account_in_db(account, none)
        main_accounts.append(account)

        choice2 = input("Would you like to add a partition? Type Yes or No.\n").lower()
        if choice2 == 'yes':
            if not account.create_partition():
                main_menu()
        else:
            main_menu()

    else:
        pickle_everything(main_accounts)


main_menu()

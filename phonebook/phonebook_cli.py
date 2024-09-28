import argparse
from schema import Contact, PhoneNumber
from phonebook import Phonebook

phonebook = Phonebook()

def create_parser():
    parser =argparse.ArgumentParser(description='Phonebook CLI')
    group =parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', help='List all the contacts', action='store_true')
    group.add_argument('-a', '--add', help='Add a new contact: [name] [email] [phonenumber]', nargs='+')
    group.add_argument('-d', '--details', help= 'Get details of contact')
    group.add_argument('-del', '--delete', help= 'delete contact')
    return parser

def print_all_contacts():
    for i in phonebook.get_all_contacts():
        print(i)

def add_custom_contact(args):
    number = args[-1]
    email = args[-2]
    name = args[:-2]
    print(args, name)
    if len(name) == 3:
        first_name = name[0]
        middle_name = name[1]
        last_name = name[2]

    elif len(name) == 2:
        first_name = name[0]
        middle_name = ""
        last_name = name[1]
    
    elif len(name) == 1:
        first_name = name[0]
        middle_name = ""
        last_name = ""
    else:
        first_name = name[0]
        middle_name = ""
        last_name = ""
    
    print(first_name,middle_name,last_name)
    phonenumber = PhoneNumber(label='main',country_code='+1', phone_number=number)
    contact = Contact(first_name=first_name, middle_name=middle_name, last_name=last_name, email = email, address="")
    contact.phone_numbers = [phonenumber]
    print(contact)
    phonebook.add_new_contact(contact)

def view_contact_details(id):
    contact = phonebook.get_contact_details(id)
    print(contact)

def delete_contact(_id):
    phonebook.delete_contact(_id)


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.list:
        print_all_contacts()
    elif args.add:
        add_custom_contact(args.add)
    elif args.details:
        view_contact_details(args.details)
    elif args.delete:
        delete_contact(args.delete)

if __name__ == '__main__':
    main()  



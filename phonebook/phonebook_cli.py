import argparse
from schema import Contact, PhoneNumber
from phonebook import Phonebook

# create a phonebook obj
phonebook = Phonebook()

def create_parser():
    # create a parser to parse cli arguments
    parser =argparse.ArgumentParser(description='Phonebook CLI')
    # create a mutually excusive group
    # to avoid pairing og arguments
    group =parser.add_mutually_exclusive_group()
    # add arguments to the group
    group.add_argument('-l', '--list', help='List all the contacts', action='store_true')
    group.add_argument('-a', '--add', help='Add a new contact: [name] [email] [phonenumber]', nargs='+')
    group.add_argument('-d', '--details', help= 'Get details of contact')
    group.add_argument('-del', '--delete', help= 'delete contact')
    return parser

def print_all_contacts():
    # print all contacts in the phonebook
    for i in phonebook.get_all_contacts():
        print(i)

def add_custom_contact(args):
    # parse arguments
    number = args[-1] # last argument will be phoenumber
    email = args[-2] # 2nd last will be email
    name = args[:-2] # all else will be name
    print(args, name)
    # if name has three elements
    # assign to fist, middle and last name
    if len(name) == 3:
        first_name = name[0]
        middle_name = name[1]
        last_name = name[2]
    # if name has two elements
    # set middle name as blank
    elif len(name) == 2:
        first_name = name[0]
        middle_name = ""
        last_name = name[1]
    # if name has single element
    # set only first name
    elif len(name) == 1:
        first_name = name[0]
        middle_name = ""
        last_name = ""
    # if name list is > 3:
    # set only first name and discard the rest
    else:
        first_name = name[0]
        middle_name = ""
        last_name = ""
    
    print(first_name,middle_name,last_name)
    # create phonenumber object with some default values
    phonenumber = PhoneNumber(label='main',
                              country_code='+1', 
                              phone_number=number)
    # create contact obj
    contact = Contact(first_name=first_name, 
                      middle_name=middle_name, 
                      last_name=last_name, 
                      email = email, address="")
    # update phone_numbers property
    contact.phone_numbers = [phonenumber]
    print(contact)
    # add new contact
    phonebook.add_new_contact(contact)

def view_contact_details(id):
    # view contact details
    contact = phonebook.get_contact_details(id)
    print(contact)

def delete_contact(_id):
    # delete contact by id
    phonebook.delete_contact(_id)


def main():
    # initialize the parser
    parser = create_parser()
    # parse arguments
    args = parser.parse_args()
    # call functions based on args
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



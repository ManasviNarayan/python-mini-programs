from schema import Contact
from repository import PhonebookRepo
import re


class Phonebook:
    
    def __init__(self):
        # initialize the repo object
        self.repo = PhonebookRepo()
        
    def get_all_contacts(self):
        # get all contacts from the repo
        return self.repo.get_all_contacts()
            
    def search_contact(self, query: str):
        # loop over all contacts to search for query string
        for contact in self.get_all_contacts():
            # use the str representation 
            # of contact object
            # to serach for the query string
            if query.lower() in str(contact).lower():
                yield contact # Return one contact at a time
    
    def get_contact_details(self, contact_id):
        try:
            # check if contact exists and return contact details
            if self.repo.contact_exists(contact_id):
                return self.repo.get_contact_details(contact_id)
            else:
                raise Exception('Contact not found')
        except Exception as e:
            print(f"Error: {e}")
            
    def add_new_contact(self, contact: Contact):
        try:
            # format the contact object to standardize
            contact = self._format_contact(contact)
            for number in contact.phone_numbers:
                # check if new phonenumber already exists 
                #  in some contact
                if self.repo.phone_number_exists(number.phone_number):
                    raise Exception(f'Phone Number {number.phone_number} already exists')
            # else add contact
            self.repo.add_new_contact(contact)
        except Exception as e:
            print(f"Error adding contact: {e}")
                        
    def update_contact(self, contact:Contact):
        try:
            # format conatct object to standardize input
            contact = self._format_contact(contact)
            # update contact with new object
            # if contact exists
            if self.repo.contact_exists(contact._id):    
                self.repo.update_contact(contact)
            else:
                raise Exception('Contact Not Found')
        except Exception as e:
            print(f"Error updating contact: {e}")
    
    def delete_contact(self, contact_id):
        try:
            # check if contact exists and delete
            if self.repo.contact_exists(contact_id):
                self.repo.delete_contact(contact_id)
            else:
                raise Exception('Contact Not Found')
        except Exception as e:
            print(f"Error deleting contact: {e}")

    def _validate_email(self, email:str):
        # check if email address is valid
        pattern = re.compile(r'\w+@\w.\w')
        if pattern.match(email):
            return True
        else:
            return False

    def _validate_phonenumber(self, phone_number:str):
        # check if phone number is valid
        # 0(optional)10 digits
        pattern = re.compile(r'^0?\d{10}$')
        if pattern.match(phone_number):
            return True
        else:
            return False
        
    def _validate_country_code(self, country_code:str):
        # check if country code is valid
        # + digits(min=1, max=3)
        pattern = re.compile(r'^\+?\d{1,3}$')
        if pattern.match(country_code):
            return True
        else:
            return False
    
    def _format_contact(self, contact: Contact):
        # format contact object
        # convert name, address to title case
        contact.first_name = contact.first_name.strip().title()
        contact.middle_name = contact.middle_name.strip().title()
        contact.last_name = contact.last_name.strip().title()
        contact.address = contact.address.strip().title()
        #convert email to lower case
        contact.email = contact.email.strip().lower()
        # check if email is valid
        if not self._validate_email(contact.email):
                raise Exception('Invalid email')
        for number in contact.phone_numbers:
            number.phone_number = number.phone_number.strip()
            # remove whitespace from phonenumber
            number.phone_number = re.sub(r'\s', "", number.phone_number)
            number.country_code = number.country_code.strip()
            # convert label to upper case
            number.label = number.label.strip().upper()
            # check if  countrycode is valid
            if not self._validate_country_code(number.country_code):
                raise Exception('Invalid country code')
            # check if phonenumber is valid
            if not self._validate_phonenumber(number.phone_number):
                raise Exception('Invalid phone number')
        return contact
        
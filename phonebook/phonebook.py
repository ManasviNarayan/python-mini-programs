from schema import Contact
from repository import PhonebookRepo
import re


class Phonebook:
    
    def __init__(self):
        self.repo = PhonebookRepo()
        
    def get_all_contacts(self):
        return self.repo.get_all_contacts()
            
    def search_contact(self, query: str):
        for contact in self.get_all_contacts():
            if query.lower() in str(contact).lower():
                yield contact
    
    def get_contact_details(self, contact_id):
        try:
            return self.repo.get_contact_details(contact_id)
        except Exception as e:
            print(f"Error: {e}")
            
    def add_new_contact(self, contact: Contact):
        try:
            contact = self._format_contact(contact)
            for number in contact.phone_numbers:
                if self.repo.phone_number_exists(number.phone_number):
                    raise Exception(f'Phone Number {number.phone_number} already exists')
            self.repo.add_new_contact(contact)
        except Exception as e:
            print(f"Error adding contact: {e}")
                        
    def update_contact(self, contact:Contact):
        try:
            contact = self._format_contact(contact)
            if self.repo.contact_exists(contact._id):    
                self.repo.update_contact(contact)
            else:
                raise Exception('Contact Not Found')
        except Exception as e:
            print(f"Error updating contact: {e}")
    
    def delete_contact(self, contact_id):
        try:
            self.repo.delete_contact(contact_id)
        except Exception as e:
            print(f"Error deleting contact: {e}")

    def _validate_email(self, email:str):
        pattern = re.compile(r'\w+@\w.\w')
        if pattern.match(email):
            return True
        else:
            return False

    def _validate_phonenumber(self, phone_number:str):
        pattern = re.compile(r'^0?\d{10}$')
        if pattern.match(phone_number):
            return True
        else:
            return False
        
    def _validate_country_code(self, country_code:str):
        pattern = re.compile(r'^\+?\d{1,3}$')
        if pattern.match(country_code):
            return True
        else:
            return False
    
    def _format_contact(self, contact: Contact):
        contact.first_name = contact.first_name.strip().title()
        contact.middle_name = contact.middle_name.strip().title()
        contact.last_name = contact.last_name.strip().title()
        contact.address = contact.address.strip().title()
        contact.email = contact.email.strip().lower()
        if not self._validate_email(contact.email):
                raise Exception('Invalid email')
        for number in contact.phone_numbers:
            number.phone_number = number.phone_number.strip()
            number.phone_number = re.sub(r'\s', "", number.phone_number)
            number.country_code = number.country_code.strip()
            number.label = number.label.strip().upper()
            if not self._validate_country_code(number.country_code):
                raise Exception('Invalid country code')
            if not self._validate_phonenumber(number.phone_number):
                raise Exception('Invalid phone number')
        return contact
        
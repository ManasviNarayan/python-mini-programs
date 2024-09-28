import sqlite3
from contextlib import closing
from schema import PhoneNumber, Contact

class PhonebookRepo:
    
    def __init__(self):
        self.all_contacts = []
        self.con = sqlite3.connect('phonebook.db')        
        self.con.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        with self.con as con:
            con.execute('''CREATE TABLE IF NOT EXISTS
                        phonebook(_ID INTEGER PRIMARY KEY,
                        FIRST_NAME TEXT, 
                        MIDDLE_NAME TEXT, 
                        LAST_NAME TEXT,
                        EMAIL TEXT UNIQUE,
                        ADDRESS TEXT)''')
            
            con.execute('''CREATE TABLE IF NOT EXISTS
                        phonenumber(CONTACT_ID INTEGER,
                        LABEL TEXT,
                        COUNTRY_CODE TEXT,
                        PHONE_NUMBER TEXT,
                        FOREIGN KEY(CONTACT_ID) REFERENCES phonebook(_ID))''')
        
    def get_all_contacts(self):
        with self.con as con:
            result = con.execute('''select * from phonebook order by first_name''')
            contacts = result.fetchall()
            for contact in contacts:
                contact = {k.lower(): contact[k] for k in contact.keys()}
                result = con.execute('''select * from phonenumber where contact_id = ?''', (contact['_id'],))
                phones = result.fetchall()
                phonenumbers = []
                for number in phones:
                    phonenumbers.append(PhoneNumber(label=number['label'],
                                                    country_code=number['country_code'],
                                                    phone_number=number['phone_number']))
                contact_details = Contact(**contact)
                contact_details.phone_numbers = phonenumbers
                yield contact_details
            
    def get_contact_details(self, contact_id):
        try:
            with self.con as con:
                result = con.execute('''select * from phonebook where _id = ?''', (contact_id,))
                contact = result.fetchone()
                if contact is None:
                    raise Exception('Contact not found')
                contact = {k.lower(): contact[k] for k in contact.keys()}
                result = con.execute('''select * from phonenumber where contact_id = ?''', (contact_id,))
                phones = result.fetchall()
                phonenumbers = []
                for number in phones:
                    phonenumbers.append(PhoneNumber(label=number['label'],
                                                    country_code=number['country_code'],
                                                    phone_number=number['phone_number']))
                contact_details = Contact(**contact)
                contact_details.phone_numbers= phonenumbers
                return contact_details
        except Exception as e:
            print(f'Error: {e}')
            raise
            
    def add_new_contact(self, contact: Contact):
        try:
            with self.con as con:
                con.execute('''insert into phonebook(first_name, middle_name, last_name, email, address) 
                            values (?,?,?,?,?)''',(contact.first_name, contact.middle_name, contact.last_name,contact.email, contact.address))
                phonenumbers = contact.phone_numbers
                for number in phonenumbers:
                    con.execute('''insert into phonenumber(contact_id, label, country_code, phone_number) values(?,?,?,?)''',
                                (contact._id, number.label, number.country_code, number.phone_number))
        except Exception as e:
            print(f'Error: {e}')
            raise
               
    def update_contact(self, contact: Contact):
        try:
            with self.con as con:
                con.execute('''update phonebook 
                            set first_name = ?, 
                                middle_name = ?, 
                                last_name = ?, 
                                email = ?, 
                                address = ? 
                            where _id = ?
                             ''',(contact.first_name, 
                                  contact.middle_name, 
                                  contact.last_name,
                                  contact.email, 
                                  contact.address, 
                                  contact._id))
                con.execute('''delete from phonenumber 
                            where contact_id = ?''', (contact._id,))
                phonenumbers = contact.phone_numbers
                for number in phonenumbers:
                    con.execute('''insert into phonenumber(
                                contact_id, label, country_code, phone_number) values(?,?,?,?)''',
                                (contact._id, number.label, number.country_code, number.phone_number)) 
        except Exception as e:
            print(f'Error: {e}')
            raise
        
    def delete_contact(self, contact_id):
        try:
            with self.con as con:
                con.execute('''delete from phonenumber
                            where contact_id = ?''', (contact_id,))
                con.execute('''delete from phonebook
                            where _id = ?''', (contact_id,))
        except Exception as e:
            print(f'Error: {e}')
            raise

    def phone_number_exists(self, number):
        with self.con as con:
            result = con.execute('select * from phonenumber where phone_number = ?', (number,))
            out = result.fetchone() is not None
        return out
        
    def contact_exists(self, contact_id:int):
        with self.con as con:
            result = con.execute('select * from phonebook where _id = ?', (contact_id,))
            out = result.fetchone() is not None  
            return out
        

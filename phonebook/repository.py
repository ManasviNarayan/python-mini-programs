import sqlite3
from contextlib import closing
from schema import PhoneNumber, Contact

class PhonebookRepo:
    
    def __init__(self):
        # initialize a connection to phonebook db
        self.con = sqlite3.connect('phonebook.db')   
        # return output for each row as 
        # a dict like Row object     
        self.con.row_factory = sqlite3.Row
        # create tables if does not exists
        self._create_tables()

    def _create_tables(self):
        # create phonebook and phonenumber tables
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
        # get all records
        with self.con as con:
            # fetch all contacts from phonebook table
            result = con.execute('''select * from phonebook order by first_name''')
            # directly loop on the cursor object 
            # instead of calling fetchall()
            for contact in result:
                # convert contact Row object to dict
                contact = {k.lower(): contact[k] for k in contact.keys()}
                # fetch all phone numbers for each contact
                # from phonenumber table
                result = con.execute('''select * from phonenumber where contact_id = ?''', (contact['_id'],))
                phones = result.fetchall()
                phonenumbers = []
                for number in phones:
                    # create a phonenumber object
                    phonenumbers.append(PhoneNumber(label=number['label'],
                                                    country_code=number['country_code'],
                                                    phone_number=number['phone_number']))
                # create Contact object using dict
                contact_details = Contact(**contact)
                # update phone_numbers attribute 
                # with list of PhoneNumber objects
                contact_details.phone_numbers = phonenumbers
                # return one object at a time
                yield contact_details
            
    def get_contact_details(self, contact_id):
        try:
            with self.con as con:
                # fetch conatct details based on id
                result = con.execute('''select * from phonebook where _id = ?''', (contact_id,))
                contact = result.fetchone()
                if contact is None:
                    raise Exception('Contact not found')
                # convert row object to dict
                contact = {k.lower(): contact[k] for k in contact.keys()}
                # fetch all phonebumbers for the contact
                result = con.execute('''select * from phonenumber where contact_id = ?''', (contact_id,))
                phones = result.fetchall()
                phonenumbers = []
                # create PhoneNumber object 
                # for each number in that contact
                for number in phones:
                    phonenumbers.append(PhoneNumber(label=number['label'],
                                                    country_code=number['country_code'],
                                                    phone_number=number['phone_number']))
                # create contact object with dict
                contact_details = Contact(**contact)
                # update phone_number attribute
                contact_details.phone_numbers= phonenumbers
                return contact_details
        except Exception as e:
            print(f'Error: {e}')
            raise
            
    def add_new_contact(self, contact: Contact):
        try:
            with self.con as con:
                # insert contact into phonebook table
                con.execute('''insert into phonebook(first_name, middle_name, last_name, email, address) 
                            values (?,?,?,?,?)''',(contact.first_name, contact.middle_name, contact.last_name,contact.email, contact.address))
                # get the id of the newly inserted contact
                new_id = con.execute("SELECT last_insert_rowid() AS new_id")
                new_id = new_id.fetchone()[0]
                # insert phone numbers into phonenumber table
                phonenumbers = contact.phone_numbers
                for number in phonenumbers:
                    con.execute('''insert into phonenumber(contact_id, label, country_code, phone_number) values(?,?,?,?)''',
                                (new_id, number.label, number.country_code, number.phone_number))
        except Exception as e:
            print(f'Error: {e}')
            raise
               
    def update_contact(self, contact: Contact):
        try:
            with self.con as con:
                # update contact details in phonebook table
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
                # first delete preexisting phonenumbers for the contact
                con.execute('''delete from phonenumber 
                            where contact_id = ?''', (contact._id,))
                # add all phonenumbers from updated conatact object
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
                # delete from phonebook table
                con.execute('''delete from phonenumber
                            where contact_id = ?''', (contact_id,))
                # delete from phonenumber table
                con.execute('''delete from phonebook
                            where _id = ?''', (contact_id,))
        except Exception as e:
            print(f'Error: {e}')
            raise

    def phone_number_exists(self, number):
        with self.con as con:
            # fetch record with given phonenumber
            result = con.execute('select * from phonenumber where phone_number = ?', (number,))
            out = result.fetchone() is not None
        return out
        
    def contact_exists(self, contact_id:int):
        with self.con as con:
            # fetch contact with given id
            result = con.execute('select * from phonebook where _id = ?', (contact_id,))
            out = result.fetchone() is not None  
            return out
        

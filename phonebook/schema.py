from dataclasses import dataclass

@dataclass
class PhoneNumber:
    label: str
    country_code: str
    phone_number: str

    def __str__(self):
        return f'{self.label}: {self.country_code}{self.phone_number}'

    def __repr__(self):
        return repr(f'PhoneNumber(label={self.label}, country_code={self.country_code}, phone_number={self.phone_number}')

@dataclass
class Contact():
    first_name: str
    middle_name: str | None = ""
    last_name: str | None = ""
    email: str | None = None
    address: str | None = ""
    phone_numbers = list[PhoneNumber] | None 
    _id: int | None = None


    def __str__(self):
        return f'{self._id} {self.first_name} {self.middle_name} {self.last_name} | {self.email} | {self.address} | {[str(i) for i in self.phone_numbers]}'
    
    def __repr__(self):
        return repr(f"Contact(_id={self._id}, first_name={self.first_name},middle_name={self.middle_name}, last_name={self.last_name}, email={self.email},address={self.address}, phone_numbers={self.phone_numbers})")
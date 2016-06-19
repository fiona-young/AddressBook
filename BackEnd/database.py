import sqlite3
class Database:
    def __init__(self,location = 'example.db'):
        self.conn = sqlite3.connect(location)
        self.c = self.conn.cursor()

    def get_auto_increment(self,table_id='item_id',table_name='item_list'):
        t = (table_id,table_name)
        self.c.execute('SELECT MAX(%s) FROM %s'% t)
        last = self.c.fetchone()[0]
        return 1 if last is None else last+1

    def get_next_item_id(self):
        return self.get_auto_increment('item_id','item_list')

    def get_next_email_id(self):
        return self.get_auto_increment('email_id','email')

    def get_next_phone_id(self):
        return self.get_auto_increment('phone_id','phone')

    def get_next_address_id(self):
        return self.get_auto_increment('address_id','address')

    def get_company_id_from_name(self,company_name):
        self.c.execute('SELECT item_id from company WHERE name = ?',(company_name,))
        return self.c.fetchone()[0]

    def add_company(self,input):
        if 'name' not in input:
            return
        item_id = self.get_next_item_id()
        self.c.execute('INSERT into item_list VALUES(?)',(item_id,))
        self.c.execute('INSERT into company(item_id,name) VALUES(?,?)',(item_id,input['name']))
        self.add_email_or_phone(input,item_id)
        created, address_id = self.add_address(input)
        if created:
                self.c.execute('UPDATE company SET address_id = ? WHERE item_id = ?',(address_id,item_id))
        self.commit()

    def update_company(self,input):
        if 'name' not in input:
            return
        item_id = input['item_id']
        previous_company = self.get_company(item_id)
        if input['name']!=previous_company['name']:
            self.c.execute('UPDATE company set name = ? where item_id = ?',(input['name'],item_id))
        self.update_email_or_phone(input,previous_company,item_id)
        self.add_email_or_phone(input,item_id)
        if previous_company['address_id'] is None:
            created, address_id = self.add_address(input)
            if created:
                self.c.execute('UPDATE company SET address_id = ? WHERE item_id = ?',(address_id,item_id))
        else:
            self.update_address(previous_company['address_id'],previous_company,input)
        self.commit()

    def update_address(self,address_id, previous, input):
        for possible_items in ['line1', 'line2','country','UK', 'postcode']:
            if possible_items in input:
                item = input[possible_items]
                if item is None or item == previous[possible_items]:
                    continue
                self.c.execute('UPDATE address set %s=? where address_id=?'%possible_items,(item,address_id))

    def add_address(self, input):
        address_id = self.get_next_address_id()
        created = False
        for possible_items in ['line1', 'line2','country','UK', 'postcode']:
            if possible_items in input:
                item = input[possible_items]
                if item is None:
                    continue
                if not created:
                    self.c.execute('INSERT into address(address_id,%s) VALUES(?,?)'%possible_items,(address_id,item))
                    created = True
                else:
                    self.c.execute('UPDATE address set %s=? where address_id=?'%possible_items,(item,address_id))
        return (created, address_id)

    def add_email_or_phone(self,input,item_id):
        if 'email_add' in input:
            self.c.execute('INSERT into email VALUES(?,?,?)',(self.get_next_email_id(),item_id,input['email_add']))
        if 'phone_add' in input:
            self.c.execute('INSERT into phone VALUES(?,?,?)',(self.get_next_phone_id(),item_id,input['phone_add']))

    def update_email_or_phone(self,input,previous, item_id):
        if 'emails' in input and previous['emails'] != input['emails']:
            for key,value in input['emails'].items():
                self.c.execute('UPDATE email SET email = ? WHERE item_id = ? AND email_id = ?' ,(value,item_id,key))
        if 'phones' in input and previous['phones'] != input['phones']:
            for key,value in input['phones'].items():
                self.c.execute('UPDATE phone SET phone_number = ? WHERE item_id = ? AND phone_id = ?' ,(value,item_id,key))

    def add_person(self,input):
        if 'first_name' not in input:
            return
        item_id = self.get_next_item_id()
        self.c.execute('INSERT into item_list VALUES(?)',(item_id,))
        self.c.execute('INSERT into people(item_id,first_name) VALUES(?,?)',(item_id,input['first_name']))
        if 'second_name' in input:
            self.c.execute('UPDATE people set second_name = ? WHERE item_id =?',(item_id,input['second_name']))
        if 'company' in input:
            company_id = self.get_company_id_from_name(input['company'])
            if company_id is not None:
                self.c.execute('UPDATE people set company_id = ? WHERE item_id =?',(company_id,item_id))
        self.add_email_or_phone(input,item_id)
        created, address_id = self.add_address(input)
        if created:
            self.c.execute('UPDATE people SET address_id = ? WHERE item_id = ?',(address_id,item_id))
        self.commit()

    def get_emails(self,item_id):
        self.c.execute('SELECT email_id,email from email where item_id = ?',(item_id,))
        return dict(self.c.fetchall())

    def get_phone(self,item_id):
        self.c.execute('SELECT phone_id,phone_number from phone where item_id = ?',(item_id,))
        return dict(self.c.fetchall())

    def get_companies(self, company_id = None):
        columns = ['item_id','name','address_id','line1','line2','country','postcode']
        main_query = 'SELECT item_id,name,company.address_id,line1,line2,country,postcode from company LEFT JOIN address ON(company.address_id=address.address_id)'
        if company_id is None:
            self.c.execute(main_query)
        else:
            self.c.execute(main_query+' WHERE item_id = ?',(company_id,))
        companies = []
        for db_result in self.c.fetchall():
            company = dict(zip(columns,db_result))
            self.append_emails_and_phones(company)
            companies.append(company)
        return companies

    def get_company(self, item_id):
        companies = self.get_companies(item_id)
        if len(companies) !=1:
            return []
        else:
            return companies[0]

    def append_emails_and_phones(self,item):
        emails = self.get_emails(item['item_id'])
        if len(emails)>0:
            item['emails']=emails
        phones = self.get_phone(item['item_id'])
        if len(phones)>0:
            item['phones']=phones


    def get_people(self, person_id = None):
        columns = ['item_id','first_name','second_name','company_id','address_id','line1','line2','country','postcode']
        main_query = 'SELECT item_id,first_name,second_name,company_id,people.address_id,line1,line2,country,postcode from people LEFT JOIN address ON(people.address_id=address.address_id)'
        if person_id is None:
            self.c.execute(main_query)
        else:
            self.c.execute(main_query+' WHERE item_id = ?',(person_id,))
        people = []
        for db_result in self.c.fetchall():
            person = dict(zip(columns,db_result))
            if person['company_id'] is not None:
                person['company_id']=str(person['company_id'])
            self.append_emails_and_phones(person)
            people.append(person)
        return people

    def get_person(self, item_id):
        people = self.get_people(item_id)
        if len(people) !=1:
            return []
        else:
            return people[0]

    def create(self):
        self.c.execute('''CREATE TABLE item_list(item_id integer  primary key)''')
        self.c.execute('''CREATE TABLE company (item_id integer primary key, name varchar unique, address_id integer DEFAULT NULL)''')
        self.c.execute('''CREATE TABLE people (item_id integer primary key, company_id integer DEFAULT NULL,first_name varchar, second_name varchar DEFAULT NULL, address_id integer DEFAULT NULL)''')
        self.c.execute('''CREATE TABLE address (address_id integer primary key, line1 varchar DEFAULT NULL, line2 varchar DEFAULT NULL, country varchar DEFAULT NULL, postcode varchar DEFAULT NULL)''')
        self.c.execute('''CREATE TABLE phone (phone_id INTEGER primary key, item_id INTEGER, phone_number varchar)''')
        self.c.execute('''CREATE TABLE email (email_id INTEGER primary key,item_id INTEGER, email varchar)''')
        self.commit()

    def commit(self):
        self.conn.commit()

    def populate(self):
        company_id = self.add_company({'name': 'Administrate', 'email': 'email@administrate.com', 'phone': '0134343',
                                     'line1': 'a street', 'line2': 'in edinburgh', 'country': 'UK', 'postcode': 'a postcode'})
        person_id = self.add_person({'first_name': 'Jane', 'second_name': 'Doe', 'email': 'jane.doe@administrate.com',
                           'line1': 'another street', 'line2': 'in Glasgow', 'country': 'UK',
                                       'postcode': 'another postcode','company':'Administrate'})


#db = Database()
#db.create()
#db.populate()
#companies =db.get_companies()
#company = db.get_company(1)
#people =db.get_people()
#person = db.get_person(2)
#item_id = db.get_auto_increment('item_id','item_list')
b=2

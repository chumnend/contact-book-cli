import click
import sqlite3

@click.group()
def contacts():
    pass

@contacts.command()
def init():
    """ 
    creates an SQLite database file to store contact information
    """
    conn = None
    try:
        conn=sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("CREATE TABLE contacts (id integer PRIMARY KEY AUTOINCREMENT, name text, phone text, address text);")
    except sqlite3.Error as e:
        print(e)
    
    if(conn):
        conn.close()
        
@contacts.command()
def list():
    """
    list all contacts current in the db
    """
    conn = None 
    try:
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM contacts;")
        rows = c.fetchall()
        
        if(len(rows) == 0):
            click.echo("no contacts found.")
        else:
            for row in rows:
                click.echo(row)
    except sqlite3.Error as e:
        print(e)
    
    if(conn):
        conn.close()

@contacts.command()
@click.option("--name", help="contact's name")
@click.option("--phone", help="contact's phone number")
@click.option("--address", help="contact's address")
def create(name, phone, address):
    """
    adds new contact to the db
    """
    if(name is None):
        name = click.prompt("Enter Contact Name: ")
    
    if(phone is None):
        phone = click.prompt("Enter Contact Phone Number: ")
        
    if(address is None):
        address = click.prompt("Enter Contact Address: ")
        
    click.echo("\nName: %s\nPhone: %s\nAddress: %s\n" % (name, phone, address))
    
    if(click.confirm('Do you want to continue?')):
        conn = None
        try:
            conn=sqlite3.connect("contacts.db")
            c = conn.cursor()
            c.execute("INSERT INTO contacts (name, phone, address) VALUES (?,?,?);", (name, phone, address))
            conn.commit()
            click.echo("contact created.")
        except sqlite3.Error as e:
            print(e)
        
        if(conn):
            conn.close()
    else:
        click.echo("contact creation aborted.")
    
@contacts.command()
@click.argument("id")
def show(id):
    """shows a specific user given id"""
    conn = None
    try:
        conn=sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("SELECT name, phone, address FROM contacts WHERE id=?;", (id,))
        row = c.fetchone()
        
        if(row is None):
            click.echo("contact does not exist.")
        else:
            click.echo(row)
    except sqlite3.Error as e:
        print(e)
    
    if(conn):
        conn.close()
    
@contacts.command()
@click.option("--name", help="new contact name")
@click.option("--phone", help="new contact phone number")
@click.option("--address", help="new contact address")
@click.argument("id")
def update(id, name, phone, address):
    """updates a specific user given id"""
    if(name is None):
        name = click.prompt("Enter New Contact Name: ")
    
    if(phone is None):
        phone = click.prompt("Enter New Contact Phone Number: ")
        
    if(address is None):
        address = click.prompt("Enter New Contact Address: ")
        
    click.echo("\nNew Name: %s\nNew Phone: %s\nNew Address: %s\n" % (name, phone, address))
    
    if(click.confirm('Do you want to continue?')):
        conn = None
        try:
            conn=sqlite3.connect("contacts.db")
            c = conn.cursor()
            c.execute("UPDATE contacts SET name=?, phone=?, address=? WHERE id=?;", (name, phone, address, id))
            conn.commit()
            click.echo("contact updated.")
        except sqlite3.Error as e:
            print(e)
        
        if(conn):
            conn.close()
    else:
        click.echo("contact update aborted.")


@contacts.command()
@click.argument("id")
def delete(id):
    """deletes a specific user given id"""
    conn = None
    try:
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("DELETE FROM contacts WHERE id=?;", (id,))
        conn.commit()
        click.echo("contact deleted.")
    except sqlite3.Error as e:
        print(e)
    
    if(conn):
        conn.close()

@contacts.command()
def purge():
    """clears all contact information from db"""
    if(click.confirm('WARNING: THIS WILL ERASE ALL CONTACTS. Do you want to continue?')):
        conn = None
        try:
            conn = sqlite3.connect("contacts.db")
            c = conn.cursor()
            c.execute("DELETE FROM contacts;")
            conn.commit()
            click.echo("all contacts deleted.")
        except sqlite3.Error as e:
            print(e)
        
        if(conn):
            conn.close()
    else:
        click.echo("contact purge aborted.")

if __name__ == "__main__":
    contacts()
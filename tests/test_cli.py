from contacts.app import contacts
import click
from click.testing import CliRunner
import pathlib

def test_cli():
    runner = CliRunner() 
    
    with runner.isolated_filesystem():
        # testing if db file is created
        result = runner.invoke(contacts, ['init'])
        path = pathlib.Path('contacts.db')
        assert result.exit_code == 0
        assert path.exists() is True
        
        # testing listening with empty contact book
        result = runner.invoke(contacts, ["list"])
        assert result.exit_code == 0
        assert result.output == "no contacts found.\n"
        
        # testing contact creation 
        result = runner.invoke(contacts, ["create", "--name", "tester", "--phone", "123 456 789", "--address", "123 ABC Street"], input="y\n")
        assert result.exit_code == 0
        assert not result.exception
        
        # testing listing contact
        result = runner.invoke(contacts, ["list"])
        assert result.exit_code == 0
        assert result.output == "(1, 'tester')\n"
    
        # testing showing contact
        result = runner.invoke(contacts, ["show", "1"])
        assert result.exit_code == 0
        assert result.output == "('tester', '123 456 789', '123 ABC Street')\n"
        
        # testing update contact
        result = runner.invoke(contacts, ["update", "1", "--name", "tester2", "--phone", "789 456 123", "--address", "321 ABC Street"], input="y\n")
        assert result.exit_code == 0
        assert not result.exception
        
        result = runner.invoke(contacts, ["show", "1"])
        assert result.exit_code == 0
        assert result.output == "('tester2', '789 456 123', '321 ABC Street')\n"
        
        # testing delete contact
        result = runner.invoke(contacts, ["delete", "1"])
        assert result.exit_code == 0
        assert result.output == "contact deleted.\n"
        
        # testing purge contacts
        result = runner.invoke(contacts, ["create", "--name", "1", "--phone", "1", "--address", "1"], input="y\n")
        result = runner.invoke(contacts, ["create", "--name", "2", "--phone", "2", "--address", "2"], input="y\n")
        result = runner.invoke(contacts, ["create", "--name", "3", "--phone", "3", "--address", "3"], input="y\n")
        
        result = runner.invoke(contacts, ["list"])
        assert result.exit_code == 0
        assert result.output == "(2, '1')\n(3, '2')\n(4, '3')\n"
        
        result = runner.invoke(contacts, ["purge"], input="y\n")
        assert result.exit_code == 0
        assert not result.exception
        
        result = runner.invoke(contacts, ["list"])
        assert result.exit_code == 0
        assert result.output == "no contacts found.\n"
        
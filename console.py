#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import shlex
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in the usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formatting - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as an empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' and type(eval(pline)) is dict:
                       _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """Create an object of any class with given parameters"""
        if not args:
            print("** class name missing **")
            return

        # Split the arguments into class name and parameters
        args_list = shlex.split(args)
        class_name = args_list[0]
        param_str = ' '.join(args_list[1:])

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Parse parameters into a dictionary
        params = {}
        try:
            # Split parameters by space
            param_list = param_str.split(' ')

            for param in param_list:
                # Split each parameter by '=' to get key-value pair
                key, value = param.split('=')

                # Process value based on its type
                if value[0] == '"' and value[-1] == '"':
                    # String value enclosed in double quotes
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    # Float value
                    value = float(value)
                elif value.isdigit():
                    # Integer value
                    value = int(value)

                    # Add key-value pair to the params dictionary
                    params[key] = value

        except Exception as e:
            print(f"Error parsing parameters: {e}")
            return

        # Create an instance of the specified class with the given parameters
        new_instance = HBNBCommand.classes[class_name](**params)

        storage.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type with given parameters")
        print("[Usage]: create <className> <param1>=<value1> <param2>=<value2> ...\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

        def do_destroy(self, args):
            """ Destroys a specified object """
            new = args.partition(" ")
            c_name = new[0]
            c_id = new[2]
            if c_id and ' ' in c_id:
                c_id = c_id.partition(' ')[0]

            if not c_name:
                print("** class name missing **")
                return

            if c_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            if not c_id:
                print("** instance id missing **")
                return

            key = c_name + "." + c_id
            try:
                del storage.all()[key]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys a specified instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Prints all instances or all instances of a class """
        if args not in HBNBCommand.classes and args:
            print("** class doesn't exist **")
            return

        obj_list = [str(obj) for key, obj in storage.all().items()
                    if not args or type(obj) == HBNBCommand.classes[args]]
        print(obj_list)

    def help_all(self):
        """ Help information for the all command """
        print("Prints all instances or all instances of a class")
        print("[Usage]: all [className]\n")

    def do_count(self, args):
        """ Counts the instances of a class """
        if args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        count = sum(1 for obj in storage.all().values()
                    if type(obj) == HBNBCommand.classes[args])
        print(count)

    def help_count(self):
        """ Help information for the count command """
        print("Counts the instances of a class")
        print("[Usage]: count <className>\n")

    def do_update(self, args):
        """ Updates a certain object with new information """
        if not args:
            print("** class name missing **")
            return

        # Split the arguments into class name, id, attribute, and value
        args_list = shlex.split(args)
        class_name = args_list[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:
            print("** instance id missing **")
            return

        instance_id = args_list[1]
        key = f"{class_name}.{instance_id}"

        if key not in storage.all():
            print("** no instance found **")
            return

        if len(args_list) < 3:
            print("** attribute name missing **")
            return

        attribute = args_list[2]

        if len(args_list) < 4:
            print("** value missing **")
            return

        value_str = args_list[3]

        # Try to convert the value to the correct type
        try:
            value = eval(value_str)
        except (NameError, SyntaxError):
            print("** invalid value **")
            return

        # Update the attribute with the new value
        instance = storage.all()[key]
        setattr(instance, attribute, value)
        instance.save()

    def help_update(self):
        """ Help information for the update command """
        print("Updates an object with new information")
        print("[Usage]: update <className> <id> <attribute> <value>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()

import sys


class DataExtractor:

    @staticmethod
    def get_data(*args, **kwargs) -> str:
        """Data retrieval.
        If the data are entered on the command line, then we use them.
        In this case we work as a utility.
        Otherwise, if the data came in 'args', the program works in library mode.
        There is no third way."""
        cmd = args or sys.argv[1:]
        data, is_path = DataExtractor.this_is_the_way(*cmd)
        prep_data = DataExtractor.get_file_data(data) if is_path else data
        return prep_data

    @staticmethod
    def get_file_data(path: str) -> str:
        data = ""
        try:
            with open(path) as f:
                data = f.read()
        except FileNotFoundError:
            error_messages = """
            If you are trying to check a file make sure that the path is correct. 
            The calculation will be done on this data as a line."""
            print(error_messages)
        return data or path

    @staticmethod
    def this_is_the_way(path='', *args) -> (str, bool):
        """"The first element of the input data is always either a path or data.
        If there is nothing on the first position then the user has not entered anything."""
        is_path = False
        if not isinstance(path, str):
            return "", None
        if path:
            str_path = str(path)
            is_path = str_path.find('/') != -1 and str_path[-4:].find('.') != -1
            is_path = is_path or (len(str_path) < 20 and str_path[-4:].find('.') != -1) or False
        return path, is_path


class StaplesControl:

    def __init__(self, data):
        self.stap = ("()", "[]", "{}")
        self.slen = 0
        self.data = data

    def remove_part(self, part: str):
        """Remove part from data."""
        self.data = self.data.replace(part, "")

    def one_step(self):
        """Deletes parts of the data one by one."""
        for part in self.stap:
            self.remove_part(part)
            self.remove_part(part)

    def clear_string(self):
        """Removes parts from the data as long as the data can be deleted."""
        while self.slen != len(self.data):
            self.slen = len(self.data)
            self.one_step()

    def result(self) -> bool:
        """Returns True if true otherwise False."""
        return not self.data

    def run(self):
        self.clear_string()
        return self.result()


class DataPreparation:
    """This class is designed to remove all characters from the data except those in 'white_list_chr'."""
    white_list_chr = ['(', '[', '{', ')', ']', '}']

    @staticmethod
    def valid_character(character: str) -> bool:
        return character in DataPreparation.white_list_chr

    @staticmethod
    def clean_string(string: str) -> filter:
        return filter(DataPreparation.valid_character, string)

    @staticmethod
    def get_clean_data(data: str) -> str:
        return "".join(DataPreparation.clean_string(data))


class StaplesDataObject:

    def __init__(self, data):
        self.data = data
        self.prep = DataPreparation
        self.ctrl = StaplesControl

    def run(self):
        return StaplesControl(DataPreparation.get_clean_data(self.data)).run()

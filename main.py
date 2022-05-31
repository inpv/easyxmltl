import os
import datetime as dt
from lxml import etree


class Main:

    parser = None
    file_object = None
    root = None
    doc_type = None
    steps_counter = 0
    time_range = 0

    @staticmethod
    def renumber_steps(tag):  # creates a new step index and writes to the tag
        Main.steps_counter += 1
        new_text = etree.CDATA(str(Main.steps_counter))
        tag.text = new_text

    @staticmethod
    def process_document(destination):  # loops through the entire XML document and writes to it

        Main.parser = etree.XMLParser(strip_cdata=False)
        Main.file_object = etree.parse(destination, parser=Main.parser)
        Main.root = Main.file_object.getroot()

        Main.steps_counter = 0

        if Main.doc_type == 1:
            for child in Main.root:
                for subchild in child:
                    for grandchild in subchild:
                        for grandgrandchild in grandchild:
                            if grandgrandchild.tag == "step_number":
                                Main.renumber_steps(grandgrandchild)

                        if grandchild.getnext() is None:
                            Main.steps_counter = 0

        elif Main.doc_type == 2:
            for child in Main.root:
                for subchild in child:
                    for grandchild in subchild:
                        for grandgrandchild in grandchild:
                            for grandgrandgrandchild in grandgrandchild:
                                if grandgrandgrandchild.tag == "step_number":
                                    Main.renumber_steps(grandgrandgrandchild)

                            if grandgrandchild.getnext() is None:
                                Main.steps_counter = 0

        Main.file_object.write(destination, encoding="utf-8", xml_declaration=True)

        print("File at dest " + destination + " written successfully!")

    @staticmethod
    def process_files():  # processes all recently updated XML files within a set time range
        now = dt.datetime.now()
        ago = now - dt.timedelta(minutes=Main.time_range)
        user = os.getlogin()
        files_arr = []

        for root, dirs, files in os.walk('C:\\Users\\' + str(user) + '\\Downloads\\'):
            for fname in files:
                path = os.path.join(root, fname)
                st = os.stat(path)
                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                if mtime > ago:
                    file_ext = os.path.splitext(path)[-1]
                    if file_ext == '.xml':
                        files_arr.append(path)

        for file in files_arr:
            Main.process_document(file)

    @staticmethod
    def main():
        print()
        print("Welcome to easyxmltl, a utility for bulk TestLink test case editing.")
        print()
        print("Set the time range (in minutes) for the files you wish to process.")
        Main.time_range = int(input("Time range: "))
        print()
        print("Set the document type you wish to process.")
        print("1. Test case")
        print("2. Test suite")
        print()
        Main.doc_type = int(input("Document type: "))
        print()
        print("Starting process...")
        Main.process_files()


if __name__ == "__main__":
    Main.main()

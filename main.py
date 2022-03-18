import os
import re
import datetime as dt
from bs4 import BeautifulSoup
from lxml import etree


class Main:

    temp_tag = None
    steps_counter = 0

    parser = None
    file_object = None
    root = None

    xml_string = """
    <step>
        <step_number><![CDATA[]]></step_number>
        <actions>
        </actions>
        <expectedresults>
        </expectedresults>
        <execution_type><![CDATA[]]></execution_type>
    </step>"""

    @staticmethod
    def add_new_steps(local_grandgrandchild):

        tag = etree.fromstring(Main.xml_string, Main.parser)

        for subtag in tag:
            if subtag.tag == "step_number":
                inner_text_step_number = etree.CDATA(str(2))
                subtag.text = inner_text_step_number
            elif subtag.tag == "actions":
                inner_text_actions = etree.CDATA(str())
                subtag.text = inner_text_actions
            elif subtag.tag == "expectedresults":
                inner_text_results = etree.CDATA(str())
                subtag.text = inner_text_results
            elif subtag.tag == "execution_type":
                inner_text_execution_type = etree.CDATA(str(1))
                subtag.text = inner_text_execution_type

        local_grandgrandchild.addnext(tag)

    @staticmethod
    def slice_inner_tags(local_grandgrandgrandchild, local_grandgrandchild):

        inner_text = BeautifulSoup(local_grandgrandgrandchild.text, features="lxml")
        inner_counter = 0

        for tag in inner_text.find_all(re.compile("^p")):
            inner_counter += 1

            if inner_counter == 1:
                Main.temp_tag = tag

            elif inner_counter > 1:
                Main.add_new_steps(local_grandgrandchild)
                # local_grandgrandgrandchild.text = etree.CDATA(str(Main.temp_tag))

    @staticmethod
    def renumber_steps(tag):
        Main.steps_counter += 1
        new_text = etree.CDATA(str(Main.steps_counter))
        tag.text = new_text

    @staticmethod
    def switch_modes(grandgrandgrandchild, grandgrandchild):  # switches editing modes based on tag name
        if grandgrandgrandchild.tag == "step_number":
            pass
            # Main.renumber_steps(grandgrandgrandchild)

        elif grandgrandgrandchild.tag == "actions":
            # pass
            Main.slice_inner_tags(grandgrandgrandchild, grandgrandchild)

        elif grandgrandgrandchild.tag == "expectedresults":
            pass

    @staticmethod
    def process_document(destination):  # loops through the entire XML document and writes to it

        Main.parser = etree.XMLParser(strip_cdata=False)
        Main.file_object = etree.parse(destination, parser=Main.parser)
        Main.root = Main.file_object.getroot()

        Main.steps_counter = 0

        for child in Main.root:
            for subchild in child:
                for grandchild in subchild:
                    for grandgrandchild in grandchild:
                        for grandgrandgrandchild in grandgrandchild:
                            Main.switch_modes(grandgrandgrandchild, grandgrandchild)

                        if grandgrandchild.getnext() is None:
                            Main.steps_counter = 0

        Main.file_object.write(destination, encoding="utf-8", xml_declaration=True)

        print("File at dest " + destination + " written successfully!")

    @staticmethod
    def main():  # processes all recently updated XML files within a set time range
        now = dt.datetime.now()
        ago = now - dt.timedelta(minutes=360)
        user = os.getlogin()
        files_arr = []

        for root, dirs, files in os.walk('C:\\Users\\'+str(user)+'\\Downloads\\'):
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


if __name__ == "__main__":
    Main.main()

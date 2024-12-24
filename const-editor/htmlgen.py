# From : An_HTML_Table_Generator_in_Python blog by GeoffreyBrown

import io
import html
import urllib.parse

class genrow():

    def __init__(self, tabdef):
        self.__tabdef = tabdef
        self.__markup = ""

    def __enter__(self):
        self.__markup += "<tr>\n"
        return self

    def __exit__(self, *exc):
        self.__markup += "</tr>\n"
        return False

    def setmarkup(self, row):

        self.__markup += f"""<td><input type="checkbox" onclick="updateidlist(this.checked, '{row["id"]}')"></td>\n"""

        for coldef in self.__tabdef:

            if "protocol" not in coldef or coldef["protocol"] == "":
                self.__markup += f"""<td>{html.escape(row[coldef["name"]])}</td>\n"""

            elif coldef["protocol"] == "id":
                self.__markup += f"""<td><a onclick="location = './user/{row["id"]}'; return false;" href="">{html.escape(row[coldef["name"]])}</a><td>\n"""

            elif coldef["protocol"] == "mailto":
                self.__markup += f"""<td><a href="mailto:{urllib.parse.quote(row[coldef["name"]])}" target="_blank">{html.escape(row[coldef["name"]])}</a></td>\n"""

    def getmarkup(self):
        return self.__markup


def gentable(f):
    def closure():
        data, tabdef = f()

        out = io.StringIO()
        write = out.write

        #####
        #
        # table
        #
        write("<table>\n")
        write("<colgroup><col/></colgroup>\n")

        #####
        #
        # thead
        #
        write("<thead>\n")
        write("<tr>\n")
        write("<td/>\n")

        for coldef in tabdef:
            write(f"""<td>{coldef["prompt"]}</td>\n""")

        write("</tr>\n")
        write("</thead>\n")
        #
        # thead
        #
        #####


        #####
        #
        # tfoot
        #
        write("<tfoot>\n")
        write(f"""<td colspan="{len(tabdef)}">{len(data)} object(s)</td>\n""")
        write("</tfoot>\n")
        #
        # tfoot
        #
        #####

        #####
        #
        # tbody
        #
        write("<tbody>\n")

        with genrow(tabdef) as rg:
            for row in data:
                rg.setmarkup(row)
                write(rg.getmarkup())

        write("</tbody>\n")
        #
        # tbody
        #
        #####

        write("</table>\n")
        #
        # table
        #
        #####

        return out.getvalue()
    return closure


@gentable
def gettable():

    data = (
        {"id":"1", "name":"homer", "fullname":"Homer Simpson", "company":"Simpson Inc.", "orgunit":"", "external":"No", "email":"homer@simpson.biz"},
        {"id":"2", "name":"marge", "fullname":"Marge Simpson", "company":"Simpson Inc.", "orgunit":"", "external":"No", "email":"marge@simpson.biz"},
    )

    return (
        data,
        (
            {"prompt":"Name", "name":"name", "protocol":"id", "key":"name"},
            {"prompt":"Full Name", "name":"fullname", "key":"fullname"},
            {"prompt":"Company", "name":"company", "key":"company"},
            {"prompt":"Organizational Unit", "name":"orgunit", "key":"orgunit;name"},
            {"prompt":"External", "name":"external", "key":"external"},
            {"prompt":"e-Mail Address", "name":"email", "protocol":"mailto", "key":"email"},
        ),
    )

print(gettable())

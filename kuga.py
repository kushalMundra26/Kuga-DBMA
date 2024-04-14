import csv

class BTreeNode:
    def __init__(self, keys=[], children=[], is_leaf=True):
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf


class BTree:
    def __init__(self, degree):
        self.root = BTreeNode()
        self.degree = degree

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and str(key) > str(node.keys[i]):
            i += 1
        if i < len(node.keys) and str(key) == str(node.keys[i]):
            return True
        if node.is_leaf:
            return False
        else:
            return self.search(key, node.children[i])

    def insert(self, key):
        key = str(key)
        if self.search(key):
            return
        if len(self.root.keys) == (2 * self.degree) - 1:
            new_root = BTreeNode(children=[self.root])
            self.split_child(new_root, 0)
            self.root = new_root
        self.insert_non_full(self.root, key)

    def insert_non_full(self, node, key):
        key = str(key)
        i = len(node.keys) - 1
        if node.is_leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.degree) - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key)

    def split_child(self, parent, index):
        child = parent.children[index]
        new_child = BTreeNode(
            keys=child.keys[self.degree:], 
            children=child.children[self.degree:], 
            is_leaf=child.is_leaf
        )
        child.keys = child.keys[:self.degree - 1]
        child.children = child.children[:self.degree]
        parent.keys.insert(index, child.keys.pop())
        parent.children.insert(index + 1, new_child)

    def delete(self, key):
        key = str(key)
        if not self.search(key):
            return
        self.delete_key(self.root, key)

    def delete_key(self, node, key):
        key = str(key)
        i = 0
        while i < len(node.keys) and str(key) > str(node.keys[i]):
            i += 1
        if i < len(node.keys) and str(key) == str(node.keys[i]):
            if node.is_leaf:
                del node.keys[i]
            else:
                pred = self.get_predecessor(node, i)
                node.keys[i] = pred
                self.delete_key(node.children[i], pred)
        else:
            if node.is_leaf:
                return
            elif len(node.children[i].keys) >= self.degree:
                self.delete_key(node.children[i], key)
            else:
                if i > 0 and len(node.children[i-1].keys) >= self.degree:
                    self.borrow_from_prev(node, i)
                elif i < len(node.keys) and len(node.children[i+1].keys) >= self.degree:
                    self.borrow_from_next(node, i)
                else:
                    if i < len(node.keys):
                        self.merge(node, i)
                    else:
                        self.merge(node, i-1)
                    self.delete_key(node.children[i], key)

    def borrow_from_prev(self, node, index):
        child = node.children[index]
        sibling = node.children[index - 1]
        child.keys.insert(0, node.keys[index - 1])
        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())
        node.keys[index - 1] = sibling.keys.pop()

    def borrow_from_next(self, node, index):
        child = node.children[index]
        sibling = node.children[index + 1]
        child.keys.append(node.keys[index])
        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))
        node.keys[index] = sibling.keys.pop(0)

    def merge(self, node, index):
        child = node.children[index]
        sibling = node.children[index + 1]
        child.keys.append(node.keys.pop(index))
        child.keys.extend(sibling.keys)
        if not child.is_leaf:
            child.children.extend(sibling.children)
        node.children.pop(index + 1)

    def inorder_traversal(self, node=None):
        if node is None:
            node = self.root
        if not node.is_leaf:
            for i in range(len(node.keys)):
                yield from self.inorder_traversal(node.children[i])
                yield node.keys[i]
            yield from self.inorder_traversal(node.children[len(node.keys)])
        else:
            for key in node.keys:
                yield key


class DBMS:
    def __init__(self):
        self.tables = {}

    def create_table(self, table_name, num_columns, column_names=None):
        if column_names is None:
            column_names = ['Column{}'.format(i + 1) for i in range(num_columns)]
        self.tables[table_name] = {'columns': num_columns, 'indexes': [BTree(2) for _ in range(num_columns)], 'data': [], 'column_names': column_names}

    def insert(self, table_name, row):
        table = self.tables.get(table_name)
        if table:
            if len(row) == table['columns']:
                converted_row = []
                for index, value in enumerate(row):
                    column_type = type(table['data'][0][index]) if table['data'] else type(value)
                    converted_row.append(column_type(value))
                    table['indexes'][index].insert(column_type(value))
                table['data'].append(converted_row)
            else:
                print("Number of columns doesn't match the table schema.")
        else:
            print("Table not found.")

    def delete(self, table_name, key_column, key_value):
        table = self.tables.get(table_name)
        if table:
            key_index = None
            for i, name in enumerate(table['column_names']):
                if name == key_column:
                    key_index = i
                    break
            if key_index is None:
                print("Key column not found.")
                return

            btree = table['indexes'][key_index]
            for row in table['data']:
                if str(key_value) == str(row[key_index]):
                    table['data'].remove(row)
                    btree.delete(key_value)
                    print("Record deleted successfully.")
                    return
            print("Key not found.")
        else:
            print("Table not found.")


    def search(self, table_name, column_name, key):
        table = self.tables.get(table_name)
        if table:
            index = None
            for i, name in enumerate(table['column_names']):
                if name == column_name:
                    index = i
                    break
            if index is None:
                print("Column not found.")
                return []

            result = []
            for row in table['data']:
                if str(key) == str(row[index]):
                    result.append(row)
            if result:
                return result
            else:
                print("Key not found.")
                return []
        else:
            print("Table not found.")
            return []

    def update(self, table_name, key_column, key_value, update_dict):
        table = self.tables.get(table_name)
        if table:
            key_index = None
            for i, name in enumerate(table['column_names']):
                if name == key_column:
                    key_index = i
                    break
            if key_index is None:
                print("Key column not found.")
                return 

            btree = table['indexes'][key_index]
            for row in table['data']:
                if str(key_value) == str(row[key_index]):
                    for column_name, new_value in update_dict.items():
                        column_index = None
                        for i, name in enumerate(table['column_names']):
                            if name == column_name:
                                column_index = i
                                break
                        if column_index is None:
                            print("Column '{}' not found.".format(column_name))
                            return
                        row[column_index] = new_value
                        if isinstance(key_value, int) or isinstance(key_value, float):
                            btree.delete(key_value)
                            btree.insert(str(key_value))
                        else:
                            btree.delete(str(key_value))
                            btree.insert(key_value)
                    print("Record updated successfully.")
                    return
            print("Key not found.")
        else:
            print("Table not found.")


    def display_table(self, table_name):
        table = self.tables.get(table_name)
        if table:
            print("Table:", table_name)
            print("Column Names:", table['column_names'])
            print("Data:")
            for row in table['data']:
                print(row)
            print()
        else:
            print("Table not found.")
            
    def export_to_csv(self, table_name, file_name):
        table = self.tables.get(table_name)
        if table:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(table['column_names'])  # Write column headers
                writer.writerows(table['data'])  # Write table data
            print("Table '{}' data exported to '{}' successfully.".format(table_name, file_name))
        else:
            print("Table not found.")
    
    def import_from_csv(self, table_name, file_name):
        with open(file_name, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        if table_name not in self.tables:
            # Create the table if it doesn't exist
            if len(rows) > 0:
                # Assuming the first row contains column headings
                column_names = rows[0]
                self.create_table(table_name, len(column_names), column_names)
                print("Table '{}' created.".format(table_name))
            else:
                print("No data found in the CSV file.")
                return

        table = self.tables[table_name]
        if len(rows) > 0:
            # Assuming the first row contains column headings
            column_names = rows[0]
            if column_names != table['column_names']:
                print("Column names in CSV do not match the table schema.")
                return

            # Assuming the rest of the rows contain data
            for row in rows[1:]:
                if len(row) != table['columns']:
                    print("Number of columns in CSV does not match the table schema.")
                    return
                converted_row = []
                for index, value in enumerate(row):
                    column_type = type(table['data'][0][index]) if table['data'] else str
                    converted_row.append(column_type(value))
                    table['indexes'][index].insert(column_type(value))
                table['data'].append(converted_row)
            print("Data imported from '{}' into table '{}' successfully.".format(file_name, table_name))
        else:
            print("No data found in the CSV file.")

            
def check_tokens(tokens):
    if len(tokens) < 2:
        print("Error: Insufficient tokens.")
        print("Format 1: create table <table_name> <column_headings>")
        print("Format 2: insert in <csv_table_name> <data_entries>")
        print("Format 3: update <csv_table_name> <column_name> <new_value> where <condition_column> = <condition_value>")
        print("Format 4: delete from <csv_table_name> where <condition_column> = <condition_value>")
        print("Format 5: select * from <csv_table_name> where <condition_column> = <condition_value>")
        print("Format 6: export to <csv_file_name> from <csv_table_name>")
        print("Format 7: import <csv_file_name> as <csv_table_name>")
        return False
    if tokens[0] == "create" and tokens[1] == "table":
        return True
    elif tokens[0] == "insert" and tokens[1] == "in":
        return True
    elif tokens[0] == "update" or tokens[0] == "delete":
        return True
    elif tokens[0] == "select" and tokens[1] == "*" and tokens[2] == "from":
        return True
    elif tokens[0] == "export" and tokens[1] == "to":
        return True
    elif tokens[0] == "import":
        return True
    print("Error: Invalid command format.")
    print("Format 1: create table <table_name> <column_headings>")
    print("Format 2: insert in <csv_table_name> <data_entries>")
    print("Format 3: update <csv_table_name> <column_name> <new_value> where <condition_column> = <condition_value>")
    print("Format 4: delete from <csv_table_name> where <condition_column> = <condition_value>")
    print("Format 5: select * from <csv_table_name> where <condition_column> = <condition_value>")
    print("Format 6: export to <csv_file_name> from <csv_table_name>")
    print("Format 7: import <csv_file_name> as <csv_table_name>")
    return False
    
    
def main():
    user_input = input("kuga dbms> ")
    tokens = user_input.split()
    global column_headings

    # Check if tokens meet the specified format
    if not check_tokens(tokens):
        return 1  # Terminate program if tokens are invalid

    # If the command is in the "insert in" format, insert data into the CSV file
    if tokens[0] == "insert" and tokens[1] == "in":
        table_name = tokens[2]
        data_to_insert = [token.strip('()') for token in tokens[3].split(',')]  # Remove brackets
        dbms.insert(table_name, data_to_insert)
        dbms.display_table(table_name)
        
    # If the command is in the "update" format, update data in the CSV file
    elif tokens[0] == "update":
        table_name = tokens[1]
        column_name = tokens[2]
        new_value = tokens[3]
        condition_column = tokens[5]
        condition_value = tokens[7]
        dbms.update(table_name, condition_column, condition_value,{column_name:new_value} )
        dbms.display_table(table_name)
    # If the command is in the "delete from" format, delete data from the CSV file
    elif tokens[0] == "delete" and tokens[1] == "from":
        table_name = tokens[2]
        condition_column = tokens[4]
        condition_value = tokens[6]
        dbms.delete(table_name, condition_column, condition_value)
        dbms.display_table(table_name)

    elif tokens[0] == "select" and tokens[1] == "*" and tokens[2] == "from":
        if "where" not in tokens:
            table_name = tokens[3]
            dbms.display_table(table_name)
        else:
            table_name = tokens[3]
            condition_column = tokens[5]
            condition_value = tokens[7]
            print(dbms.search(table_name, condition_column, condition_value))

    elif tokens[0] == "export" and tokens[1] == "to":
        file_name = tokens[2]+".csv"
        table_name= tokens[4]
        dbms.export_to_csv(table_name, file_name)

    #import abc as bca
    elif tokens[0] == "import":
        if "as" in tokens:
            file_name = tokens[1]+".csv"
            dbms.import_from_csv(tokens[3],file_name)
        else:
            file_name = tokens[1]+".csv"
            table_name = tokens[1]
            dbms.import_from_csv(table_name, file_name)

    # Otherwise, assume it's in the "create table" format
    else:
        # Creating a CSV file with column headings
        table_name = tokens[2]
        column_headings = [heading.strip('()') for heading in tokens[3].split(',')]  # Remove brackets
        dbms.create_table(table_name, len(column_headings), column_headings)
        print("current table")
        dbms.display_table(table_name)

if __name__ == "__main__":
    print("Format 1: create table <table_name> <column_headings>")
    print("Format 2: insert in <csv_table_name> <data_entries>")
    print("Format 3: update <csv_table_name> <column_name> <new_value> where <condition_column> = <condition_value>")
    print("Format 4: delete from <csv_table_name> where <condition_column> = <condition_value>")
    print("Format 5: select * from <csv_table_name> where <condition_column> = <condition_value>")
    print("Format 6: export to <csv_file_name> from <csv_table_name>")
    print("Format 7: import <csv_file_name> as <csv_table_name>")
    dbms = DBMS()
    while True:
        main()
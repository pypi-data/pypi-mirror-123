__version__ = "4.0.0";

import json, os;

class DB:
    """
    Creates a new instance of a database.

    Argument 1 -> dict.

    Dicts Values:
    name - Name of database.
    directory - Sets directory of file. (Optional)
    path - Sets path of file, overrides directories and file naming. (Optional)
    """
    
    # Essentials #
    def __init__(self, config: dict):
        """Creates a new instance of a database."""

        if "name" in config.keys():
            self.name = config["name"];
        else:
            err = "\u001b[31mConfig object must contain attribute \"name\".\u001b[37m";
            raise AttributeError(err) from None;
        if "path" in config.keys():
            self.path = config["path"];
        elif "directory" in config.keys() or "folder" in config.keys():
            self.directory = config["directory"];
            self.path = os.path.join(self.directory, f"{self.name}.json");
        else:
            self.path = os.path.join(f"{self.name}.json");

        if not os.path.exists(self.path):
            if hasattr(self, "directory") and not os.path.isdir(self.directory):
                try:
                    os.mkdir(os.path.join(self.directory));
                    with open(self.path, "w") as f: f.write(json.dumps({self.name: []}));
                except Exception as err:
                    raise err;
            else:
                with open(self.path, "w") as f: f.write(json.dumps({self.name: []}));
        
        with open(self.path, "r") as f:
            if f.read() == "":
                with open(self.path, "w") as db:
                    db.write(json.dumps({self.name: []}));

    def __repr__(self):
        return "Database Object";
    
    def __gt__(self, k):
        db = self.all();
        for obj in db[self.name]:
            if "key" in obj and "arr" in obj and not "data" in obj:
                if obj["key"] == k:
                    return {"key": obj["key"], "arr": obj["arr"], "index": db[self.name].index(obj)};
                else:
                    continue;
        return None;
        
    def __ga__(self, k):
        db = self.all();

        for item in db[self.name]:
            if "key" in item and "data" in item and not "arr" in item:
                if item["key"] == k:
                    return {"key": item["key"], "data": item["data"], "index": db[self.name].index(item)};
            else:
                continue;
        return None;


    # STANDARD KEY STORAGE STARTS #
    def all(self):
        """
        Returns all objects in database.
        """
        try:
            with open(self.path, "r") as f: return json.loads(f.read());
        except:
            with open(self.path, "w") as f: f.write(json.dumps({self.name: []}));

    def keys(self):
        """
        Returns all keys in database.
        """

        db = self.all();
        
        l = [];

        for item in db[self.name]:
            if "data" in item and not "arr" in item:
                l.append(item);
            else:
                continue;
        return l;
                
    def get(self, key: str):
        """
        Gets value of given key in database.

        qik.get("example") -> \"Hello, World!\"
        """

        if self.exists(key):
            return self.__ga__(key)["data"];
        else:
            err = "\u001b[31mCannot get the value of a non existent key.\u001b[37m";
            raise RuntimeError(err) from None;

    def exists(self, key: str):
        """
        Checks if given key exists in database.

        qik.exists("example") -> True
        """

        if self.__ga__(key) == None:
            return False;
        else:
            return True;
            
    def set(self, key: str, data):
        """
        Sets given key to a value in database.

        qik.set(\"example\", \"Hello, World!\") -> \"Hello, World!\"
        """

        db = self.all();

        if not self.exists(key):
            db[self.name].append({"key": key, "data": data});
            with open(self.path, "w") as f: f.write(json.dumps(db));
        else:
            db[self.name][self.__ga__(key)["index"]]["data"] = data;
            with open(self.path, "w") as f: f.write(json.dumps(db));

    def add(self, key: str, data: float or int) -> float or int:
        """
        Adds amount to given key in database.

        qik.add(\"number_value\", 2) -> 4
        """

        db = self.all();

        if not self.exists(key):
            err = "\u001b[31mCannot add a value to a non existing key.\u001b[37m";
            raise RuntimeError(err) from None;
        else:
            if isinstance(data, int) or isinstance(data, float):
                if isinstance(self.__ga__(key)["data"], int) or isinstance(self.__ga__(key)["data"], float):
                    db[self.name][self.__ga__(key)["index"]]["data"] += data;
                    with open(self.path, "w") as f: f.write(json.dumps(db));

                    return db[self.name][self.__ga__(key)["index"]]["data"];
                else:
                    err = f"\u001b[31mExpected data type \"float\" or \"int\", got {type(self.__ga__(data))}.\u001b[37m";
                    raise TypeError(err) from None;
            else:
                err = f"\u001b[31mExpected type \"float\" or \"int\", got {type(self.__ga__(data))}.\u001b[37m";
                raise TypeError(err) from None;

    def subtract(self, key: str, data: float or int) -> float or int:
        """
        Subtracts amount from given key in database.

        qik.subtract(\"number_value\", 2) -> 0
        """
        self.add(key, -data);
     
    def delete(self, key: str) -> bool:
        """
        Deletes a key from the database.

        qik.delete(\"example\") -> True
        """
        db = self.all();

        if self.exists(key) and not key == "all":
            db[self.name].pop(self.__ga__(key)["index"]);
            with open(self.path, "w") as f: f.write(json.dumps(db));
            return True;
        elif key == "all":
            db[self.name] = [];
            with open(self.path, "w") as f: f.write(json.dumps(db));
            return True;
        else:
            err = "\u001b[31mCannot delete non-existent key.\u001b[37m";
            raise RuntimeError(err) from None;
    
    def unlink(self, key):
        """
        Deletes file entirely from database.

        qik.unlink() -> True
        """

        try:
            if "directory" in self:
                os.remove(self.path);
                os.removedirs(self.directory);
                return True;
            else:
                os.remove(self.path);
                return True;
        except Exception as err:
            raise err;
    # STANDARD KEY STORAGE ENDS #

    # TABLE STORAGE STARTS #
    def tables(self):
        """
        Returns all tables in database.
        """

        db = self.all();
        l = [];

        for item in db[self.name]:
            if "arr" in item and not "data" in item:
                l.append(item);
            else:
                continue;
        return l;
    
    def hasTable(self, key: str):
        if not self.__gt__(key) == None:
            return True;
        else:
            return False;
    # TABLE STORAGE ENDS #

class Table:
    def __init__(self, database: DB, table_name: str):
        """
        exampleTable = Table(exampleDB, \"exampleTable\");

        Argument 1 - Database object.
        Argument 2 - Table name.
        """

        self.name = table_name;
        self.path = database.path;
        self.DB = database;
        db = database.all();

        if not self.DB.hasTable(self.name):
            db[self.DB.name].append({"key": self.name, "arr": []});

            with open(self.path, "w") as f: f.write(json.dumps(db));
        else:
            pass;

    def __repr__(self):
        return "Database Table Object";

    def contents(self) -> list:
        """
        Returns tables contents.

        ["Hello", "World!"]
        exampleTable.contents() -> ["Hello", "World!"]
        """

        return self.DB.__gt__(self.name)["arr"];
    
    def append(self, data) -> list:
        """
        Appends an element to the table.

        []
        exampleTable.append("Hello, World!") -> ["Hello, World!"]
        """

        db = self.DB.all();
        db[self.DB.name][self.DB.__gt__(self.name)["index"]]["arr"].append(data);

        with open(self.path, "w") as f: f.write(json.dumps(db));

        return db;

    def pop(self) -> list:
        pass;
    
    def index(self, value) -> int:
        """
        Finds index of given value in the table.

        ["Example", "Table", "Hello, World!"]
        exampleTable.index("Hello, World!") -> 2
        """
        for item in self.DB.__gt__(self.name)["arr"]:
            if item is value:
                return self.DB.__gt__(self.name)["arr"].index(item);
        return None;

    def insert(self, data, index: int) -> list:
        """
        Inserts an element at a given index in the Table

        ["Hello", "World"]
        exampleTable.insert("$", 1) -> ["Hello", "$", "World"]
        """
        if 0 <= index < len(self.contents()):
            table = self.contents();

            table.insert(index, data);

            db = self.DB.all();

            db[self.DB.name][self.DB.__gt__(self.name)["index"]]["arr"] = table;

            with open(self.path, "w") as f: f.write(json.dumps(db));

            return table;
        else:
            err = "Invalid index provided, cannot insert element at out of range index.";

            raise IndexError(err) from None;
    
    def replace(self, data, index: int) -> list:
        """
        Replaces content at a given index in the Table

        ["Hello", "World"]
        exampleTable.replace("Apple", 0) -> ["Apple", "World"]
        """

        if 0 <= index < len(self.contents()):
            db = self.DB.all();

            db[self.DB.name][self.DB.__gt__(self.name)["index"]]["arr"][index] = data;

            with open(self.path, "w") as f: f.write(json.dumps(db));


            return db;
    
    def clear(self) -> bool:
        """
        Clears all table values.

        exampleTable.clear() -> True
        """

        db = self.DB.all();
        db[self.DB.name][self.DB.__gt__(self.name)["index"]]["arr"] = [];

        with open(self.path, "w") as f: f.write(json.dumps(db));

        return True;
    
    def contains(self, data) -> bool:
        """
        Checks if table contains a given value.

        ["Hello", "World"]
        exampleTable.contains("Orange") -> False
        """

        if data in self.DB.all()[self.DB.name][self.DB.__gt__(self.name)["index"]]["arr"]:
            return True;
        else:
            return False;
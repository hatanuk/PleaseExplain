import sqlite3 as sql
from sqlite3 import connect

DB_PATH = "./database/database.db"
MAX_TERMS = 108

con = connect(DB_PATH, check_same_thread=False)
cur = con.cursor()


# - PUBLIC -

def fetch_all_terms(guild_id):
    """Returns: [TermName, TermDefinition, CreatorID, CreatedAt, UpdatedAt, TermImage]"""

    return _fetch(["TermName", "TermDefinition", "CreatorID", "CreatedAt", "UpdatedAt", "TermImage"], "TermDB", guild_id)


def fetch_term(guild_id, term):
    """Returns: TermName, TermDefinition, CreatorID, CreatedAt, UpdatedAt, TermImage"""

    result = _fetch(["TermName", "TermDefinition", "CreatorID", "CreatedAt", "UpdatedAt", "TermImage"], "TermDB",
                    guild_id, term)
    if not result:
        return None
    else:
        return result[0]
    

def fetch_term_count(term: str, guildid: str):
    return _one_record("SELECT COUNT(*) FROM TermDB WHERE TermNameLower = (?) AND GuildID = (?)", term.lower(), guildid)[0]

    
def insert_definition(term: str, definition: str, userid: int, guildid: int, time: str, image=None):
    # Check TOTAL count of server terms
    term_count = _one_record("SELECT COUNT(*) FROM TermDB WHERE GuildID = (?)", guildid)
    if len(term_count) > 0 and term_count[0] > MAX_TERMS:
        return "full"

    # Check if there exists an equivalent term in the database
    already_exists = _one_record("SELECT COUNT(*) FROM TermDB WHERE GuildID = (?) AND TermNameLower = (?)", guildid, term.lower()) > 0

    if already_exists:
        return "already_exists"

    if not image:
        _insert(["GuildID", "TermName", "TermNameLower", "TermDefinition", "CreatorID", "CreatedAt", "UpdatedAt"],
               [guildid, term, term.lower(), definition, userid, time, time], "TermDB")
    else:
        _insert(["GuildID", "TermName", "TermNameLower", "TermDefinition", "CreatorID", "CreatedAt", "UpdatedAt", "TermImage"],
               [guildid, term, term.lower(), definition, userid, time, time, image], "TermDB")
    return "successful"


def remove_term(term: str, guildid:str):
    try:
        _execute("DELETE FROM TermDB WHERE TermNameLower = (?) AND GuildID = (?)", term.lower(), guildid)
        return True
    except:
        return False


# - PRIVATE - 

def _with_commit(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        _commit()

    return wrapper


def _print_db(db):
    cur.execute("SELECT * FROM [%s]" % db)
    print(cur.fetchall())


def _commit():
    con.commit()


def _close():
    con.close()


def _one_record(command, *values):
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def _records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()


def _column(command, *values):
    cur.execute(command, tuple(values))

    columns = []
    for item in cur.fetchall():
        columns.append(item[0])

    print(columns)
    return columns


@_with_commit
def _execute(command, *values):
    cur.execute(command, tuple(values))


def _multiexec(command, valueset):
    cur.executemany(command, valueset)


def _scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())


def format_columns(columns) -> str:
    f_columns = ""
    v_columns = ""

    i = 0
    for column in columns:
        i += 1
        f_columns = f_columns + column + ", " if i < len(columns) else f_columns + column
        v_columns = v_columns + "?, " if i < len(columns) else v_columns + "?"
    return f_columns, v_columns


@_with_commit
def _insert(columns: list, values: list, database: str):
    if len(columns) != len(values):
        raise Exception("Amount of columns must match amount of values!")

    f_columns, v_columns = format_columns(columns)
    _execute("INSERT INTO %s(%s) VALUES (%s)" % (database, f_columns, v_columns), *values)



def format_values(values: list):
    f_values = ""

    i = 0
    for value in values:
        i += 1
        f_values = f_values + value + ", " if i < len(values) else f_values + value

    return f_values


def _fetch(values: list, database: str, guildid, termname=None, limit=9999):
    if len(values) == 0:
        values = "*"
    else:
        values = format_values(values)

    if termname is not None:
        fetched = _records("SELECT %s FROM %s WHERE GuildID = (?) AND TermNameLower = (?) ORDER BY TermNameLower LIMIT %s" % (values, database, limit), guildid, termname.lower())
        if len(fetched) < 1:
            return None
        else:
            return fetched
    else:
        fetched = _records("SELECT %s FROM %s WHERE GuildID = (?) ORDER BY TermNameLower LIMIT %s" % (values, database, limit), guildid)
        if len(fetched) < 1:
            return None
        else:
            return fetched


@_with_commit
def build(guild_ids):
    _execute(
        """CREATE TABLE IF NOT EXISTS {}(
    GuildID integer,
    GuildName text
    
    );""".format("DiscordServers"))

    # Message DB for each guild
    _execute("""CREATE TABLE IF NOT EXISTS {}(
    TermID integer PRIMARY KEY AUTOINCREMENT,
    GuildID integer,
    TermName text,
    TermNameLower text,
    TermDefinition text,
    CreatorID integer,
    CreatedAt text,
    UpdatedAt text,
    TermImage blob
    
    );""".format("TermDB"))

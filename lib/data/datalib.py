import sqlite3 as sql
from sqlite3 import connect

DB_PATH = "./database/database.db"
MAX_TERMS = 108

con = connect(DB_PATH, check_same_thread=False)
cur = con.cursor()


# - PUBLIC -

def fetch_config(guild_id):
    return _records("SELECT Value, TypeID FROM ConfigDB WHERE GuildId = ?", guild_id)


def set_monitoring(guild_id, on: bool):
    value = 1 if on else 0
    _update_config(guild_id, "1", value)

def is_monitoring_on(guild_id):
    monitoring_on = _one_record("SELECT Value FROM ConfigDB WHERE GuildID = (?) AND TypeId = (?)", guild_id, 1) 

    return True if monitoring_on == 1 else False

def set_usage_count(guild_id, term, usage_count):
    if usage_count:
        _execute(f"UPDATE TermDB SET UsageCount = ? WHERE GuildId = ? AND TermName = ?", usage_count, guild_id, term)


def increment_usage_count(guild_id, term):
    usage_count = fetch_usage_count(guild_id, term)
    if usage_count:
       set_usage_count(guild_id, term, usage_count + 1)

def fetch_usage_count(guild_id, term):
    result = _fetch(["UsageCount"], "TermDB", guild_id)

    if not result or result[0] == None:
        return None
    else:
        return result[0]

def fetch_all_terms(guild_id):
    """Returns: [TermName, TermDefinition, CreatorID, CreatedAt, UpdatedAt, TermImage, UsageCount]"""

    return _fetch(["TermName", "TermDefinition", "CreatorID", "CreatedAt", "UpdatedAt", "TermImage", "UsageCount"], "TermDB", guild_id)


def fetch_term(guild_id, term):
    """Returns: TermName, TermDefinition, CreatorID, CreatedAt, UpdatedAt, TermImage, UsageCount"""

    result = _fetch(["TermName", "TermDefinition", "CreatorID", "CreatedAt", "UpdatedAt", "TermImage", "UsageCount"], "TermDB",
                    guild_id, term)
    if not result:
        return None
    else:
        return result[0]
    

def fetch_term_count(term: str, guildid: str):
    return _one_record("SELECT COUNT(*) FROM TermDB WHERE TermNameLower = (?) AND GuildID = (?)", term.lower(), guildid)

    
def insert_definition(term: str, definition: str, userid: int, guildid: int, time: str, image=None):
    # Check TOTAL count of server terms
    term_count = _one_record("SELECT COUNT(*) FROM TermDB WHERE GuildID = (?)", guildid)
    if term_count > 0 and term_count > MAX_TERMS:
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


def clear_usage_data(guild_id):
    _execute("UPDATE TermDB SET UsageCount = NULL WHERE GuildID = ?", guild_id)
    set_monitoring(guild_id, on=False)


def clear_dictionary_data(guild_id):
    _execute("DELETE FROM TermDB WHERE GuildID = ?", guild_id)

def clear_config_data(guild_id):
    _execute("DELETE FROM ConfigDB WHERE GuildID = ?", guild_id)


def clear_all_data(guild_id):
    clear_dictionary_data(guild_id)


# - PRIVATE - 

def _update_config(guild_id, category, value):
    exists = _one_record("SELECT 1 FROM ConfigDB WHERE GuildId = ? AND TypeId = ?", guild_id, category)
    if exists:
        _execute(f"UPDATE ConfigDB SET Value = ? WHERE GuildId = ? AND TypeId = ?", value, guild_id, category)
    else:
        _execute(f"INSERT INTO ConfigDB (GuildId, TypeId, Value) VALUES (?, ?, ?)", guild_id, category, value)




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

    _execute("""CREATE TABLE IF NOT EXISTS {}(
    TermID integer PRIMARY KEY AUTOINCREMENT,
    GuildID integer,
    TermName text,
    TermNameLower text,
    TermDefinition text,
    CreatorID integer,
    CreatedAt text,
    UpdatedAt text,
    TermImage blob,
    UsageCount integer
    );""".format("TermDB"))


    # TYPE IDS:
    # 1 - MonitoringOn (Value: 0 or 1)
    _execute("""CREATE TABLE IF NOT EXISTS {}(
    GuildID integer,
    TypeID integer,
    Value integer
    );""".format("ConfigDB"))


def _insert_default_config(guild_id):

    # Monitoring ON by default
    _update_config(
        guild_id, "1", 1
    )


def on_guild_join(guild_id):
    _insert_default_config(guild_id)

def on_guild_remove(guild_id):
    clear_all_data(guild_id)
    clear_config_data(guild_id)
import os
import sys
import logging
import yaml
import sqlite3


# Check badger database root
BADGER_DB_ROOT = os.getenv('BADGER_DB_ROOT')
if BADGER_DB_ROOT is None:
    logging.error('Please set the BADGER_DB_ROOT env var!')
    sys.exit()
elif not os.path.exists(BADGER_DB_ROOT):
    os.makedirs(BADGER_DB_ROOT)
    logging.info(
        f'Badger database root {BADGER_DB_ROOT} created')


def save_routine(routine):
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')

    # Initialize
    if not os.path.exists(db_routine):
        con = sqlite3.connect(db_routine)
        cur = con.cursor()
        cur.execute('create table routine (name not null primary key, config)')
    else:
        con = sqlite3.connect(db_routine)
        cur = con.cursor()

    # Insert a record
    cur.execute('insert into routine values (?, ?)',
                (routine['name'], yaml.dump(routine, sort_keys=False)))
    con.commit()
    con.close()


def load_routine(name):
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')
    con = sqlite3.connect(db_routine)
    cur = con.cursor()

    cur.execute('select * from routine where name=:name', {'name': name})
    records = cur.fetchall()
    con.close()

    if len(records) == 1:
        return yaml.safe_load(records[0][1])
    elif len(records) == 0:
        logging.warn(f'Routine {name} not found in the database!')
        return None
    else:
        raise Exception(
            f'Multiple routines with name {name} found in the database!')


def list_routines():
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')
    con = sqlite3.connect(db_routine)
    cur = con.cursor()

    cur.execute('select name from routine')
    names = [record[0] for record in cur.fetchall()]
    con.close()

    return names


def save_run(run):
    pass


def load_run(name):
    pass

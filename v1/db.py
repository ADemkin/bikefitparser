from os import remove
from os.path import exists
from sqlite3 import Connection


class Database:
    def __init__(self, dbname):
        self.dbname = dbname

    def create(self):
        """Creates a db with all required fields
        """
        if exists(self.dbname):
            raise ValueError('Database {} already exist'.format(self.dbname))
        connect = Connection(self.dbname)
        cursor = connect.cursor()
        cursor.execute(
        """
        CREATE TABLE data (
            id integer primary key asc,
            inseam integer,
            trunk integer,
            forearm integer,
            arm integer,
            thigh integer,
            lower_leg integer,
            sternal_notch integer,
            height integer,
            top_tube_min real,
            top_tube_max real,
            seat_tube_cc_min real,
            seat_tube_cc_max real,
            seat_tube_ct_min real,
            seat_tube_ct_max real,
            stem_min real,
            stem_max real,
            bb_saddle_min real,
            bb_saddle_max real,
            saddle_handlebar_min real,
            saddle_handlebar_max real,
            saddle_setback_min real,
            saddle_setback_max real,
            seatpost_setback integer,
            status text
        )
        """
        )
        connect.commit()
        connect.close()

    def insert_parsed_data(self, parsed_data, primary_key):
        """Insert parsed data into row with given promary key
        """
        connect = Connection(self.dbname)
        cursor = connect.cursor()
        cursor.execute(
        """
        UPDATE
            data
        SET
            top_tube_min = :top_tube_min,
            top_tube_max = :top_tube_max,
            seat_tube_cc_min = :seat_tube_cc_min,
            seat_tube_cc_max = :seat_tube_cc_max,
            seat_tube_ct_min = :seat_tube_ct_min,
            seat_tube_ct_max = :seat_tube_ct_max,
            stem_min = :stem_min,
            stem_max = :stem_max,
            bb_saddle_min = :bb_saddle_min,
            bb_saddle_max = :bb_saddle_max,
            saddle_handlebar_min = :saddle_handlebar_min,
            saddle_handlebar_max = :saddle_handlebar_max,
            saddle_setback_min = :saddle_setback_min,
            saddle_setback_max = :saddle_setback_max,
            seatpost_setback = :seatpost_setback,
            status = :status
        WHERE
            id = :id
        """,
            {
                'top_tube_min': parsed_data['Top Tube'][0],
                'top_tube_max': parsed_data['Top Tube'][1],
                'seat_tube_cc_min': parsed_data['Seat Tube Range CC'][0],
                'seat_tube_cc_max': parsed_data['Seat Tube Range CC'][1],
                'seat_tube_ct_min': parsed_data['Seat Tube Range CT'][0],
                'seat_tube_ct_max': parsed_data['Seat Tube Range CT'][1],
                'stem_min': parsed_data['Stem Length'][0],
                'stem_max': parsed_data['Stem Length'][1],
                'bb_saddle_min': parsed_data['BB Saddle Position'][0],
                'bb_saddle_max': parsed_data['BB Saddle Position'][1],
                'saddle_handlebar_min': parsed_data['Saddle Handlebar'][0],
                'saddle_handlebar_max': parsed_data['Saddle Handlebar'][1],
                'saddle_setback_min': parsed_data['Saddle Setback'][0],
                'saddle_setback_max': parsed_data['Saddle Setback'][1],
                'seatpost_setback': 1 if parsed_data['Saddle Setback'] else 0,
                'status': 'processed',
                'id': primary_key,
            }
        )
        connect.commit()
        connect.close()

    def insert_input_data(self, inseam, trunk, forearm, arm, thigh, leg, notch, height):
        """Insert data into a table
        """
        connect = Connection(self.dbname)
        cursor = connect.cursor()
        cursor.execute(
        """
        INSERT INTO data
            (
                inseam,
                trunk,
                forearm,
                arm,
                thigh,
                lower_leg,
                sternal_notch,
                height,
                status
            )
        VALUES
            (
                :inseam,
                :trunk,
                :forearm,
                :arm,
                :thigh,
                :leg,
                :notch,
                :height,
                :status
            )
        """,
            {
                'inseam': inseam,
                'trunk': trunk,
                'forearm': forearm,
                'arm': arm,
                'thigh': thigh,
                'leg': leg,
                'notch': notch,
                'height': height,
                'status': 'unprocessed',
            }
        )
        connect.commit()
        connect.close()

    def fetch_unprocessed(self):
        """Returns one unprocessed row in a tuple(id, a, b, c, d, e, f, g, h)
        and set its status to 'processing'
        """
        connect = Connection(self.dbname)
        cursor = connect.cursor()
        cursor.execute(
        """
        SELECT
            *
        FROM
            'data'
        WHERE
            status = 'unprocessed'
            LIMIT 1
        """
        )
        unprocessed_row = cursor.fetchone()
        if unprocessed_row:
            cursor.execute(
            """
            UPDATE
                data
            SET
                status = 'processing'
            WHERE
                id = :id
            """,
                {'id': unprocessed_row[0]},
            )
        connect.commit()
        connect.close()
        if unprocessed_row:
            return unprocessed_row[:9]

    def get_unprocessed_count(self):
        """Return number of unprocessed rows
        """
        connect = Connection(self.dbname)
        cursor = connect.cursor()
        cursor.execute(
        """
        SELECT
            count(*)
        FROM
            "data"
        WHERE
            status = "unprocessed"
        """
        )
        unprocessed = cursor.fetchone()
        connect.commit()
        connect.close()
        return unprocessed[0]

    def heal(self):
        """Change status from processing to unprocess for all rows in case of
        failed attempt
        """
        connect = Connection(self.dbname)
        cursor = connect.cursor()
        cursor.execute(
        """
        UPDATE
            "data"
        SET
            status = "unprocessed"
        WHERE
            status = "processing"
        """
        )
        connect.commit()
        connect.close()

def test_db():
    dbname = 'test.db(DELETE_ME)'
    table_size = 300
    parsed_data_example = {
        'Top Tube': ('52.3', '52.7'),
        'Seat Tube Range CC': ('58.3', '58.8'),
        'Seat Tube Range CT': ('60.1', '60.6'),
        'Stem Length': ('10.8', '11.4'),
        'BB Saddle Position': ('79.7', '81.7'),
        'Saddle Handlebar': ('51.5', '52.1'),
        'Saddle Setback': ('7.2', '7.6'),
        'Setback Seatpost': False,
    }
    db = Database(dbname)
    if exists(dbname):
        remove(dbname)
        db.create()
    print('All folowing should be True:')
    for i in range(table_size):
        db.insert_input_data(i*0, i*1, i*2, i*3, i*4, i*5, i*6, i*7)
    for i in range(table_size):
        row = db.fetch_unprocessed()
        print(row[0], end=':')
        print(
            all((
                (len(row) == 9),
                (row[1] == 0),
                (row[2] == i),
                (row[3] == i*2),
                (row[4] == i*3),
                (row[5] == i*4),
                (row[6] == i*5),
                (row[8] == i*7),
            )),
            end=',',
        )
        db.insert_parsed_data(parsed_data_example, row[0])
        print(db.get_unprocessed_count() == (table_size-i-1))
    if db.get_unprocessed_count() == 0:
        print('SUCCESS!')
    remove(dbname)

if __name__ == '__main__':
    test_db()

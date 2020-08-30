from django.db import connection
from datetime import datetime
from named_storms.models import NsemPsaVariable


def wind_barbs_query(psa_id: int, date: datetime, step=100):
    with connection.cursor() as cursor:
        sql = '''
            SELECT
               ST_AsText(d1.point),
               d1.value as direction,
               d2.value as speed
            from named_storms_nsempsadata d1
                INNER JOIN named_storms_nsempsavariable v1 ON (
                    v1.nsem_id = %(psa_id)s AND
                    v1.name = %(wind_direction)s AND
                    d1.date = %(date)s AND
                    d1.nsem_psa_variable_id = v1.id
                )
                INNER JOIN named_storms_nsempsadata d2 on (
                        d1.point = d2.point AND
                        d2.date = %(date)s AND
                        d1.id != d2.id
                )
                INNER JOIN named_storms_nsempsavariable v2 ON (
                    d2.nsem_psa_variable_id = v2.id AND
                    v2.name = %(wind_speed)s
                )
                INNER JOIN named_storms_nsempsa nsn on nsn.id = v1.nsem_id
                INNER JOIN named_storms_namedstorm n on n.id = nsn.named_storm_id
            WHERE
                  ST_Within(d1.point::geometry, n.geo::geometry) AND
                  d1.id %% %(step)s = 0
        '''

        cursor.execute(sql, {
            'psa_id': psa_id,
            'date': date,
            'wind_direction': NsemPsaVariable.VARIABLE_DATASET_WIND_DIRECTION,
            'wind_speed': NsemPsaVariable.VARIABLE_DATASET_WIND_SPEED,
            'step': step,
        })
        return cursor.fetchall()

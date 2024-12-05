from typing import Any
from pydantic.types import Json

class DMLCoreOperations():
    def dml_core_insert(selfinsert_in:Any):
        dt_src = Json([
            {
                'ot' : 'I',
                'tbl_name' : 'fn_unbjy_customers',
                'data' : [{
                    'comments': "comments",
                    'email_id': "a@a.com",
                    'mobile_no': "234234",
                    'name': "nam",
                }]
            }, {
                'ot' : 'I',
                'tbl_name' : 'fn_unbjy_customers',
                'data' : [{
                    'comments': "comments",
                    'email_id': "a@a.com",
                    'mobile_no': "234234",
                    'name': "nam",
                }]
            }
        ])

        for row in dt_src:
            print(row['tbl_name'])


    

class Query():
    @classmethod
    def insertDataTblEmployeed(self,data):
        QUERY="""INSERT INTO tbl_employees (FIRST_NAME,LAST_NAME,FEET,COMMISION,ID_T)
            VALUES ('{0}','{1}',{2} ,{3},{4})""".format(
                data['FIRSTNAME'],
                data['LASTNAME'],
                data['FEET'],
                data['COMMISION'],
                data['IDT'])
        return QUERY
    
    @classmethod
    def deleteDataTblEmployeed(self,data):
        QUERY="""DELETE FROM tbl_employees
            WHERE FIRST_NAME='{0}'
            AND LAST_NAME='{1}'""".format(
                data['FIRSTNAME'],
                data['LASTNAME']
            )
        return QUERY
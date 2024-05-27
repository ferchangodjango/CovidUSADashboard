from Models.Entities.Users import User

class ModelUser():

    @classmethod
    def loggedUser(self,db,user):
        try:
            cursor=db.connection.cursor()
            QUERY=""" SELECT IDADMINISTRATOR,USERADMINISTRATOR,PASSWORDADMINISTRATOR
                FROM tbl_administrator
                WHERE USERADMINISTRATOR='{}'""".format(user.user)
            cursor.execute(QUERY)
            answer=cursor.fetchone()
            if answer!=None:
                loggedUser=User(answer[0],answer[1],User.checkPassword(answer[2],user.password))
                return loggedUser
            else:
                return None
        
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def idUser(self,db,ID):
        try:
            cursor=db.connection.cursor()
            QUERY=""" SELECT IDADMINISTRATOR,USERADMINISTRATOR
                FROM tbl_administrator
                WHERE IDADMINISTRATOR={}""".format(ID)
            cursor.execute(QUERY)
            answer=cursor.fetchone()
            if answer!=None:
                loggedUser=User(answer[0],answer[1],None)
                return loggedUser
            else:
                return None
        
        except Exception as ex:
            raise Exception(ex)


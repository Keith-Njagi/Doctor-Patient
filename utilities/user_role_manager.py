class UserPrivilege:
    user_id = ''
    role = 0
    privileges =''
    all_privileges = {1:'Doctor', 2:'User'}

    @classmethod
    def generate_user_role(cls, user_id:int):
        if user_id == 1 or user_id == 2:
            cls.user_id = user_id
            cls.role = 1
            cls.privileges = cls.all_privileges[cls.role]
        else:
            cls.user_id = user_id
            cls.role = 2
            cls.privileges = cls.all_privileges[cls.role]

    @classmethod
    def get_privileges(cls, user_id:int, role:int):
        cls.user_id = user_id
        cls.role = role
        cls.privileges = cls.all_privileges[cls.role]

    @classmethod
    def update_user_role(cls, user_id:int, role:int):
        try:
            cls.user_id = user_id
            cls.role = role
            cls.privileges = cls.all_privileges[cls.role]
        except:
            cls.user_id = user_id
            cls.role = 2
            cls.privileges = cls.all_privileges[cls.role]

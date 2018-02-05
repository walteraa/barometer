class Target:

    def __init__(self, host, machine_id, description=''):
        if host == None or host.strip() == '':
            raise ValueError('Host shouldn\'t be empty')
        if machine_id == None or machine_id < 0:
            raise ValueError('Invalid machine_id')

        self.host = host
        self.machine_id = machine_id
        self.description = description if description != None and description.strip() != '' else self.host

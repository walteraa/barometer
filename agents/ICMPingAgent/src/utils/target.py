class Target:

    def __init__(self, host, machine_id, description=''):
        if host is None or host.strip() == '':
            raise ValueError('Host shouldn\'t be empty')
        if machine_id is None or machine_id < 0:
            raise ValueError('Invalid machine_id')

        self.host = host
        self.machine_id = machine_id
        if description is not None and description.strip() != '':
            self.description = description
        else:
            self.description = self.host

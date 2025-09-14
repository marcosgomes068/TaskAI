class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def run_task(self, task):
        pass

    def save_result(self, result, filename):
        pass

def run_agent(name, role, task, save=None):
    agent = Agent(name, role)
    result = agent.run_task(task)
    if save:
        agent.save_result(result, save)
    return result
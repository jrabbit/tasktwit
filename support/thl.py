import TheHitList


def add_task(task):
    # local thl usage
    thl = TheHitList.Application()
    thl_task = TheHitList.Task()
    thl_task.title = task
    thl.inbox().add_task(thl_task)

def get_tasks():
    """returns list of THL tasks for *today*"""
    thl = TheHitList.Application()
    return [x.title for x in thl.today().tasks() if not x.completed and not x.canceled]


def finish_task(task):
    pass

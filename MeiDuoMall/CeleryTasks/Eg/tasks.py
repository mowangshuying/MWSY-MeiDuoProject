from CeleryTasks.main import celeryApp

@celeryApp.task(name='print_eg')
def print_eg():
    print("print_eg")
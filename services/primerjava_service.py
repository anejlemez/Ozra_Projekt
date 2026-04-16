from repositories.primerjava_repository import *

def primerjava_service(t1, t2):
    return {
        "tekmovalec1": get_stats_repo(t1),
        "tekmovalec2": get_stats_repo(t2)
    }
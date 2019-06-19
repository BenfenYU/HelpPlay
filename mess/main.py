import threading
import get_disney_date.fetch as fetch
import decide.go_where as go_where
from threading import Timer

if __name__ == "__main__":
    #lock = threading.Lock()
    #get_waitTime = threading.Thread(target=fetch.main,args=(lock,))
    #get_waitTime.start()
    go_where = Timer(5,go_where.main)
    go_where.start()


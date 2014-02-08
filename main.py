from myshows import login
from myshows import myshows

def main():
    myShows_login = login.MyShowsLogin("demo", "demo")
    myShows = myshows.MyShows(myShows_login)
    print myShows.profile()
    print myShows.shows()

if __name__ == "__main__":
    main()

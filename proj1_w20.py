#########################################
##### Name: Xin Hu                  #####
##### Uniqname: hsinhu              #####
#########################################
import requests
import webbrowser

class Media:
    '''A media's information container

    Attributes
    ----------
    title: string
        The media's title
    author: string
        The media's author
    release_year: string
        the media's release year
    url: string
        the median's link
    json: dictionary
        media information in json form
    '''

    def __init__(self, title="No Title", author="No Author",\
                    release_year="No Release Year", url="No URL", json=None):
        if json is None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            if "trackName" in json:
                self.title = json["trackName"]
            else:
                self.title = json["collectionName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"][:4]
            if "trackViewUrl" in json:
                self.url = json["trackViewUrl"]
            else:
                self.url = json["collectionViewUrl"]

    def info(self):
        '''Return media's basic information.

        Parameters
        ----------
        none

        Returns
        -------
        string
            contain media's title, author and release year
        '''

        return self.title + " by " + self.author + \
            " (" + str(self.release_year) +")"

    def length(self):
        '''Return media's length.

        Parameters
        ----------
        none

        Returns
        -------
        int
            media's length, default 0.
        '''

        return 0


# Other classes, functions, etc. should go here
class Song(Media):
    '''A song's information container

    Attributes
    ----------
    title: string
        The song's title
    author: string
        The song's author
    release_year: string
        the song's release year
    url: string
        the song's link
    album: string
        the song's album
    genre: string
        the song's genre
    track_length: int
        song's length in millisecond.
    json: dictionary
        song information in json form
    '''

    def __init__(self, title="No Title", author="No Author",\
                    release_year="No Release Year", url="No URL",\
                    album="No Album", genre="No Genre",\
                    track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is None:
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = json["trackTimeMillis"]

    def info(self):
        '''Return song's basic information.

        Parameters
        ----------
        none

        Returns
        -------
        string
            contain song's title, author, release year and genre
        '''

        return super().info() + " [" + self.genre + "]"

    def length(self):
        '''Return song's length.

        Parameters
        ----------
        none

        Returns
        -------
        int
            song's length in seconds (rounded to nearest second).
        '''

        return round(self.track_length/1000.0)


class Movie(Media):
    '''A movie's information container

    Attributes
    ----------
    title: string
        The movie's title
    author: string
        The movie's author
    release_year: string
        the movie's release year
    url: string
        the movie's link
    rating: string
        the movie's rating
    movie_length: int
        movie's length in millisecond.
    json: dictionary
        movie information in json form
    '''

    def __init__(self, title="No Title", author="No Author",\
                release_year="No Release Year", url="No URL",\
                rating="No Rating", movie_length = 0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is None:
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = json["trackTimeMillis"]

    def info(self):
        '''Return movie's basic information.

        Parameters
        ----------
        none

        Returns
        -------
        string
            contain movie's title, author, release year and rating
        '''

        return super().info() + " [" + self.rating + "]"

    def length(self):
        '''Return movie's length.

        Parameters
        ----------
        none

        Returns
        -------
        int
            movie's length in minutes (rounded to nearest minute).
        '''

        return round(self.movie_length/60000.0)


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    print(("-1.0").isdigit())
    BASE_URL = "https://itunes.apple.com/search"
    user_input = None

    while True:
        if not user_input:
            promt_str = 'Enter a search term, or "exit" to quit: '
            user_input = input(promt_str)
        if user_input == "exit":
            print("Bye!")
            break
        else:
            params_dict = {'term':user_input}
            response = requests.get(BASE_URL, params_dict)
            results_object = response.json()
            results_list = results_object["results"]
            if not(results_list):
                promt_str1 = "There are no results for this term. "
                promt_str2 = "Please start another search term, or exit."
                print(promt_str1 + promt_str2)
                print()
                user_input = input(promt_str)
                continue
            print()
            songs_list = []
            movies_list = []
            other_media_list = []
            for single_result in results_list:
                if "kind" in single_result:
                    if single_result["kind"] == "song":
                        songs_list.append(Song(json=single_result))
                    elif single_result["kind"] == "feature-movie":
                        movies_list.append(Movie(json=single_result))
                else:
                    other_media_list.append(Media(json=single_result))
            index = 0
            if songs_list:
                print("SONGS")
                for song in songs_list:
                    index = index + 1
                    print(str(index) + " " + song.info())
                print()
            if movies_list:
                print("MOVIES")
                for movie in movies_list:
                    index = index + 1
                    print(str(index) + " " + movie.info())
                print()
            if other_media_list:
                print("OTHER MEDIA")
                for other_media in other_media_list:
                    index = index + 1
                    print(str(index) + " " + other_media.info())
                print()

            while True:
                promt_str3 = "Enter a number for more info, "
                promt_str4 = "or another search term, or exit: "
                user_choice = input(promt_str3 + promt_str4)
                if user_choice.isnumeric():
                    if int(user_choice) < 1 or int(user_choice) > index:
                        print("number is not valid. Please enter a " +
                                "number between 1 and " + str(index))
                        continue
                    elif int(user_choice) <= len(songs_list):
                        real_index = int(user_choice) - 1
                        select_url = songs_list[real_index].url
                    elif int(user_choice) <= len(songs_list)+len(movies_list):
                        real_index = int(user_choice) - 1 - len(songs_list)
                        select_url = movies_list[real_index].url
                    else:
                        real_index = int(user_choice) - 1 - len(songs_list) \
                                        - len(movies_list)
                        select_url = other_media_list[real_index].url
                    print("Launching")
                    print(select_url)
                    print("in web browser...")
                    print()
                    webbrowser.open(select_url)
                else:
                    user_input = user_choice
                    break
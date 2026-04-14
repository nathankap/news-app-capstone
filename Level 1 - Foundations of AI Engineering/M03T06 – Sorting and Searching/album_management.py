class Album:
    def __init__(self, album_name, number_of_songs, album_artist):
        self.album_name = album_name
        self.number_of_songs = int(number_of_songs)
        self.album_artist = album_artist

    def __str__(self):
        return (f"({self.album_name}, {self.album_artist}, "
                f"{self.number_of_songs})")


# initialize albums
album1 = Album("I LOVE DAWT", 6, "Nathan")
album2 = Album("Dawt Sin Sung", 7, "Kap")
album3 = Album("future wife", 4, "me")
album4 = Album("Ring Coming Soon", 11, "IDK")
album5 = Album("in love like at the beginning", 4, "nathan & dawt")
albums1 = [album1, album2, album3, album4, album5]
print("\n\nOriginal Album List:")
for index, album in enumerate(albums1):
    print(f"({index}) {album}")

# sort by number of songs
albums1.sort(key=lambda x: x.number_of_songs)
print("\n\nAlbums (sorted by number of songs): ")
for index, album in enumerate(albums1):
    print(f"({index} {album.album_name} - {album.number_of_songs} songs")

# swap index 0 and 1
albums1[0], albums1[1] = albums1[1], albums1[0]
print("\n\nAlbums (sorted & index 0,1 swapped):")
for index, album in enumerate(albums1):
    print(f"({index}) {album}")

# initialize albums2
album2_1 = Album("my gf", 23, "dawtsung")
album2_2 = Album("grandma needs cane", 3, "old woman gf")
album2_3 = Album("fiance when", 8, "soon")
album2_4 = Album("Excitement!", 10, "In Love")
album2_5 = Album("DuhDAWTnak", 5, "Me For Her")
albums2 = [album2_1, album2_2, album2_3, album2_4, album2_5]
print("\n\nSecond Album List:")
for index, album in enumerate(albums2):
    print(f"({index}) {album}")

# copy albums1 into albums2 and add more albums
album_extra_1 = Album("Dark Side of the Moon", 9, "Pink Floyd")
album_extra_2 = Album("Oops!... I Did It Again", 16, "Britney Spears")
for album in albums1:
    albums2.append(album)
albums2.append(album_extra_1)
albums2.append(album_extra_2)

# sort by album name
albums2.sort(key=lambda x: x.album_name.casefold())
print("\n\nThird Album List (sorted alphabetically)")
for index, album in enumerate(albums2):
    print(f"({index}) {album.album_name}")

# search for dark side
for index, album in enumerate(albums2):
    if album.album_name == "Dark Side of the Moon":
        dark_side_i = index
        break

print(f"\n\nIndex of Dark Side of the Moon: {dark_side_i}")

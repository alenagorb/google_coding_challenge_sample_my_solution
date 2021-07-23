"""A video player class."""

from src.video_library import VideoLibrary


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.isPlaying = 0
        self.isPaused = 0
        self.isFlagged = {}
        self.reason = {}
        self.current_video = []
        self.playlists = {}
        self.original_playlist_names = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        ids = sorted([video.video_id for video in all_videos])

        print("Here's a list of all available videos:")
        for video_id in ids:
            if self.isFlagged.get(video_id, 0) == 1:
                print(f'{self._video_library.get_video(video_id)} - FLAGGED '
                      f'(reason: {self.reason[video_id]})')
            else:
                print(self._video_library.get_video(video_id))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if self.isFlagged.get(video_id, 0) == 1:
            print(f'Cannot play video: Video is currently flagged (reason: {self.reason[video_id]})')
        else:
            try:
                current_title = self._video_library.get_video(video_id).title
                self.current_video.append(current_title)
                self.isPaused = 0

                if self.isPlaying == 0:
                    print('Playing video:', current_title)
                    self.isPlaying = 1
                else:
                    print('Stopping video:', self.current_video[-2])
                    print('Playing video:', current_title)

            except AttributeError:
                    print('Cannot play video: Video does not exist')

    def stop_video(self):
        """Stops the current video."""

        if self.isPlaying == 1:
            print('Stopping video:', self.current_video[-1])
            self.isPlaying = 0
        else:
            print('Cannot stop video: No video is currently playing')

    def play_random_video(self):
        """Plays a random video from the video library."""
        all_videos = self._video_library.get_all_videos()
        all_no_flag_videos = []

        for video in all_videos:
            if self.isFlagged.get(video.video_id, 0) == 0:
                all_no_flag_videos.append(video)

        num_videos = len(all_no_flag_videos)
        if num_videos == 0:
            print('No videos available')
        else:
            random_video = all_no_flag_videos[random.randrange(num_videos)].video_id
            self.play_video(random_video)

    def pause_video(self):
        """Pauses the current video."""

        if self.isPlaying == 0:
            print('Cannot pause video: No video is currently playing')
        elif self.isPaused == 0:
            print('Pausing video:', self.current_video[-1])
            self.isPaused = 1
        else:
            print('Video already paused:', self.current_video[-1])


    def continue_video(self):
        """Resumes playing the current video."""

        if self.isPlaying == 0:
            print('Cannot continue video: No video is currently playing')
        elif self.isPaused == 1:
            print('Continuing video:', self.current_video[-1])
        else:
            print('Cannot continue video: Video is not paused')


    def show_playing(self):
        """Displays video currently playing."""

        all_videos = self._video_library.get_all_videos()

        if self.isPlaying == 1:
            for video in all_videos:
                if video.title == self.current_video[-1] and self.isPaused == 1:
                    print('Currently playing:', video, '- PAUSED')
                elif video.title == self.current_video[-1] and self.isPaused == 0:
                    print('Currently playing:', video)
        else:
            print('No video is currently playing')


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        assert type(playlist_name) == str
        assert all([char not in string.whitespace for char in playlist_name])

        if playlist_name.lower() not in self.playlists.keys():
            self.playlists[playlist_name.lower()] = []
            self.original_playlist_names.append(playlist_name)
            print('Successfully created new playlist:', playlist_name)
        else:
            print('Cannot create playlist: A playlist with the same name already exists')

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if self.isFlagged.get(video_id, 0) == 1:
            print(f'Cannot add video to {playlist_name}: Video is currently flagged '
                  f'(reason: {self.reason[video_id]})')
            return

        try:
            if playlist_name.lower() not in self.playlists.keys():
                print(f'Cannot add video to {playlist_name}: Playlist does not exist')
            elif video_id in self.playlists[playlist_name.lower()]:
                print(f'Cannot add video to {playlist_name}: Video already added')
            else:
                video_to_add = self._video_library.get_video(video_id)
                self.playlists[playlist_name.lower()].append(video_id)
                print(f'Added video to {playlist_name}: {video_to_add.title}')
        except AttributeError:
            print(f'Cannot add video to {playlist_name}: Video does not exist')

    def show_all_playlists(self):
        """Display all playlists."""
        if not self.original_playlist_names:
            print('No playlists exist yet')
        else:
            print('Showing all playlists:')
            for name in sorted(self.original_playlist_names):
                print(name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlists.keys():
            print(f'Cannot show playlist {playlist_name}: Playlist does not exist')
        elif not self.playlists[playlist_name.lower()]:
            print('Showing playlist:', playlist_name)
            print('No videos here yet')
        else:
            print('Showing playlist:', playlist_name)
            for video_id in self.playlists[playlist_name.lower()]:
                if self.isFlagged.get(video_id, 0) == 1:
                    print(f'{self._video_library.get_video(video_id)} - FLAGGED '
                          f'(reason: {self.reason[video_id]})')
                else:
                    print(self._video_library.get_video(video_id))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        all_videos = self._video_library.get_all_videos()
        video_ids = [video.video_id for video in all_videos]

        if playlist_name.lower() not in self.playlists.keys():
            print(f'Cannot remove video from {playlist_name}: Playlist does not exist')
        elif video_id not in self.playlists[playlist_name.lower()] and video_id in video_ids:
            print(f'Cannot remove video from {playlist_name}: Video is not in playlist')
        elif video_id not in self.playlists[playlist_name.lower()] and video_id not in video_ids:
            print(f'Cannot remove video from {playlist_name}: Video does not exist')
        else:
            video_to_remove = self._video_library.get_video(video_id)
            self.playlists[playlist_name.lower()].remove(video_id)
            print(f'Removed video from {playlist_name}: {video_to_remove.title}')

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlists.keys():
            print(f'Cannot clear playlist {playlist_name}: Playlist does not exist')
        else:
            self.playlists[playlist_name.lower()] = []
            print('Successfully removed all videos from', playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            del self.playlists[playlist_name.lower()]
            print('Deleted playlist:', playlist_name)
        except KeyError:
            print(f'Cannot delete playlist {playlist_name}: Playlist does not exist')

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        video_ids = [video.video_id for video in all_videos]
        matched_videos = {}

        if all([search_term.lower() not in video_id for video_id in video_ids]):
            print(f'No search results for {search_term}')
            return
        else:
            print(f'Here are the results for {search_term}:')
            for video_id in sorted(video_ids):
                if search_term.lower() in video_id and self.isFlagged.get(video_id, 0) != 1:
                    print(f'{len(matched_videos) + 1}) {self._video_library.get_video(video_id)}')
                    matched_videos[len(matched_videos) + 1] = video_id

        print('Would you like to play any of the above? If yes, specify the number of the video.')
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            video_num = int(input())
            if video_num in matched_videos.keys():
                video_to_play = matched_videos[video_num]
                self.play_video(video_to_play)
        except ValueError:
            return

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        try:
            assert video_tag[0] == '#'
        except AssertionError:
            print(f'No search results for {video_tag}')
            return

        all_videos = self._video_library.get_all_videos()
        id_to_tag = {}

        for video in all_videos:
            tag = ''.join(video.tags)
            Id = video.video_id
            id_to_tag[Id] = tag

        matched_videos = {}

        if all([video_tag.lower() not in tag for tag in id_to_tag.values()]):
            print(f'No search results for {video_tag}')
            return
        else:
            print(f'Here are the results for {video_tag}:')
            for video_id, tag in id_to_tag.items():
                if video_tag.lower() in tag and self.isFlagged.get(video_id, 0) != 1:
                    print(f'{len(matched_videos) + 1}) {self._video_library.get_video(video_id)}')
                    matched_videos[len(matched_videos) + 1] = video_id

        print('Would you like to play any of the above? If yes, specify the number of the video.')
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            video_num = int(input())
            if video_num in matched_videos.keys():
                video_to_play = matched_videos[video_num]
                self.play_video(video_to_play)
        except ValueError:
            return

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        self.reason[video_id] = flag_reason

        all_videos = self._video_library.get_all_videos()
        video_ids = [video.video_id for video in all_videos]

        if video_id not in video_ids:
            print(f'Cannot flag video: Video does not exist')
        elif self.isFlagged.get(video_id, 0) == 1:
            print('Cannot flag video: Video is already flagged')
        else:
            self.isFlagged[video_id] = 1
            if self.isPlaying == 1 and self._video_library.get_video(video_id).title == self.current_video[-1]:
                self.stop_video()
            elif self.isPaused == 1 and self._video_library.get_video(video_id).title == self.current_video[-1]:
                self.pause_video()

            print(f'Successfully flagged video: {self._video_library.get_video(video_id).title} '
                  f'(reason: {flag_reason})')

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        all_videos = self._video_library.get_all_videos()
        video_ids = [video.video_id for video in all_videos]

        if video_id not in video_ids:
            print(f'Cannot remove flag from video: Video does not exist')
        elif self.isFlagged.get(video_id, 0) == 1:
            self.isFlagged[video_id] = 0
            print(f'Successfully removed flag from video: {self._video_library.get_video(video_id).title}')
        else:
            print(f'Cannot remove flag from video: Video is not flagged')

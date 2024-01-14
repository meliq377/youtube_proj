from django.shortcuts import render
from django.http import HttpResponse
from pytube import YouTube
from sendfile import sendfile
from yt_dlp import YoutubeDL  # Import yt_dlp

# Optionally, import for YouTube authentication
# from pytube import Playlist

def download_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        print("Video URL:", video_url)  # Debug statement

        try:
            try:  # Attempt authentication-based download with pytube
                yt = YouTube(video_url, on_progress_callback=progress_function, use_oauth=True, allow_oauth_cache=True)
                yt.set_credentials(client_id="YOUR_API_KEY", client_secret="YOUR_CLIENT_SECRET", refresh_token="YOUR_REFRESH_TOKEN")

                # Ensure file path is assigned correctly
                video = yt.streams.filter(progressive=True).first()
                file_path = video.download()  # Assign file path here
                print("File path after pytube download:", file_path)  # Debug statement

            except Exception as e:  # Fallback to yt-dlp if authentication fails
                ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 'verbose': True}  # Output template with verbose option
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    file_path = info_dict.get('filepath', None)
                    print("Info dict after yt-dlp download:", info_dict)  # Debug statement
                    print("File path after yt-dlp download:", file_path)  # Debug statement

            # Proceed with file serving if file path is valid
# Proceed with file serving if file path is valid
            if file_path:
                if 'entries' in info_dict:
                    file_path = info_dict['entries'][0]['url']
                print("File path:", file_path)
                response = sendfile(request, file_path, attachment=True, attachment_filename='downloaded_video.mp4')
                response['Content-Type'] = 'video/mp4'  # Or use info_dict['ext']
                return response
            else:
                print("Download failed: File path not found")
                raise Exception("Download failed: Unable to retrieve file path")


        except Exception as e:  # Fallback to yt-dlp if authentication fails
            ydl_opts = {'verbose': True}  # Include verbose option
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)  # Set download to False
                file_path = info_dict.get('filepath', None)
                print("Info dict from yt-dlp:", info_dict)  # Debug statement
                file_path = info_dict.get('filepath', None)  # Update file_path assignment
                print("File path after yt-dlp download:", file_path)  # Debug statement


    return render(request, 'download_form.html')

# Optional progress callback for pytube downloads
def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    # Calculate download progress percentage
    progress = (bytes_downloaded / total_size) * 100

    # Print progress information to the console
    print(f"Downloaded {bytes_downloaded} of {total_size} bytes ({progress:.2f}%)")

    # Optionally, implement other progress tracking mechanisms, such as:
    # - Updating progress bars in your web interface
    # - Sending progress notifications to the user

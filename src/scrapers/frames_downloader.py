from timeit import default_timer as timer
import os
import ray
import shutil
import cv2
import yt_dlp
import re
import unicodedata


def clean_title(title):
    # Replace special characters with underscores
    cleaned_title = re.sub(r'[^\w\s-]', '', title)
    cleaned_title = re.sub(r'[\s]+', '_', cleaned_title)
    # Remove accents from Latin characters
    cleaned_title = ''.join(c for c in unicodedata.normalize('NFD', cleaned_title) if unicodedata.category(c) != 'Mn')
    return cleaned_title


ray.init()  # Start Ray to enable parallel processing


@ray.remote
def process_video_parallel(url, total_frames, process_number, cleaned_title, frame_split=20):
    print(f"+++ Process {process_number} started for {cleaned_title}")
    cap = cv2.VideoCapture(url)
    num_processes = os.cpu_count()
    frames_per_process = int(total_frames) // num_processes
    cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * process_number)
    count = frames_per_process * process_number

    print(f"Total frames: {total_frames}, Frames per process: {frames_per_process}")

    while count < frames_per_process * (process_number + 1):
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_split == 0:  # Save only one frame every frame_split frames
            # Define the region of interest (ROI) coordinates
            roi_top_left = (0, 20)
            roi_bottom_right = (frame.shape[1], 140)
            # Extract the ROI from the frame
            roi = frame[roi_top_left[1]:roi_bottom_right[1], roi_top_left[0]:roi_bottom_right[0]]
            filename = f"{cleaned_title}/{count}.jpg"
            cv2.imwrite(filename, roi)
            print(f"Saved {filename}")
        count += 1
    cap.release()
    print(f"--- Process {process_number} finished for {cleaned_title}")


def process_url(url, frame_split=20, quality="720p"):
    print(f"Processing URL: {url} with frame split: {frame_split} and quality: {quality}")
    ydl_opts = {}
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(url, download=False)

    if "playlist" in url:
        print(f"Processing playlist: {info_dict['title']}")
        for entry in info_dict['entries']:
            print(f"Processing video: {entry['title']}")
            process_caller(entry, frame_split, quality)
    else:
        print(f"Processing video: {info_dict['title']}")
        process_caller(info_dict, frame_split, quality)
    print("Finished processing")


def process_caller(entry, frame_split: int, quality: str):
    video_title = entry['title']
    cleaned_title = clean_title(video_title)
    try:
        os.makedirs(cleaned_title)
    except:
        shutil.rmtree(cleaned_title)
        os.makedirs(cleaned_title)
    duration = entry['duration']
    formats = entry.get('formats', None)
    for f in formats:
        if f.get('format_note', None) == quality:
            url = f.get('url', None)
            cpu_count = os.cpu_count()
            ray.get([process_video_parallel.remote(url, int(duration * 31), x, cleaned_title, frame_split) for x in
                     range(cpu_count)])


t1 = timer()
quality = "720p"
frames = 30
# video_url = "https://youtu.be/05A26mwdmuI?si=xl4iUDQNfRCeUQY3"  # Réunion 5 / 5:54
# video_url = "https://www.youtube.com/playlist?list=PLN-TcjS0qZKVUwLwwp94oqqBGxiYWgkTV"  # Pubs vs Vie
# video_url = "https://www.youtube.com/watch?v=hx_xmpZ0HXU"  # OWL 2:14:16
# video_url = "https://www.youtube.com/playlist?list=PLwnBEhITAFhhJPLEj-XcJBAgM_yMaQpKs"  # OWL Playlist

# if you want to download a playlist, the url should contain "playlist"
# if you want to download a single video, you should get the url from the share button
video_url = "https://youtu.be/bceES8u2RrQ"  # Non répertorié perso
process_url(video_url, frame_split=frames, quality=quality)
print("Total Time", timer() - t1)

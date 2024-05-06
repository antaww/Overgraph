from timeit import default_timer as timer
import os, ray, shutil
import cv2
import youtube_dl

ydl_opts = {
    'ignoreerrors': True
}

try:
    os.makedirs('chara_img')
except:
    shutil.rmtree('chara_img')
    os.makedirs('chara_img')

ray.init()


@ray.remote
def process_video_parallel(url, total_frames, process_number):
    cap = cv2.VideoCapture(url)
    num_processes = os.cpu_count()
    frames_per_process = int(total_frames) // num_processes
    cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * process_number)
    count = frames_per_process * process_number

    while count < frames_per_process * (process_number + 1):
        ret, frame = cap.read()
        if not ret:
            break
        filename = f"chara_img/{count}.jpg"
        cv2.imwrite(filename, frame)
        count += 1
    cap.release()


t1 = timer()
video_url = "https://www.youtube.com/watch?v=QipuAvqD-Uw"
ydl_opts = {}
ydl = youtube_dl.YoutubeDL(ydl_opts)
info_dict = ydl.extract_info(video_url, download=False)

formats = info_dict.get('formats', None)
print("Obtaining frames")
for f in formats:
    if f.get('format_note', None) == '144p':
        url = f.get('url', None)
        cap = cv2.VideoCapture(url)
        x = 0
        count = 0
        while x < 10:
            ret, frame = cap.read()
            if not ret:
                break
            filename = r"PATH\shot" + str(x) + ".png"
            x += 1
            cv2.imwrite(filename.format(count), frame)
            count += 300  # Skip 300 frames i.e. 10 seconds for 30 fps
            cap.set(1, count)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        cap.release()
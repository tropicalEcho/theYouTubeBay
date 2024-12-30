import yt_dlp, os, sys, shlex

def clear(): 
    os.system('cls' if os.name == 'nt' else 'clear')

currentDirectory = os.path.expanduser('~\\Downloads')
os.chdir(currentDirectory)

def changePath(newCurrentDirectory):
    try: 
        os.chdir(newCurrentDirectory)
    except FileNotFoundError: 
        print(f"ERROR: DIRECTORY '{newCurrentDirectory}' NOT FOUND.")
    except Exception as e: 
        print(f"ERROR: {str(e).upper()}")

ffmpegPath = r"C:\Program Files\ffmpeg"
manual = """
CLEAR | CLS                                           CLEARS SCREEN
HELP | H                                              PRINTS THIS
DOWNLOAD | DL <URL> <--VIDEO | --AUDIO | -V | -A>     DOWNLOAD THE GIVEN URL
EXIT | QUIT                                           KILLS THE PROGRAM
CHDIR | CD <NEW DIRECTORY>                            CHANGE DOWNLOAD PATH
"""

def progressBar(d):
    if d['status'] == 'downloading':
        try:
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            
            percent = (downloaded / total * 100) if total else 0
            width = 30
            filled = int(width * percent / 100)
            bar = '#' * filled + '-' * (width - filled)

            percent_str = f"{percent:5.1f}"
            
            sys.stdout.write(f'\rDownloading: [{bar}] {percent_str}%')
            sys.stdout.flush()
            
        except Exception:
            sys.stdout.write('\rDownloading...')
            sys.stdout.flush()
    
    elif d['status'] == 'finished':
        sys.stdout.write('\nDownload completed!\n')
        sys.stdout.flush()

def get_ydl_opts():
    video_opts, audio_opts = {}, {}
    
    common_opts = {
        'outtmpl': os.path.join(currentDirectory, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpegPath,
        'quiet': True,
        'progress_hooks': [progressBar],
    }
    
    video_opts.update(common_opts)
    video_opts.update({
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    })
    
    audio_opts.update(common_opts)
    audio_opts.update({
        'format': 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    })
    
    return video_opts, audio_opts

def download(url, format):
    ydl_opts_video, ydl_opts_audio = get_ydl_opts()
    try:
        if format in ["-V", "--VIDEO"]:
            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl: 
                ydl.download([url])
        elif format in ["-A", "--AUDIO"]:
            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl: 
                ydl.download([url])
        else: print("ERROR: INVALID FORMAT!")
    except Exception as e:
        print(f"ERROR: {str(e).upper()}")

if not ffmpegPath:
    ffmpegPath = input("FFMPEG EXECUTABLE LOCATION (USE \\): ")


while True: 
    cmd = shlex.split(input(f"{currentDirectory}$ ").strip())
    command = cmd[0].upper()
    if command in ("CLEAR", "CLS"): 
        clear()
    elif command in ("EXIT", "QUIT"): 
        sys.exit("GOODBYE!")
    elif command in ("CHDIR", "CD"):
        try:
            new_path = cmd.split(" ", 1)[1]
            changePath(new_path)
        except IndexError: 
            print("ERROR: GOT NO NEWPATH")
    elif command in ("HELP", "H"): 
        print(manual)
    elif command in ("DOWNLOAD", "DL"):
        try:
            if len(cmd) < 3:
                print("ERROR: MISSING URL OR FORMAT")
                continue
                
            url = cmd[1]
            format = cmd[2].upper()
            
            isAllowed = False
            validURL_starters = ["http", "www", "youtube", "music"]
            for validURL_starter in validURL_starters:
                if url.lower().startswith(validURL_starter):
                    isAllowed = True
                    break
            
            if not isAllowed:
                print("ERROR: INVALID URL")
                continue
                
            download(url, format)
        except IndexError:
            print("ERROR: INCORRECT COMMAND FORMAT")
    else: 
        print("ERROR: UNIDENTIFIED")
        break
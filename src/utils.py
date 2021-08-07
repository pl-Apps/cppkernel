def download(link, file_name):
    try:
        import sys
        import requests
        with open(file_name, "wb") as f:
            print("Fetching %s" % file_name)
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')
            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))    
                    sys.stdout.flush()
    except:
        pass

def extractall(target, path):
    import zipfile
    import os
    with zipfile.ZipFile(target) as archive:
        j = 0
        import progressbar
        bar = progressbar.ProgressBar(maxval=len(archive.filelist), \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for file in archive.filelist:
            if os.name == "nt":
                if not file.filename.__contains__("aux"):
                    archive.extract(file.filename, path)
            else:
                archive.extract(file.filename, path)
            bar.update(j)
            j += 1
        bar.finish()
import youtube_dl

from flask import (request,
                   render_template,
                   redirect,
                   url_for,
                   send_from_directory)

from . import app
from . import celery


@celery.task(bind=True, name='vod.views.dwl_video')
def dwl_video(self, url):

    def ytdl_finished_hook(d):
        if d['status'] == 'finished':
            print('send mail ...')

    ytdlopts = {
        'progress_hooks': [ytdl_finished_hook],
        'outtmpl': '/tmp/%(id)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ytdlopts) as ytdl:
        info = ytdl.extract_info(url, download=False) 
        ytdl.download([url])

    return {'title': info["title"],
            'ext': info["ext"],
            'id': info["id"],
            'file': "{}.{}".format(info["id"],
                                   info["ext"])}


@app.route("/<task_id>/")
def download_video(task_id):
    t = dwl_video.AsyncResult(task_id).info
    if None is t:
        return render_template('wait.html', url=task_id)
    else:
        try:
            return send_from_directory(
                directory="/tmp",
                filename=t["file"],
                as_attachment=False,
                attachment_filename="{}.{}".format(t["title"], t["ext"]),
            )
        except Exception as ex:
            return "Error when downloading: {}<br>Try with another video url.".format(str(ex))


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        video = request.form['video']
        task = dwl_video.delay(video)
        return redirect(url_for('download_video', task_id=task))
    else:
        return render_template('index.html')

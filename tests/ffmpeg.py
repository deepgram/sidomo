from sdpm import Container


def transcode_file(url):
    with Container(
        '764576996850.dkr.ecr.us-east-1.amazonaws.com/deepgram/base:latest',
        memory_limit_gb=2,
        stderr=False
    ) as c:
        for line in c.run('bash -c "curl %s > tmp.unconverted; ffmpeg -i tmp.unconverted -f wav -acodec pcm_s16le -ac 1 -ar 16000 tmp.wav; cat tmp.wav"' % url):
            yield line


if __name__ == '__main__':
    import sys

    for line in transcode_file(sys.argv[1]):
        sys.stdout.write(line)


from dockit import Container
url = 'http://www2.warwick.ac.uk/fac/soc/sociology/staff/sfuller/media/audio/9_minutes_on_epistemology.mp3'
with Container(
    'cellofellow/ffmpeg',
    memory_limit_gb=2,
    stderr=True,
    stdout=False
) as c:
    for line in c.run(
        'bash -c \"\
            wget -nv -O tmp.unconverted %s;\
            ffmpeg -i tmp.unconverted -f wav -acodec pcm_s16le -ac 1 -ar 16000 tmp.wav;\
            cat tmp.wav\
        \"\
        ' % url
    ):
        print line

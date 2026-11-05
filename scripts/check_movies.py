"""Validate image/state metadata and fully decode the generated H.264 movies."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]


def check(directory):
    import imageio_ffmpeg
    directory=Path(directory);data=json.loads((directory/'catalog.json').read_text())
    for name,expected in data['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,('stale source',name)
    for movie in data['movies']:
        frames=movie['frames'];assert frames[0]['time']==0 and frames[-1]['time']==movie['final_time']
        assert all(a['time']<b['time'] and a['step']<b['step'] for a,b in zip(frames,frames[1:]))
        assert frames[-1]['step']==movie['solver_steps']
        for frame in frames:
            path=directory/frame['file']
            assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==frame['image_sha256']
            with Image.open(path) as image:assert list(image.size)==data['pixel_size'] and image.format=='WEBP'
            assert frame['min_density']>0 and frame['min_pressure']>0
            for scale,minimum,maximum in zip(movie['scales'],('min_density','min_pressure'),('max_density','max_pressure')):
                assert scale['min']<=frame[minimum]<=frame[maximum]<=scale['max']
        path=directory/movie['video']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==movie['video_sha256']
        decoder=imageio_ffmpeg.read_frames(str(path),pix_fmt='rgb24');metadata=next(decoder)
        assert list(metadata['size'])==data['pixel_size'] and metadata['codec']=='h264'
        assert abs(metadata['fps']-movie['fps'])<1e-10
        decoded=sum(1 for _ in decoder)
        assert decoded==len(frames),(movie['id'],decoded,len(frames))
        assert abs(metadata['duration']-len(frames)/movie['fps'])<=1/movie['fps']
        print(movie['id'],':',decoded,'frames decoded; images, dimensions, time range and hashes verified')
    return len(data['movies'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=ROOT/'website/public/assets/movies')
    args=parser.parse_args();check(args.input)

import sys
sys.path.insert(0, '/Users/peng/Documents/cv_utils')

import os
import yaml
from vis_common import *

template_db = """
        <div class="col-sm-3">
            <img src="static/dreambooth_thumbnails/{identity}.png" alt="dog" style="width: 100%">
        </div>"""
template = """
        <div class="col-md-3 captioned_videos" id="res_{vid_id}" style="margin-top: 0px; margin-bottom: 0px ;">
            <video class="video lazy" loop playsinline autoplay muted style="width: 100%">
                <source data-src="static/dreambooth_additional/{identity}_{keyword}.mp4" type="video/mp4"></source>
            </video>
            <p class="compare-caption">{description}</p>
        </div>"""


with open("prompts_db.yaml", "r") as f:
    prompts = yaml.safe_load(f)
    keys = prompts.keys()

with open("gallery_template_db.html", "r") as f:
    html_template = f.read()

content = ""
page_idx = 0
prev_i = 0
row_size = 5
col_size = 4

# dele
folder = 'static/dreambooth_additional'
os.system(f"rm -r {folder}")
os.system(f"mkdir {folder}")


src_folder = '/Users/peng/Downloads/BuildingAR/code/mvdreamer.github.io/static/db_examples/'
row_counter = 0
all_video_num = np.sum(np.array([len(prompts[name].keys()) for name in keys]))
all_rows = 0
for name in keys:
    all_rows += len(prompts[name].keys()) // col_size + 1

for j, name in tqdm(enumerate(keys)):
    row_content = template_db.format(identity=name)
    prompts_id = prompts[name]
    keys = prompts_id.keys()

    for i, k in enumerate(keys):
        description = prompts_id[k]
        current_video = template.format(vid_id=i, identity=name, keyword=k, description=description)

        video_name = f"{name}_{k}.mp4"
        video_file = f"static/dreambooth_additional/{video_name}"
        if not os.path.exists(video_file):
            src_video_file = f"{src_folder}/{video_name}"
            if not os.path.exists(src_video_file):
                print(f"no {video_name}")
            os.system(f"cp {src_video_file} {video_file}")

        row_content += current_video
        first_page = page_idx - 1 < 0
        last_page = row_counter + 1 >= all_rows
        last_item = (i == (len(keys) - 1)) or ((i + 2) % col_size == 0)
        last_row = (row_counter - prev_i + 1 >= row_size)

        if  (last_row and last_item) or (last_page and last_item):
            content += f'<div class="row">{row_content}</div>'
            link1 = f"gallery_db_{page_idx - 1}.html"
            link2 = f"gallery_db_{page_idx + 1}.html"
            active1 = "disabled" if first_page else ""
            active2 = "disabled" if last_page else ""
            html = html_template.replace("{{{content}}}", content).replace("{{{link1}}}", link1).replace("{{{link2}}}", link2)
            html = html.replace("{{{active1}}}", active1).replace("{{{active2}}}", active2)
            html = html.replace("{{{start_idx}}}", str(prev_i+1)).replace("{{{end_idx}}}", str(row_counter+1)).replace("{{{total}}}", str(all_rows))

            with open(f"gallery_db_{page_idx}.html", "w") as f:
                f.write(html)

            row_content = ""
            content = ""
            page_idx += 1
            prev_i = row_counter + 1

        row_counter += (i + 2) // col_size

    if (i + 2) % col_size != 0:
        row_counter += 1

    content += f'<div class="row">{row_content}</div>'

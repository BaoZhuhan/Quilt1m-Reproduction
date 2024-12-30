import cv2
from skimage.metrics import structural_similarity
import numpy as np


def get_histo_srt_im_recon(times_rows, preds, pair_chunk_time):
    running_t = 0
    srt_se_times = []
    srt_s = 0
    srt_e = 0
    chunk_im = []
    chunk_im_time = []
    temp_im = []
    temp_im_time = []
    temp_se = []
    prev_time = 0
    prev_idx = 0
    prev_prd = 0

    for idx, (row, prd) in enumerate(zip(times_rows, preds)):
        if (not row):  # or (not prd):
            # i.e  == 0
            prev_time = row
            prev_idx = idx
            prev_prd = prd
            continue

        if prd and (not prev_prd):
            srt_s = max([prev_time, row - pair_chunk_time])
            temp_im.append(idx)
            temp_im_time.append(row)
        elif prd and prev_prd:
            if row - prev_time > pair_chunk_time:
                # end run
                chunk_im.append(temp_im or [idx])
                chunk_im_time.append(temp_im_time or [row])

                temp_im = []
                temp_im_time = []
                temp_im.append(idx)
                temp_im_time.append(row)
                running_t = 0

                srt_e = row
                temp_se.extend([srt_s, srt_e])
                srt_se_times.append(temp_se)
                temp_se = []
                srt_s = row - pair_chunk_time
            else:
                running_t += row - prev_time
                if running_t > pair_chunk_time:
                    temp_im.append(idx)
                    temp_im_time.append(row)

                    chunk_im.append(temp_im)
                    chunk_im_time.append(temp_im_time)

                    temp_im = []
                    temp_im_time = []
                    running_t = 0

                    srt_e = row
                    temp_se.extend([srt_s, srt_e])
                    srt_se_times.append(temp_se)
                    temp_se = []
                    srt_s = row - pair_chunk_time
                else:
                    # inbetween
                    temp_im.append(idx)
                    temp_im_time.append(row)
        elif (not prd) and prev_prd:
            # srt_e = min([prev_time + pair_chunk_time, row['pts_time']])
            srt_e = row
            temp_se.extend([srt_s, srt_e])
            srt_se_times.append(temp_se)
            temp_se = []

            if not temp_im:
                temp_im.append(prev_idx)
                temp_im_time.append(prev_time)
            chunk_im.append(temp_im)
            chunk_im_time.append(temp_im_time)

            temp_im = []
            temp_im_time = []
            running_t = 0
        elif (not prd) and (not prev_prd):
            pass

        prev_time = row
        prev_idx = idx
        prev_prd = prd
    return srt_se_times, chunk_im, chunk_im_time


def save_frame_chunks_recon(video, stable_se_times, id_, fps, height, width):
    ssim_threshold = 0.98
    median_frames = []
    
    if isinstance(video, str):
        video = cv2.VideoCapture(video)
    
    for index_, start_end_time in enumerate(stable_se_times):
        # 跳过或处理非预期格式
        if not isinstance(start_end_time, (list, tuple)) or len(start_end_time) < 2:
            median_frames.append(None)
            continue
        
        clip_start_time, clip_end_time = start_end_time
        
        video.set(cv2.CAP_PROP_POS_FRAMES, int(clip_start_time * fps))
        
        clip_frames = []
        fixed_frame_count = int((clip_end_time - clip_start_time) * fps)
        for _ in range(fixed_frame_count):
            ret, frame = video.read()
            if not ret:
                break
            clip_frames.append(frame)

        # 下面为原有的 SSIM 判定和处理代码
        ssim_validated_frames = []
        h, w = (height, width) if height else clip_frames[0].shape[:2]
        
        for i in range(len(clip_frames) - 1):
            try:
                top_left_x = np.random.randint(int(w / 2) - 64)
                top_left_y = np.random.randint(int(h / 2) - 64)
                crop1 = clip_frames[i][top_left_y: top_left_y + 64, top_left_x: top_left_x + 64, :]
                crop2 = clip_frames[i + 1][top_left_y: top_left_y + 64, top_left_x: top_left_x + 64, :]
                ssim_val = structural_similarity(crop1, crop2, multichannel=True, channel_axis=2)
                if ssim_val > ssim_threshold:
                    ssim_validated_frames.append(clip_frames[i])
            except IndexError:
                continue
        
        if (clip_end_time - clip_start_time) >= 3 and ssim_validated_frames:
            median_frames.append(np.median(ssim_validated_frames, axis=0).astype(np.uint8))
        else:
            median_frames.append(None)

    video.release()
    return median_frames
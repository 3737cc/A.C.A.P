import os
import numpy as np
from astropy.io import fits
import cv2
from astroalign import register

from bayer import read_fits, bayer_sequence, save_fits_rgb
from calibrate import flat_calibration, bias_calibration, dark_calibration


def color_image(input_folder, output_folder, flat_folder,dark_folder,bias_folder,target_folder, base_filename='ColorImage'):
    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 读取FITS文件数据
            fits_data = read_fits(os.path.join(input_folder, filename))

            # 降噪
            denoise_image = cv2.bilateralFilter(fits_data.astype(np.float32), 9, 75, 75)

            # 校准
            flat_image = flat_calibration(input_folder, flat_folder)
            dark_image = dark_calibration(input_folder, dark_folder)
            bias_image = bias_calibration(input_folder, bias_folder)
            calibrated_image = (denoise_image - dark_image) / (flat_image - bias_image)

            # 对齐
            # 替换为你的目标图像路径
            target_filename = target_folder
            target_data = fits.getdata(target_filename)
            aligned_image, _ = register(calibrated_image, target_data)

            # 叠加
            stacked_image = aligned_image

            # 解拜尔
            bayer_result = bayer_sequence(stacked_image)

            # 构造新的输出文件名
            existing_files = [file for file in os.listdir(output_folder) if file.startswith(base_filename)]
            num_existing_files = len(existing_files)
            output_filename = f'{base_filename}_{num_existing_files + 1}.fits'

            # 构建保存路径
            save_path = os.path.join(output_folder, output_filename)

            # 将RGB图像数据转换为FITS所需的格式
            fits_rgb_data = np.transpose(bayer_result, (2, 0, 1))

            # 保存图像
            save_fits_rgb(fits_rgb_data, save_path)
            print(f"Saved color image: {save_path}")

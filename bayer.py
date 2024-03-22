import os

from astropy.io import fits
import cv2
import numpy as np


def read_fits(file_path):
    # 读取FITS文件
    with fits.open(file_path) as hdul:
        data = hdul[0].data
    return data


def bayer_sequence(img):
    # 应用拜尔序列
    bayer_img = cv2.cvtColor(img, cv2.COLOR_BayerGB2BGR)
    return cv2.cvtColor(bayer_img, cv2.COLOR_BGR2RGB)


def save_fits_rgb(rgb_data, fits_file_path):
    # 创建新的FITS文件，包含RGB通道信息
    hdu = fits.PrimaryHDU(rgb_data)
    hdul = fits.HDUList([hdu])
    hdul.writeto(fits_file_path, overwrite=True)


def bayer_image(input_folder, output_folder, base_filename='Bayer'):
    # 替换为你的FITS文件路径
    fits_file_path = input_folder
    # 读取FITS文件数据
    fits_data = read_fits(fits_file_path)

    # 直方图均值拉伸
    equalized_image = cv2.equalizeHist(fits_data.astype(np.uint8))

    # 应用拜尔序列
    bayer_result = bayer_sequence(equalized_image)

    # 构造新的输出文件名
    existing_files = [file for file in os.listdir(output_folder) if file.startswith(base_filename)]
    num_existing_files = len(existing_files)
    output_filename = f'{base_filename}_{num_existing_files + 1}.fits'
    # 替换为你想保存的文件路径及文件名
    save_fits_path = os.path.join(output_folder, output_filename)
    # 将RGB图像数据转换为FITS所需的格式
    fits_rgb_data = np.transpose(bayer_result, (2, 0, 1))
    return fits_rgb_data, save_fits_path


def bayer_images(input_folder, save_folder):
    print(type(input_folder), type(save_folder))
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            input_file_path = os.path.join(input_folder, filename)

            with fits.open(input_file_path) as hdul_input:
                image_input = hdul_input[0].data
                # 直方图均值拉伸
                equalized_image = cv2.equalizeHist(image_input.astype(np.uint8))

                # 应用拜尔序列
                bayer_result = bayer_sequence(equalized_image)

                # 将RGB图像数据转换为FITS所需的格式
                fits_rgb_data = np.transpose(bayer_result, (2, 0, 1))
                # 保存结果
                save_path = os.path.join(save_folder, f"bayer_{filename}")
                fits.writeto(save_path, fits_rgb_data, overwrite=True)


# if __name__ == '__main__':
#
#     input_folder = "E:/Image/QHY5III715C/aligned/aligned_Capture_00009.fits"
#     output_folder = "E:/Image/QHY5III715C/4"
#
#     bayer_result, save_fits_path = bayer_image(input_folder, output_folder)
#
#     # 调用保存函数
#     save_fits_rgb(bayer_result, save_fits_path)
#
#     print(f"Saved Bayer sequence result as FITS with RGB channels to {save_fits_path}")

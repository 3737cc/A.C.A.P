import os
import astroalign as aa
import cv2
from astropy.io import fits


def align_and_save_all(target_filename, input_folder, save_folder):
    # 读取目标图像
    target_data = fits.getdata(target_filename)

    # 获取目标图像的数据类型
    target_dtype = target_data.dtype

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 加载当前文件
            current_data = fits.getdata(os.path.join(input_folder, filename))

            # 对齐图像
            aligned_data, _ = aa.register(current_data, target_data)

            # 将对齐后的图像数据类型转换为与目标图像相同的数据类型
            aligned_data = aligned_data.astype(target_dtype)

            # 构建保存路径
            save_path = os.path.join(save_folder, f"aligned_{filename}")

            # 保存对齐后的图像
            fits.writeto(save_path, aligned_data, overwrite=True)
            print(f"Saved aligned image: {save_path}")


def process_fits_images(target_filename, input_folder, save_folder):
    # 加载目标FITS图像
    with fits.open(target_filename) as hdul_target:
        image_target = hdul_target[0].data

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            input_file_path = os.path.join(input_folder, filename)

            # 加载输入FITS图像
            with fits.open(input_file_path) as hdul_input:
                image_input = hdul_input[0].data

                # 计算差异
                diff = image_target - image_input

                _, thresholded_diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # 创建一个差异图像中值为0的点的掩码
                zero_mask = diff >= thresholded_diff

                # 应用掩码并计算结果图像
                result_image = image_input.copy()
                result_image[zero_mask] += diff[zero_mask]  # 只在非零像素上添加差异

                # 保存结果
                save_path = os.path.join(save_folder, f"aligned_{filename}")
                fits.writeto(save_path, result_image, overwrite=True)

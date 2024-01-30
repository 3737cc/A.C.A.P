from astropy.io import fits
import os


def flat_calibration(input_folder, target_filename, save_folder):
    # 读取目标图像
    target_data = fits.getdata(target_filename)

    # 调整平场图像
    scale_factor = 1  # 根据需要调整这个值
    target_data = (target_data / 255.0) * scale_factor

    # 防止零除问题
    smoothing_factor = 0.01  # 可以根据实际情况调整这个值
    target_data += smoothing_factor
    target_data[target_data == 0] = target_data[target_data != 0].min()

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 加载当前文件
            current_data = fits.getdata(os.path.join(input_folder, filename))
            # 获取目标图像的数据类型
            current_dtype = current_data.dtype
            # 执行平场校准
            calibrated_image = current_data / target_data
            calibrated_image[calibrated_image < 0] = 0  # 确保不会出现负值

            # 将校准后的图像数据类型转换为与目标图像相同的数据类型
            calibrated_data = calibrated_image.astype(current_dtype)

            # 构建保存路径
            save_path = os.path.join(save_folder, f"flat_{filename}")

            # 保存校准后的图像
            fits.writeto(save_path, calibrated_data, overwrite=True)
            print(f"Saved flat image: {save_path}")


def dark_calibration(input_folder, target_filename, save_folder):
    # 读取目标图像
    target_data = fits.getdata(target_filename)

    # 获取目标图像的数据类型
    target_dtype = target_data.dtype

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 加载当前文件
            current_data = fits.getdata(os.path.join(input_folder, filename))

            # 执行平场校准
            calibrated_image = current_data - target_data
            calibrated_image[calibrated_image < 0] = 0  # 确保不会出现负值

            # 将对齐后的图像数据类型转换为与目标图像相同的数据类型
            calibrated_data = calibrated_image.astype(target_dtype)

            # 构建保存路径
            save_path = os.path.join(save_folder, f"dark_{filename}")

            # 保存对齐后的图像
            fits.writeto(save_path, calibrated_data, overwrite=True)
            print(f"Saved dark image: {save_path}")


def bias_calibration(input_folder, target_filename, save_folder):
    # 读取目标图像
    target_data = fits.getdata(target_filename)

    # 获取目标图像的数据类型
    target_dtype = target_data.dtype

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 加载当前文件
            current_data = fits.getdata(os.path.join(input_folder, filename))

            # 执行平场校准
            calibrated_image = current_data - target_data
            calibrated_image[calibrated_image < 0] = 0  # 确保不会出现负值

            # 将对齐后的图像数据类型转换为与目标图像相同的数据类型
            calibrated_data = calibrated_image.astype(target_dtype)

            # 构建保存路径
            save_path = os.path.join(save_folder, f"bias{filename}")

            # 保存对齐后的图像
            fits.writeto(save_path, calibrated_data, overwrite=True)
            print(f"Saved bias image: {save_path}")

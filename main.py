from PIL import Image, ImageChops
import os # ファイルやフォルダ操作
import glob
import shutil
import datetime # 現在時刻を取得
import time

dir_name = "input" # 画像が入っているフォルダ
new_dir_name = "output" # 画像を保存する先のフォルダ
used_dir_name ="used"

def crop_center(pil_img, crop_width, crop_height): # 画像の中心を切り出し
  img_width, img_height = pil_img.size # 画像の横幅と縦の長さを取得
  # 引数の長さにトリミング
  return pil_img.crop(((img_width - crop_width) // 2,
                        (img_height - crop_height) // 2,
                        (img_width + crop_width) // 2,
                        (img_height + crop_height) // 2))

# ディレクトリが存在しない場合は作成する
if not os.path.exists(dir_name):
  os.mkdir(dir_name)

# ディレクトリが存在しない場合は作成する
if not os.path.exists(new_dir_name):
  os.mkdir(new_dir_name)

# ディレクトリが存在しない場合は作成する
if not os.path.exists(used_dir_name):
  os.mkdir(used_dir_name)

# glob.glob()で抽出された複数のファイルを一括で移動
def move_glob(dst_path, pathname, recursive=True):
  for p in glob.glob(pathname, recursive=recursive):
    shutil.move(p, dst_path)

# pngファイルを移動
move_glob(dir_name, '*.png')
# jpgファイルを移動
move_glob(dir_name, '*.jpg')

files = os.listdir(dir_name)

i = 1

for file in files: # ホーム画面用の処理
  dt_now = datetime.datetime.now()
  print(dt_now.strftime('%Y%m%d_%H%M%S'))
  name = str(dt_now.strftime('%Y%m%d_%H%M%S'))
  name += ".png"

  im_original = Image.open(os.path.join(dir_name, file))
  width, height = im_original.size

  # 縦2, 横3にトリミング
  nim = crop_center(im_original, height * 1.5, height)

  # 切り抜いた画像を保存
  # nim.save(os.path.join(new_dir_name, file))
  nim.save(os.path.join(new_dir_name, name))

  # 1枚ごとに完了を報告
  print(str(i) + " done!")
  i += 1
  time.sleep(1)

# 使った画像は使用済みファイルに移動
move_glob(used_dir_name, "./mikakou/*.PNG")
move_glob(used_dir_name, "./mikakou/*.JPG")

# 終了時に元の画像を削除
# shutil.rmtree(dir_name)

# すべて完了
print("Complete!")
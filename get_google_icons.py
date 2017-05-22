#!/usr/bin/python

"""

This script downloads icon from the https://design.google.com/icons/
and automatically extracts and transfer the icons to your android project
resource folder.

"""

import zipfile, argparse, sys, os, shutil, urllib2

OUTPUT_DIR_NAME = "EF"

DRAWABLE_DIRS = (
	'drawable-hdpi',
	'drawable-mdpi',
	'drawable-xhdpi',
	'drawable-xxhdpi',
	'drawable-xxxhdpi',
)

BASE_DL_LINK = "https://storage.googleapis.com/material-icons/external-assets/v4/icons/zip/"

def transfer_icons(proj_dir):
	icon_dir = os.listdir(OUTPUT_DIR_NAME)[0]
	cur_dir = OUTPUT_DIR_NAME + "/"
	for d in os.listdir(cur_dir + icon_dir):
		cur_dir += icon_dir + "/"

		if os.path.isdir(cur_dir + d) and d == "android":
			cur_dir += d + "/"
			res_dir = proj_dir + "app/src/main/res/"

			for proj_res_dir in os.listdir(res_dir):
				if proj_res_dir in os.listdir(cur_dir):
					ic_file = os.listdir(cur_dir + proj_res_dir)[0]
					src = cur_dir + proj_res_dir + "/" + ic_file
					dest = res_dir + proj_res_dir
					shutil.copy(src, dest)
			break

	print "Transfer Done."

def extract_files(cp_file):
	dc_file = file(cp_file, 'rb')
	with zipfile.ZipFile(dc_file, 'r') as z:
		z.extractall(OUTPUT_DIR_NAME)

def download_icon(icon_name, dimen, color):
	icon_file_name = icon_name + "_" + color + "_" + dimen + "dp.zip"
	output = urllib2.urlopen(BASE_DL_LINK + icon_file_name)
	output_file = open(icon_file_name, 'wb')
	block_size = 8192
	while True:
		b = output.read(block_size)
		if not b:
			break

		output_file.write(b)

	return icon_file_name

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-d', '--dir', help="Path where your project directory resides.", required=True)
	parser.add_argument('-i', '--icon', help="What icon to download", required=True)
	parser.add_argument('-s', '--size', help="Size of the icon to download", required=True)
	parser.add_argument('-c', '--color', help="Color of the icon to download", required=True)

	args = parser.parse_args()

	icon = download_icon(args.icon, args.size, args.color)
	extract_files(icon)

	proj_dir = args.dir

	# Check of the drawable icons exists if not create the drawable folders
	res_dir = proj_dir + "app/src/main/res/"
	for d in DRAWABLE_DIRS:
		if not os.path.isdir(res_dir + d):
			print d + " not found. Creating folder."
			os.makedirs(res_dir + d)

	transfer_icons(proj_dir)
	shutil.rmtree(OUTPUT_DIR_NAME)
	os.remove(icon)


if __name__ == '__main__':
	main()

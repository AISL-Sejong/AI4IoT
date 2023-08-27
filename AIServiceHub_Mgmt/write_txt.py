def create(txt_path, img_path):
    f= open(txt_path,"w+")
    f.write(img_path)
    f.close()
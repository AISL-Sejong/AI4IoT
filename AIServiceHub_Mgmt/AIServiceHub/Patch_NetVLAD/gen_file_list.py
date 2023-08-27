import os

# path="/home/userg/Patch-NetVLAD/patchnetvlad/image_files"
path="{address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/Patch_NetVLAD/patchnetvlad/mobius/union"
file_list=os.listdir(path)

for i in file_list:
    print(i)
    # f = open("patchnetvlad/dataset_imagenames/image_names_index.txt", 'a')
    f = open("{address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/Patch-NetVLAD/patchnetvlad/dataset_imagenames/mobius_db.txt", 'a')
    f.write(i+'\n')

f.close()

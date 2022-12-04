'''
MIT License
Copyright (c) 2021 Stephen Hausler, Sourav Garg, Ming Xu, Michael Milford and Tobias Fischer
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
We thank Nanne https://github.com/Nanne/pytorch-NetVlad for the original design of the NetVLAD
class which in itself was based on https://github.com/lyakaap/NetVLAD-pytorch/blob/master/netvlad.py
In our version we have significantly modified the code to suit our Patch-NetVLAD approach.
'''

import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.neighbors import NearestNeighbors
import faiss
import numpy as np

class NetVLAD(nn.Module):
    """NetVLAD layer implementation"""
    cnt = 0
    def __init__(self, num_clusters=64, dim=128,
                 normalize_input=True, vladv2=False, use_faiss=True):
        """
        Args:
            num_clusters : int
                The number of clusters
            dim : int
                Dimension of descriptors
            normalize_input : bool
                If true, descriptor-wise L2 normalization is applied to input.
            vladv2 : bool
                If true, use vladv2 otherwise use vladv1
        """
        super().__init__()
        self.num_clusters = num_clusters
        self.dim = dim
        self.alpha = 0
        self.vladv2 = vladv2
        self.normalize_input = normalize_input
        self.conv = nn.Conv2d(dim, num_clusters, kernel_size=(1, 1), bias=vladv2)
        # noinspection PyArgumentList
        self.centroids = nn.Parameter(torch.rand(num_clusters, dim))
        self.use_faiss = use_faiss


    def init_params(self, clsts, traindescs):   #self, 클러스터s, 학습discriptors
        print("여긴 들어가지가 않네요")
        if not self.vladv2:
            clstsAssign = clsts / np.linalg.norm(clsts, axis=1, keepdims=True)
            dots = np.dot(clstsAssign, traindescs.T)
            dots.sort(0)
            dots = dots[::-1, :]  # sort, descending

            self.alpha = (-np.log(0.01) / np.mean(dots[0, :] - dots[1, :])).item()
            # noinspection PyArgumentList
            self.centroids = nn.Parameter(torch.from_numpy(clsts))
            # noinspection PyArgumentList
            self.conv.weight = nn.Parameter(torch.from_numpy(self.alpha * clstsAssign).unsqueeze(2).unsqueeze(3))
            self.conv.bias = None
            print("1")
        else:
            if not self.use_faiss:
                knn = NearestNeighbors(n_jobs=-1)
                knn.fit(traindescs)
                del traindescs
                ds_sq = np.square(knn.kneighbors(clsts, 2)[1])
                del knn
                print("2")
            else:
                print("여기로간다 여기로")
                index = faiss.IndexFlatL2(traindescs.shape[1])
                print("벡터의 차원은? :")
                print(index.ntotoal)
                # noinspection PyArgumentList
                index.add(traindescs)
                del traindescs
                # noinspection PyArgumentList
                print(index.search(clst, 2))
                ds_sq = np.square(index.search(clsts, 2)[1])
                #D, I = index.search(query_vector, k)     # actual search, k-nearest-neighbor search
                #D = len(query_vector), I = len(db_vector)형태의 array -> D는 찾아낸 nearest-neighbor와 query간의 거리, I는 그에 상응하는 database index
                del index
                print("3")

            self.alpha = (-np.log(0.01) / np.mean(ds_sq[:, 1] - ds_sq[:, 0])).item()
            # noinspection PyArgumentList
            self.centroids = nn.Parameter(torch.from_numpy(clsts))
            del clsts, ds_sq

            # noinspection PyArgumentList
            self.conv.weight = nn.Parameter(
                (2.0 * self.alpha * self.centroids).unsqueeze(-1).unsqueeze(-1)
            )
            # noinspection PyArgumentList
            self.conv.bias = nn.Parameter(
                - self.alpha * self.centroids.norm(dim=1)
            )

    def forward(self, x):

        N, C = x.shape[:2]

        if self.normalize_input:
            x = F.normalize(x, p=2, dim=1)  # across descriptor dim

        # soft-assignment
        # print("******************")
        # print(N)
        # print(self.num_clusters)
        # print("******************")
        soft_assign = self.conv(x).view(N, self.num_clusters, -1)
        soft_assign = F.softmax(soft_assign, dim=1)

        x_flatten = x.view(N, C, -1)

        # calculate residuals to each clusters
        vlad = torch.zeros([N, self.num_clusters, C], dtype=x.dtype, layout=x.layout, device=x.device)
        f=open("/{filepath}/AIServiceHub_Mgmt/AIServiceHub/Patch_NetVLAD/log.txt",'a')
        itera = str(int(self.cnt))
        f.write("\n\n\n\n"+str(itera)+"'s image\n")
        #print("\n\n새로운 이미지\n\n")
        for C in range(self.num_clusters):  # slower than non-looped, but lower memory usage
            residual = x_flatten.unsqueeze(0).permute(1, 0, 2, 3) - \
                self.centroids[C:C + 1, :].expand(x_flatten.size(-1), -1, -1).permute(1, 2, 0).unsqueeze(0)
            residual *= soft_assign[:, C:C + 1, :].unsqueeze(2)
            vlad[:, C:C + 1, :] = residual.sum(dim=-1)
            #cpu_residual = residual.cpu()

            # ************************************배치사이즈 조정하는건, 
            # ************************************이 후 레이어 개발 이 방향으로 결정나면
            # ************************************

            # cpu_residual = residual.cpu()
            # np_residual = cpu_residual.numpy()
            # np.set_printoptions(threshold=np.inf)
            # f.write("for" + str(C) + "'s centroid\n")
            # f.write(str(np_residual.mean(axis = 3).mean(axis = 2))+"\n")
            # print(itera+"'s complete")


        # f=open("gaegatnae.txt",'a')
        # cpu_vlad = vlad.cpu()
        # np_vlad = cpu_vlad.numpy()
        # np.set_printoptions(threshold=np.inf)
        # print(np_vlad.shape)
        # f.write("\n\n\n\n\n\n\n")
        # f.write(str(np_vlad))
        # f.write("\n\n\n\n\n\n\n")
        # f.close()
            
        # f.close()
        vlad = F.normalize(vlad, p=2, dim=2)  # intra-normalization
        vlad = vlad.view(x.size(0), -1)  # flatten
        vlad = F.normalize(vlad, p=2, dim=1)  # L2 normalize
        # f=open("norm_first_VLAD.txt",'w')
        # cpu_vlad = vlad.cpu()
        # np_vlad = cpu_vlad.numpy()
        #print(vlad.shape)
        #np.set_printoptions(threshold=np.inf)
        #print(np_vlad.shape)
        #f.write(str(np_vlad))
        #f.close()
        self.cnt += 1
        return vlad
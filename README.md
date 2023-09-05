# AI4IoT
AI4IoT is an AI enabler for standard IoT platforms.  
Our goal is to develop open sources to support AI functions on standard IoT platforms such as Mobius, an open source platform of oneM2M, and EdgeX.  
We also develop various Use Cases using the AI4IoT framework. 

# Version
Version 2.0.0

# About this repository
This repository contains a framework for providing efficient artificial intelligence services to Mobius, the oneM2M standard platform.  
It does not include requirement.txt related to module installation.  
We recommend installing and using Mobius on your local or server.  

# Installation 
~~~bash
git clone https://github.com/AISL-sejong/AI4IoT.git
~~~

**🔥 Download the modules you need directly using pip or conda. 🔥**


# Running the examples
✅ {ip} refers to the IP address of Mobius.  
✅ {port} refers to the Mobius server port or Mobius MQTT port depending on the situation.  
✅ {address} means your file path.  
✅ In AI4IoT/AIServiceHub_Mgmt/AIServiceHub/yolov5_crowdhuman/utils/google_utils.py, the GitHub address and the issued GitHub token value must be written in line 25. (Currently written information cannot be used.)  
✅ The nCube-Thyme-Node.js was used to create a container and create a sub in here.

1. Run sub_target.py on AIServiceBrokerIPE_Mgmt.
2. Run main.py on AIServiceHub_Mgmt.


# Related
[📖 Journal](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002950289)  
[📷 Demo Video](https://www.youtube.com/watch?v=Ds2LofmWyKo)  
📧 Contact E-mail: kimyj.sejong@gmail.com  

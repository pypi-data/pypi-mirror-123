#coding:UTF-8 #定义程序的编码
#通过setuptools模块导入所需要的函数
from setuptools import setup, find_packages
setup(    
  name="mldn-masg",    
  version="1.0",    
  author="李兴华",    
  url="http://www.yootk.com",    
  packages=find_packages("src"), #src就是模块的保存目录   
  package_dir = {'':'src'},   # 告诉setuptools包都在src下    
  package_data = {        
   # 任何包中含有.txt文件，都包含它         
   "": ['*.txt','*.info','*.properties','*.py'],        
   # 包含demo包data文件夹中的 *.dat文件        
   "": ['data/*.*'],    
   },    
   exclude=["*.test", "*.test.*", "test.*", "test"] # 取消所有的测试包   
   )

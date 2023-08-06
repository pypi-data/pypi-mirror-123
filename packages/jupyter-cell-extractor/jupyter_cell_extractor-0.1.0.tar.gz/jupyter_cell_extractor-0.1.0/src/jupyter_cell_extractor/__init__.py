
#from pkg_resources import resource_filename
import os
this_dir, _ = os.path.split(__file__)
#print("nigger \n")
#print(this_dir,"\n")
#print(os.path.join(this_dir, "data", "classic.tplx"))
os.environ["TEMPLATE_TPLX"] = os.path.join(this_dir, "data", "classic.tplx")

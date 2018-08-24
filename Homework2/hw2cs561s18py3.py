from sklearn.externals import joblib
import numpy as np
import sys
import warnings
warnings.filterwarnings('ignore')
#import time

#start = time.time()
input_file = open(sys.argv[2], "r")
content = input_file.read()
feature = np.array(content).ravel()

loaded_model = joblib.load('modelmlp3.sav')



pred = loaded_model.predict(feature)
#print(pred)
output_file = open("output.txt", 'w')
output_file.write(str(pred[0]))
output_file.close()

#end = time.time()
#print("Run Time: ",str(end - start))
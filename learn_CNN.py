#import area
from keras.datasets import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

from keras.preprocessing.image import array_to_img, img_to_array, load_img
from matplotlib import pyplot as plt
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
from keras.optimizers import Adam
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.callbacks import TensorBoard
import numpy as np

#preparing data area

cif_labels=["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

train_data=[]
train_labels=[]
train_times=700
count=0
for index, img in enumerate(x_train):
  if y_train[index][0]==0 or y_train[index][0]==2:
    train_data.append(img)
    train_labels.append(y_train[index])
    count=count+1
  if count ==train_times:
    break

test_data=[]
test_labels=[]
test_times=300
count=0
for index, img in enumerate(x_test):
  if y_test[index][0]==0 or y_test[index][0]==2:
    test_data.append(img)
    test_labels.append(y_test[index])
    count=count+1
  if count ==test_times:
    break

_train_data=np.array(train_data)
_train_data=_train_data.astype("float32")
_train_data/=255

_test_data=np.array(test_data)
_test_data=_test_data.astype("float32")
_test_data/=255

_train_labels=np_utils.to_categorical(train_labels, 10)
_test_labels=np_utils.to_categorical(test_labels, 10)

#create model
model=Sequential()

model.add(Conv2D(32, (3,3), padding="same", input_shape=(32,32,3)))
model.add(Activation("relu"))
model.add(Conv2D(32, (3,3), padding="same"))
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3,3), padding="same"))
model.add(Activation("relu"))
model.add(Conv2D(64, (3,3), padding="same"))
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation="softmax"))

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

tsb=TensorBoard(log_dir="./logs")
batch_size=32
epochs=20
history=model.fit(_train_data, _train_labels, batch_size=batch_size, epochs=epochs, validation_split=0.2, callbacks=[tsb])

model.save("./learn_CNN_model.h5")

#check learning status
n=list(range(1,epochs+1))
plt.plot(n,history.history["val_loss"], label="val_loss")
#plt.plot(n,history.history["loss"], label="loss")
plt.legend()
plt.show()

#predict and check results
img_pred=model.predict_classes(_test_data)

for i in range(3):
  ax=plt.figure().add_subplot(4,1,1)
  img=array_to_img(test_data[i])
  ax.imshow(img)
  plt.title("pred: {0}, ans: {1}".format(cif_labels[img_pred[i]], cif_labels[test_labels[i][0]]))
  ax.axis("off")
  plt.show()

mat=[[0,0],[0,0]]

for i in range(len(img_pred)):
  if img_pred[i]==test_labels[i][0]:
    if img_pred[i]==0:
      mat[0][0]=mat[0][0]+1
    else:
      mat[1][1]=mat[1][1]+1
  else:
    if img_pred[i]==0:
      mat[0][1]=mat[0][1]+1
    else:
      mat[1][0]=mat[1][0]+1
print(mat)

r=100*(mat[0][0]+mat[1][1])/300
print(round(r,1))

import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization, AveragePooling2D
from keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.utils import to_categorical
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint

from datetime import datetime
import matplotlib.pyplot as plt

test=pd.read_csv('C:\\Users\\JooHwan\\Desktop\\MFCC.csv')
temp = pd.DataFrame(test)
del test

temp[['Frame1-1','Frame1-2','Frame1-3','Frame1-4','Frame1-5','Frame1-6','Frame1-7','Frame1-8','Frame1-9','Frame1-10','Frame1-11','Frame1-12']]=temp['Frame1'].str.split(' ', expand=True)
temp[['Frame2-1','Frame2-2','Frame2-3','Frame2-4','Frame2-5','Frame2-6','Frame2-7','Frame2-8','Frame2-9','Frame2-10','Frame2-11','Frame2-12']]=temp['Frame2'].str.split(' ', expand=True)
temp[['Frame3-1','Frame3-2','Frame3-3','Frame3-4','Frame3-5','Frame3-6','Frame3-7','Frame3-8','Frame3-9','Frame3-10','Frame3-11','Frame3-12']]=temp['Frame3'].str.split(' ', expand=True)
temp[['Frame4-1','Frame4-2','Frame4-3','Frame4-4','Frame4-5','Frame4-6','Frame4-7','Frame4-8','Frame4-9','Frame4-10','Frame4-11','Frame4-12']]=temp['Frame4'].str.split(' ', expand=True)
temp[['Frame5-1','Frame5-2','Frame5-3','Frame5-4','Frame5-5','Frame5-6','Frame5-7','Frame5-8','Frame5-9','Frame5-10','Frame5-11','Frame5-12']]=temp['Frame5'].str.split(' ', expand=True)
del temp['Frame1']
del temp['Frame2']
del temp['Frame3']
del temp['Frame4']
del temp['Frame5']


testset = np.array(temp.astype(float))
del temp
le =LabelEncoder()
X = testset[:,3:]

Y = testset[:,1]
YY = np_utils.to_categorical(le.fit_transform(Y))
num_labels = len(YY[1])

x_train, x_test, y_train, y_test = train_test_split(X, YY, test_size=0.1, random_state = 42)
num_sets_test = len(x_test)
num_sets_train = len(x_train)


num_rows = 5
num_columns = 12
num_channels = 1
filter_size = 2

x_train = x_train.reshape(num_sets_train, num_rows, num_columns, num_channels)
x_test = x_test.reshape(num_sets_test, num_rows, num_columns, num_channels)



model = Sequential()


model.add(Conv2D(filters=128, kernel_size=3, input_shape=(num_rows, num_columns, num_channels), activation='relu',strides=1,padding='same'))
model.add(MaxPooling2D(pool_size=3,padding='same',strides=1))
model.add(BatchNormalization())
model.add(Dropout(0.2))

model.add(Conv2D(filters=128, kernel_size=3, activation='relu',strides=1,padding= 'same'))
model.add(MaxPooling2D(pool_size=3,padding='same',strides=1))



model.add(Flatten())
#dense layer add for filtering
model.add(Dense(256))

model.add(Dropout(0.2))

model.add(Dense(128))

model.add(Dense(num_labels, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')



score = model.evaluate(x_test, y_test, verbose=1)
accuracy = 100*score[1]

print("Pre-training accuracy: %.4f%%" % accuracy)



num_epochs = 70
num_batch_size = 128

checkpointer = ModelCheckpoint(filepath='saved_models/MJJ.hdf5',
                               verbose=1, save_best_only=True)

start = datetime.now()
history = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs, validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

duration = datetime.now() - start
print("Training completed in time: ", duration)


acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

model.save('MJJaftercoaching_non_biased_solving.h5')
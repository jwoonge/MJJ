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
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint
import csv
from datetime import datetime
import matplotlib.pyplot as plt

#test=pd.read_csv('C:\\Users\\USER-PC\\Desktop\\MFCC.csv')
def voice_all_class() :
    temp = []
    f = open('dataset/MFCC_dummy_noran_voice_class.csv', 'r')
    reader = csv.reader(f)
    for row in reader:
        temp.append(row)
    f.close()

    temp = np.array(temp)
    print(temp.shape)
    X = temp[0:, 0:60]
    Y = temp[0:, 60]
    del temp

    le = LabelEncoder()
    one = OneHotEncoder()
    Y = Y.astype(np.int64)
    Y = np_utils.to_categorical(Y)
    num_labels = len(Y[1])

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    num_sets_test = len(x_test)
    num_sets_train = len(x_train)

    print(num_labels)
    num_rows = 5
    num_columns = 12
    num_channels = 1
    filter_size = 2

    x_train = x_train.reshape(num_sets_train, num_rows, num_columns, num_channels)
    x_test = x_test.reshape(num_sets_test, num_rows, num_columns, num_channels)

    print(x_train[1])

    model = Sequential()

    model.add(Conv2D(filters=128, kernel_size=3, input_shape=(num_rows, num_columns, num_channels), activation='relu',
                     strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=128, kernel_size=3, activation='relu', strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))

    model.add(Flatten())
    # dense layer add for filtering
    model.add(Dense(256, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(128, activation='relu'))

    model.add(Dense(num_labels, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
                  optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999))

    score = model.evaluate(x_test, y_test, verbose=1)
    accuracy = 100 * score[1]

    print("Pre-training accuracy: %.4f%%" % accuracy)

    num_epochs = 500
    num_batch_size = 2048
    # num_batch_size = 128

    checkpointer = ModelCheckpoint(filepath='saved_models/MFCC_ㄴㄹㅇㅁ_voiced_classification.hdf5',
                                   verbose=1, save_best_only=True)

    start = datetime.now()
    history = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs,
                        validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

    duration = datetime.now() - start
    print("Training completed in time: ", duration)

    model.save('MJJaftercoaching_128.h5')
def unvoice_all_class() :
    temp = []
    f = open('dataset/MFCC_dummy_whoe_unvoice_class.csv', 'r')
    reader = csv.reader(f)
    for row in reader:
        temp.append(row)
    f.close()

    temp = np.array(temp)
    print(temp.shape)
    X = temp[0:, 0:60]
    Y = temp[0:, 60]
    del temp

    le = LabelEncoder()
    one = OneHotEncoder()
    Y = Y.astype(np.int64)
    Y = np_utils.to_categorical(Y)
    num_labels = len(Y[1])

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    num_sets_test = len(x_test)
    num_sets_train = len(x_train)

    print(num_labels)
    num_rows = 5
    num_columns = 12
    num_channels = 1
    filter_size = 2

    x_train = x_train.reshape(num_sets_train, num_rows, num_columns, num_channels)
    x_test = x_test.reshape(num_sets_test, num_rows, num_columns, num_channels)

    print(x_train[1])

    model = Sequential()

    model.add(Conv2D(filters=128, kernel_size=3, input_shape=(num_rows, num_columns, num_channels), activation='relu',
                     strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=128, kernel_size=3, activation='relu', strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))

    model.add(Flatten())
    # dense layer add for filtering
    model.add(Dense(256, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(128, activation='relu'))

    model.add(Dense(num_labels, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
                  optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999))

    score = model.evaluate(x_test, y_test, verbose=1)
    accuracy = 100 * score[1]

    print("Pre-training accuracy: %.4f%%" % accuracy)

    num_epochs = 500
    num_batch_size = 8192
    # num_batch_size = 128

    checkpointer = ModelCheckpoint(filepath='saved_models/MFCC_whole_unvoiced_classification.hdf5',
                                   verbose=1, save_best_only=True)

    start = datetime.now()
    history = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs,
                        validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

    duration = datetime.now() - start
    print("Training completed in time: ", duration)

    model.save('MJJaftercoaching_128.h5')
def ygd_class() :
    temp = []
    f = open('dataset/MFCC_dummy_ja_거된그.csv', 'r')
    reader = csv.reader(f)
    for row in reader:
        temp.append(row)
    f.close()

    temp = np.array(temp)
    print(temp.shape)
    X = temp[0:, 0:60]
    Y = temp[0:, 60]
    del temp

    le = LabelEncoder()
    one = OneHotEncoder()
    Y = Y.astype(np.int64)
    Y = np_utils.to_categorical(Y)
    num_labels = len(Y[1])

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    num_sets_test = len(x_test)
    num_sets_train = len(x_train)

    print(num_labels)
    num_rows = 5
    num_columns = 12
    num_channels = 1
    filter_size = 2

    x_train = x_train.reshape(num_sets_train, num_rows, num_columns, num_channels)
    x_test = x_test.reshape(num_sets_test, num_rows, num_columns, num_channels)

    print(x_train[1])

    model = Sequential()

    model.add(Conv2D(filters=128, kernel_size=3, input_shape=(num_rows, num_columns, num_channels), activation='relu',
                     strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=128, kernel_size=3, activation='relu', strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))

    model.add(Flatten())
    # dense layer add for filtering
    model.add(Dense(256, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(128, activation='relu'))

    model.add(Dense(num_labels, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
                  optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999))

    score = model.evaluate(x_test, y_test, verbose=1)
    accuracy = 100 * score[1]

    print("Pre-training accuracy: %.4f%%" % accuracy)

    num_epochs = 200
    num_batch_size = 8192
    # num_batch_size = 128

    checkpointer = ModelCheckpoint(filepath='saved_models/MFCC_ygd.hdf5',
                                   verbose=1, save_best_only=True)

    start = datetime.now()
    history = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs,
                        validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

    duration = datetime.now() - start
    print("Training completed in time: ", duration)
def pmp_class() :
    temp = []
    f = open('dataset/MFCC_dummy_ja_파마파비유.csv', 'r')
    reader = csv.reader(f)
    for row in reader:
        temp.append(row)
    f.close()

    temp = np.array(temp)
    print(temp.shape)
    X = temp[0:, 0:60]
    Y = temp[0:, 60]
    del temp

    le = LabelEncoder()
    one = OneHotEncoder()
    Y = Y.astype(np.int64)
    Y = np_utils.to_categorical(Y)
    num_labels = len(Y[1])

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    num_sets_test = len(x_test)
    num_sets_train = len(x_train)

    print(num_labels)
    num_rows = 5
    num_columns = 12
    num_channels = 1
    filter_size = 2

    x_train = x_train.reshape(num_sets_train, num_rows, num_columns, num_channels)
    x_test = x_test.reshape(num_sets_test, num_rows, num_columns, num_channels)

    print(x_train[1])

    model = Sequential()

    model.add(Conv2D(filters=128, kernel_size=3, input_shape=(num_rows, num_columns, num_channels), activation='relu',
                     strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=128, kernel_size=3, activation='relu', strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))

    model.add(Flatten())
    # dense layer add for filtering
    model.add(Dense(256, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(128, activation='relu'))

    model.add(Dense(num_labels, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
                  optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999))

    score = model.evaluate(x_test, y_test, verbose=1)
    accuracy = 100 * score[1]

    print("Pre-training accuracy: %.4f%%" % accuracy)

    num_epochs = 200
    num_batch_size = 8192
    # num_batch_size = 128

    checkpointer = ModelCheckpoint(filepath='saved_models/MFCC_pmp.hdf5',
                                   verbose=1, save_best_only=True)

    start = datetime.now()
    history = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs,
                        validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

    duration = datetime.now() - start
    print("Training completed in time: ", duration)
def ycgyh_class() :
    temp = []
    f = open('dataset/MFCC_dummy_ja_양치경구후.csv', 'r')
    reader = csv.reader(f)
    for row in reader:
        temp.append(row)
    f.close()

    temp = np.array(temp)
    print(temp.shape)
    X = temp[0:, 0:60]
    Y = temp[0:, 60]
    del temp

    le = LabelEncoder()
    one = OneHotEncoder()
    Y = Y.astype(np.int64)
    Y = np_utils.to_categorical(Y)
    num_labels = len(Y[1])

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    num_sets_test = len(x_test)
    num_sets_train = len(x_train)

    print(num_labels)
    num_rows = 5
    num_columns = 12
    num_channels = 1
    filter_size = 2

    x_train = x_train.reshape(num_sets_train, num_rows, num_columns, num_channels)
    x_test = x_test.reshape(num_sets_test, num_rows, num_columns, num_channels)

    print(x_train[1])

    model = Sequential()

    model.add(Conv2D(filters=128, kernel_size=3, input_shape=(num_rows, num_columns, num_channels), activation='relu',
                     strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=128, kernel_size=3, activation='relu', strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))

    model.add(Flatten())
    # dense layer add for filtering
    model.add(Dense(256, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(128, activation='relu'))

    model.add(Dense(num_labels, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
                  optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999))

    score = model.evaluate(x_test, y_test, verbose=1)
    accuracy = 100 * score[1]

    print("Pre-training accuracy: %.4f%%" % accuracy)

    num_epochs = 200
    num_batch_size = 8192
    # num_batch_size = 128

    checkpointer = ModelCheckpoint(filepath='saved_models/MFCC_ycgyh.hdf5',
                                   verbose=1, save_best_only=True)

    start = datetime.now()
    history = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs,
                        validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

    duration = datetime.now() - start
    print("Training completed in time: ", duration)
def all_class() :
    temp = []
    f = open('dataset/MFCC_dummy_full_classification.csv', 'r')
    reader = csv.reader(f)
    for row in reader:
        temp.append(row)
    f.close()

    temp = np.array(temp)
    print(temp.shape)
    X = temp[0:, 0:60]
    Y = temp[0:, 60]
    del temp

    le = LabelEncoder()
    one = OneHotEncoder()
    Y = Y.astype(np.int64)
    Y = np_utils.to_categorical(Y)
    num_labels = len(Y[1])

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    num_sets_test = len(x_test)
    num_sets_train = len(x_train)

    print(num_labels)
    num_rows = 5
    num_columns = 12
    num_channels = 1
    filter_size = 2

    x_train = x_train.reshape(num_sets_train, num_rows, num_columns, num_channels)
    x_test = x_test.reshape(num_sets_test, num_rows, num_columns, num_channels)

    print(x_train[1])

    model = Sequential()

    model.add(Conv2D(filters=128, kernel_size=3, input_shape=(num_rows, num_columns, num_channels), activation='relu',
                     strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=128, kernel_size=3, activation='relu', strides=1, padding='same'))
    model.add(MaxPooling2D(pool_size=2, padding='same', strides=1))

    model.add(Flatten())
    # dense layer add for filtering
    model.add(Dense(256, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(128, activation='relu'))

    model.add(Dense(num_labels, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
                  optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999))

    score = model.evaluate(x_test, y_test, verbose=1)
    accuracy = 100 * score[1]

    print("Pre-training accuracy: %.4f%%" % accuracy)

    num_epochs = 100
    num_batch_size = 8192
    # num_batch_size = 128

    checkpointer = ModelCheckpoint(filepath='saved_models/MFCC_ALL.hdf5',
                                   verbose=1, save_best_only=True)

    start = datetime.now()
    history = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs,
                        validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

    duration = datetime.now() - start
    print("Training completed in time: ", duration)
    model.save('MJJaftercoaching_128.h5')
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

all_class()
__author__ = "Jakob Aungiers"
__copyright__ = "Jakob Aungiers 2018"
__version__ = "2.0.0"
__license__ = "MIT"


import os
import json
import time
import math
import matplotlib.pyplot as plt
from core.data_processor import DataLoader
from core.model import Model,LossHistory
import numpy as np

from core.model import newest_model

config_file = 'web_flask/LSTM/config.json'

def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()

def plot_results_multiple(predicted_data, true_data, prediction_len):
    print(predicted_data)
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    ax.plot(predicted_data)
    #bx = fig.add_subplot(222)
    #bx.plot(true_data)
    #bx.plot(predicted_data)
    '''
	# Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    '''
    plt.show()

def main(train_after = False):
    config_file = 'web_flask/LSTM/config.json'
    configs = json.load(open(config_file, 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])

    data = DataLoader(
        configs['data']['filename'],
        configs['data']['train_test_split'],
        configs['data']['columns'],
        normalise_meth=configs['data']['normalise']
    )

    model = Model()
    model.build_model(configs) if not train_after else \
        model.load_model(os.path.join( configs['model']['save_dir'],configs['model']['model_name']))
    history = LossHistory()

    x, y = data.get_train_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )

    x_test, y_test = data.get_test_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )

	# in-memory training
    model.train(
    x,
    y,
    epochs = configs['training']['epochs'],
    batch_size = configs['training']['batch_size'],
    save_dir = configs['model']['save_dir'],
    history = history,
    x_test=x_test, 
    y_test = y_test
    )
    '''
    # out-of memory generative training
    steps_per_epoch = math.ceil((data.len_train - configs['data']['sequence_length']) / configs['training']['batch_size'])
    model.train_generator(
        data_gen=data.generate_train_batch(
            seq_len=configs['data']['sequence_length'],
            batch_size=configs['training']['batch_size'],
            normalise=configs['data']['normalise']
        ),
        epochs=configs['training']['epochs'],
        batch_size=configs['training']['batch_size'],
        steps_per_epoch=steps_per_epoch,
        save_dir=configs['model']['save_dir']
    )

    '''
    
    history.loss_plot('epoch')
    #loss, accuracy = model.model.evaluate(x_test, y_test)
    #print(loss,accuracy)
    
    

    #predictions = model.predict_sequences_multiple(x_test, configs['data']['sequence_length'], configs['data']['sequence_length'])
    #predictions = model.predict_sequence_full(x_test, configs['data']['sequence_length'])
    predictions = model.predict_point_by_point(x[0])#_test)

    #plot_results_multiple(predictions, y, configs['data']['sequence_length'])
    plot_results(predictions, y)

def main_plot():

    configs = json.load(open(config_file, 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
    data = DataLoader(
        os.path.join('data', configs['data']['filename']),
        configs['data']['train_test_split'],
        configs['data']['columns'],
        normalise_meth=configs['data']['normalise']
    )

    x, y = data.get_test_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )
    model = Model()
    global newest_model
    if newest_model:
        model_way = newest_model
    else:
        model_way = '/home/bf/Documents/Projects/helpplay/HelpPlay/train/LSTM-Neural-Network-for-Time-Series-Prediction/saved_models/10062019-163648-e40.h5'
    model.load_model(model_way)
    print(model.model.evaluate(x, y))
    pre_y = model.predict_point_by_point(x)
    print(x)
    plot_results(pre_y,y)

if __name__ == '__main__':
    
    #main_plot() # 用来测试集
    main(train_after=True) # 用来训练新模型或在老的基础上训练
    #plot_results_multiple([1,2,3],[2,3,4],0)
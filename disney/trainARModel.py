# coding: utf-8
from __future__ import print_function
import tensorflow as tf
import matplotlib.pyplot as plt

def main():

    csv_file_name = './data/BuzzLightyearPlanetRescue.txt'
    reader = tf.contrib.timeseries.CSVReader(csv_file_name)
    train_input_fn = tf.contrib.timeseries.RandomWindowInputFn(
        reader,batch_size = 4,window_size=16
    )

    with tf.Session() as sess:
        data = reader.read_full()
        coord = tf.train.Coordinator()
        tf.train.start_queue_runners(sess=sess, coord=coord)
        data = sess.run(data)
        coord.request_stop()

    ar = tf.contrib.timeseries.ARRegressor(
        periodicities=200,input_window_size=12,output_window_size=4,
        num_features=1,
        loss=tf.contrib.timeseries.ARModel.NORMAL_LIKELIHOOD_LOSS,
        model_dir = u'./AR_BuzzLightyearPlanetRescue.pth'
    )

    ar.train(input_fn = train_input_fn,steps = 6000)

    evaluation_input_fn = tf.contrib.timeseries.WholeDatasetInputFn(reader)
    evaluation = ar.evaluate(input_fn=evaluation_input_fn,steps = 1)

    (predictions,) = tuple(ar.predict(
        input_fn=tf.contrib.timeseries.predict_continuation_input_fn(
            evaluation,steps=250
        )
    ))

    plt.figure(figsize=(15,5))
    plt.plot(data['times'].reshape(-1),data['values'].reshape(-1),label=
    'origin')
    plt.plot(evaluation['times'].reshape(-1),evaluation['mean'].reshape(-1),
    label='evaluation')
    plt.plot(predictions['times'].reshape(-1),
    predictions['mean'].reshape(-1),label='prediction')
    plt.xlabel('time_step')
    plt.ylabel('values')
    plt.legend(loc=4)
    plt.savefig('predict_result.jpg')

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
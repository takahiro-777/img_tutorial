#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
参考リスト
https://www.tensorflow.org/get_started/mnist/pros
-> 公式チュートリアルの該当ページ

http://qiita.com/KojiOhki/items/64a2ee54214b01a411c7
-> 公式チュートリアルの翻訳（少々内容が古く、global_variables_initializer()のところだけ本家元に修正した）
"""

#import modules
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# FLAG args
tf.app.flags.DEFINE_string("run_mode", "inference", "run mode(train or inference)")
tf.app.flags.DEFINE_string("continuity", True, "continue or from_zero")
FLAGS = tf.app.flags.FLAGS

#functions
# 重みの初期化
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# 畳み込みとプーリング
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


#main function
if __name__ == '__main__':
    # placeholder(入力データの配列型)、Variable(モデルのパラメータ)の定義
    W = tf.Variable(tf.zeros([784,10]))
    b = tf.Variable(tf.zeros([10]))
    x = tf.placeholder(tf.float32, shape=[None, 784])
    y_ = tf.placeholder(tf.float32, shape=[None, 10])

    # 第一畳み込み層
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    x_image = tf.reshape(x, [-1,28,28,1])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # 第二畳み込み層
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # 高密度結合層
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # ドロップアウト
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # 読み出し層
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])
    y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    # 誤差関数の定義、最適化
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # セッションの記述、変数の初期化
    sess = tf.InteractiveSession()
    saver = tf.train.Saver()

    # 学習========
    if FLAGS.run_mode == "train":
        step = 0
        if FLAGS.continuity == True:
            ckpt = tf.train.get_checkpoint_state('./model/')
            if ckpt: # checkpointがある場合
                last_model = ckpt.model_checkpoint_path # 最後に保存したmodelへのパス
                print("load " + last_model)
                step += int(last_model.split("_")[-1].split(".")[0])
                saver.restore(sess, last_model) # 変数データの読み込み
        else:
            # ディレクトリの自動生成（すでにある場合は再帰的に消して作成）
            sess.run(tf.global_variables_initializer())
            if tf.gfile.Exists("model/"):
                tf.gfile.DeleteRecursively("model/")
                print("removed model dir")
            tf.gfile.MakeDirs("model/")
            print("made model dir")


        for i in range(step+1,step+20001):
            batch = mnist.train.next_batch(50)
            if i%100 == 0:
                train_accuracy = accuracy.eval(feed_dict={
                    x:batch[0], y_: batch[1], keep_prob: 1.0})
                print("step %d, training accuracy %g"%(i, train_accuracy))
            if i%1000 == 0 and i>0:
                print("saving model/model_"+str(i)+".ckpt")
                saver.save(sess, "./model/model_"+str(i)+".ckpt")

            train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

        # 正答率の出力
        print("test accuracy %g"%accuracy.eval(feed_dict={
            x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
    elif FLAGS.run_mode == "inference":
        ckpt = tf.train.get_checkpoint_state('./model/')
        if ckpt: # checkpointがある場合
            last_model = ckpt.model_checkpoint_path # 最後に保存したmodelへのパス
            print("load " + last_model)
            saver.restore(sess, last_model) # 変数データの読み込み
        print("test accuracy %g"%accuracy.eval(feed_dict={
            x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
        print("test 1000 accuracy %g"%accuracy.eval(feed_dict={
            x: mnist.test.images[:1000], y_: mnist.test.labels[:1000], keep_prob: 1.0}))

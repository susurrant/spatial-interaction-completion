
import tensorflow as tf
import numpy as np
from func import *
from scipy import stats

def read_data(path, normalization=False):
    train_X = []
    train_y = []
    test_X = []
    test_y = []

    tr_f = read_flows(path + 'train.txt')
    te_f = read_flows(path + 'test.txt')
    if normalization:
        features = read_features(path + 'entities.dict', path + 'features.txt')
    else:
        features = read_features(path + 'entities.dict', path + 'features_raw.txt')

    for k in tr_f:
        train_y.append(k[2])
        train_X.append([features[k[0]][3], features[k[1]][2],
                        dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1])])

    for k in te_f:
        test_y.append(k[2])
        test_X.append([features[k[0]][3], features[k[1]][2],
                       dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1])])

    return np.array(train_X).reshape((-1, 3)), np.array(train_y).reshape((-1, 1)), \
           np.array(test_X).reshape((-1, 3)), np.array(test_y).reshape((-1, 1))


def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function:
        outputs = activation_function(Wx_plus_b)
    else:
        outputs = Wx_plus_b
    return outputs


if __name__ == '__main__':
    path = 'SI-GCN/data/taxi/'
    train_X, train_y, test_X, test_y = read_data(path, normalization=True)

    learn_rate = 0.005
    num_of_hidden_units = 30

    xs = tf.placeholder(tf.float32, shape = (None, 3))
    ys = tf.placeholder(tf.float32, shape = (None, 1))

    hidden_layer = add_layer(xs, 3, num_of_hidden_units, activation_function=tf.nn.sigmoid)
    prediction = add_layer(hidden_layer, num_of_hidden_units, 1, activation_function=None)

    loss = tf.losses.mean_squared_error(ys, prediction)
    train_step = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss)

    RMSE = []
    SMC = []
    MAPE = []
    real = np.array(test_y.flatten().tolist())
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        for i in range(40000):
            sess.run(train_step, feed_dict={xs: train_X, ys: train_y})
            #if i and i % 50 == 0:
                #pass
                #print('iteration', i, ':', sess.run(loss, feed_dict={xs: train_X, ys: train_y}))
                #pred = sess.run(prediction, feed_dict={xs: test_X}).flatten().tolist()
                #RMSE.append(np.sqrt(np.mean(np.square(np.array(real) - np.array(pred)))))
                #SMC.append(stats.spearmanr(np.array(real), np.array(pred))[0])

        #np.savetxt('./GNN_RMSE_'+str(num_of_hidden_units)+'.txt', np.array(RMSE), fmt='%.3f', delimiter=',')
        #np.savetxt('./GNN_SMC_'+str(num_of_hidden_units)+'.txt', np.array(SMC), fmt='%.3f', delimiter=',')

        pred = sess.run(prediction, feed_dict={xs:test_X})
        evaluate(pred.flatten().tolist(), test_y.flatten().tolist())
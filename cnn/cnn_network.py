# -*- coding: UTF-8 -*-
import numpy as np
from conv_layer import ConvLayer
from pooling_layer import PoolingLayer
from stacking_layer import StackingLayer
from fc_layer import FcLayer

# from conv_layer import IdentityActivator
from activator import ReluActivator, SoftmaxActivator


class CnnNetwork(object):
    def __init__(self, input_size, n_class=1):
        conv1 = ConvLayer(
            input_size=input_size,
            input_dim=1,
            zero_padding=2,
            stride=1,
            kernel_size=np.array([5, 5]),
            n_kernels=32,
            activator=ReluActivator())

        self.conv1 = conv1

        pool1 = PoolingLayer(
            input_size=conv1.output_size,
            input_dim=conv1.n_kernels,
            kernel_size=2,
            stride=2,
            mode='max')

        self.pool1 = pool1

        conv2 = ConvLayer(
            input_size=pool1.output_size,
            input_dim=pool1.input_dim,
            zero_padding=2,
            stride=1,
            kernel_size=np.array([5, 5]),
            n_kernels=64,
            activator=ReluActivator())
        self.conv2 = conv2

        pool2 = PoolingLayer(
            input_size=conv2.output_size,
            input_dim=conv2.n_kernels,
            kernel_size=2,
            stride=2,
            mode='max')
        self.pool2 = pool2

        stack = StackingLayer(
            input_size=pool2.output_size,
            input_dim=pool2.input_dim)
        self.stack = stack

        fc1 = FcLayer(
            input_size=stack.output_size,
            output_size=1024,
            activator=ReluActivator())
        self.fc1 = fc1

        fc2 = FcLayer(
            input_size=fc1.output_size,
            output_size=n_class,
            activator=SoftmaxActivator())
        self.fc2 = fc2
        self.layers = [conv1, pool1, conv2, pool2, stack, fc1]
        self.output_layer = fc2

    def predict_one_sample(self, x):
        output = x
        print("input:{}".format(x.shape))
        for layer in self.layers:
            output = layer.forward(output)
            print("layer:{}".format(output.shape))
        output = self.output_layer.forward(output)
        print("output:{}".format(output.shape))

        return output

    def train_one_sample(self, y, pred, learning_rate):
        delta = y - pred
        self.output_layer.delta = delta
        delta = self.output_layer.backward(delta)

        print("output delta:{}".format(delta.shape))

        for layer in reversed(self.layers):
            delta = layer.backward(delta)
            print("layer delta:{}".format(delta.shape))

        self.output_layer.update(learning_rate)
        for layer in self.layers:
            layer.update(learning_rate)


if __name__ == "__main__":
    network = CnnNetwork(input_size=np.array([28, 28]), n_class=10)
    input_array = np.random.uniform(0, 1, (1, 28, 28))

    pred = network.predict_one_sample(input_array)
    print(pred)

    print("------ train ---------")
    y = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]).reshape([10, 1])
    network.train_one_sample(y, pred, 0.01)
    print("------ train ---------")

    pred = network.predict_one_sample(input_array)
    print(pred)

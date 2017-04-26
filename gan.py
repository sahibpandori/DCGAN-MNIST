"""
GAN network that handles the training of the generator and discriminator.
"""

from util import *
from discriminator import *
from generator import *

class GAN():
    def __init__(self):
        self.g = Generator()
        self.d = Discriminator(self.g.x_fake)

        self.d_loss = tf.reduce_mean(-(tf.log(self.d.y_real) + tf.log(1 - self.d.y_fake)))
        self.d_optimizer = tf.train.AdamOptimizer(ETA).minimize(self.d_loss, var_list=self.d.params)

        self.g_loss = tf.reduce_mean(-tf.log(self.d.y_fake))
        self.g_optimizer = tf.train.AdamOptimizer(ETA).minimize(self.g_loss, var_list=self.g.params)


    def train(self, data):
        with tf.Session() as sess:
            # initialize globals
            sess.run(tf.global_variables_initializer())
            clear()

            # same random numbers for all saved samples
            z_sample = np.random.normal(0, 1, size=[1, DIM_Z])

            for epoch in range(MAX_EPOCHS):
                d_loss = 0
                g_loss = 0
                for iteration in range(TRAIN_SIZE // BATCH_SIZE):
                    # next MNIST batch
                    x_real, _= data.train.next_batch(BATCH_SIZE)
                    # because most values are 0
                    x_real = 2 * (x_real.astype(np.float32) - 0.5)
                    
                    # random input to generator
                    z = np.random.normal(0, 1, size=[BATCH_SIZE, DIM_Z]).astype(np.float32)

                    # get generator output
                    x_fake = sess.run(self.g.x_fake, feed_dict={self.g.z:z})
                    # run optimizer ops
                    _, d_loss_curr = sess.run([self.d_optimizer, self.d_loss], feed_dict={self.d.x_real:x_real, self.g.z:z})
                    _, g_loss_curr = sess.run([self.g_optimizer, self.g_loss], feed_dict={self.d.x_real:x_real, self.g.z:z})

                    d_loss += d_loss_curr
                    g_loss += g_loss_curr


                print(epoch,": ",d_loss / (TRAIN_SIZE // BATCH_SIZE + 1), g_loss / (TRAIN_SIZE // BATCH_SIZE + 1))
                sample = sess.run(self.g.x_fake, feed_dict={self.g.z:z_sample})
                save_sample(sample, SAVE_PATH % epoch)

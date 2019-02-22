import time
import tensorflow as tf

from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Flatten

from models import BaseModel


class CNNModel(BaseModel):
    @classmethod
    def variant_default(cls, x_train, y_train, x_val, y_val, params):
        model = Sequential()
        model.add(
            Conv2D(
                params["filters"],
                (params["kernel_size"], params["kernel_size"]),
                padding="same",
                activation=params["activation"],
                input_shape=x_train.shape[1:],
            )
        )

        for i in range(params["conv_modules"]):
            model.add(
                Conv2D(
                    params["filters"],
                    (params["kernel_size"], params["kernel_size"]),
                    padding="same",
                    activation=params["activation"],
                )
            )
            model.add(MaxPooling2D())
            if params["dropout"] > 0:
                model.add(Dropout(params["dropout"]))

        model.add(Flatten())
        for i in range(params["hidden_layers"]):
            model.add(
                tf.keras.layers.Dense(params["units"], activation=params["activation"])
            )

            if params["batch_norm"] > 0:
                model.add(tf.keras.layers.BatchNormalization())

            if params["dropout"] > 0:
                model.add(tf.keras.layers.Dropout(params["dropout"]))

        model.add(Dense(10, activation=params["output_activation"]))

        model.compile(
            optimizer=tf.keras.optimizers.SGD(
                lr=params["lr"], momentum=params["momentum"]
            ),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

        print(model.summary())

        history = model.fit(
            x_train,
            y_train,
            validation_data=(x_val, y_val),
            epochs=params["epochs"],
            batch_size=params["batch_size"],
            verbose=1,
            callbacks=[
                tf.keras.callbacks.TensorBoard(
                    "./logs/"
                    + "cnn_default/"
                    + "-".join("=".join((str(k), str(v))) for k, v in params.items())
                    + "-ts={}".format(str(time.time()))
                )
            ],
        )

        return history, model

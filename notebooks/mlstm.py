# %%
import pandas as pd
from keras.models import Model
from keras.layers import Input, Dense, LSTM, multiply, concatenate, Activation, Masking, Reshape
from keras.layers import Conv1D, BatchNormalization, GlobalAveragePooling1D, Permute, Dropout

# from keras_utils.training import train_model, evaluate_model, set_trainable
# from keras_utils.layers import AttentionLSTM

DATASET_INDEX = 16

MAX_TIMESTEPS = 256
MAX_NB_VARIABLES = 70
NB_CLASS = 2
TRAINABLE = True

def squeeze_excite_block(input):
    ''' Create a squeeze-excite block
    Args:
        input: input tensor
        filters: number of output filters
        k: width factor

    Returns: a keras tensor
    '''
    filters = input.shape[-1] # channel_axis = -1 for TF

    se = GlobalAveragePooling1D()(input)
    se = Reshape((1, filters))(se)
    se = Dense(filters // 16,  activation='relu', kernel_initializer='he_normal', use_bias=False)(se)
    se = Dense(filters, activation='sigmoid', kernel_initializer='he_normal', use_bias=False)(se)
    se = multiply([input, se])
    return se


# %%
df = pd.read_csv("../results/dataset.csv")
# %%

ip = Input(shape=(MAX_NB_VARIABLES, MAX_TIMESTEPS))
    # stride = 10

    # x = Permute((2, 1))(ip)
    # x = Conv1D(MAX_NB_VARIABLES // stride, 8, strides=stride, padding='same', activation='relu', use_bias=False,
    #            kernel_initializer='he_uniform')(x)  # (None, variables / stride, timesteps)
    # x = Permute((2, 1))(x)

    #ip1 = K.reshape(ip,shape=(MAX_TIMESTEPS,MAX_NB_VARIABLES))
    #x = Permute((2, 1))(ip)
x = Masking()(ip)
x = LSTM(8)(x)
x = Dropout(0.8)(x)

y = Permute((2, 1))(ip)
y = Conv1D(128, 8, padding='same', kernel_initializer='he_uniform')(y)
y = BatchNormalization()(y)
y = Activation('relu')(y)
y = squeeze_excite_block(y)

y = Conv1D(256, 5, padding='same', kernel_initializer='he_uniform')(y)
y = BatchNormalization()(y)
y = Activation('relu')(y)
y = squeeze_excite_block(y)

y = Conv1D(128, 3, padding='same', kernel_initializer='he_uniform')(y)
y = BatchNormalization()(y)
y = Activation('relu')(y)

y = GlobalAveragePooling1D()(y)

x = concatenate([x, y])

out = Dense(NB_CLASS, activation='softmax')(x)

model = Model(ip, out)
model.summary()

# %%
# model.
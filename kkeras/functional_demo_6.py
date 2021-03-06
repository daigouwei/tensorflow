# 视频问答模型
import keras
from keras import Input, Model
from keras.layers import TimeDistributed, LSTM, Dense

video_input = Input(shape=(100, 224, 224, 3))
# This is our video encoded via the previously trained vision_model (weights are reused)
encoded_frame_sequence = TimeDistributed(vision_model)(video_input) # the output will be a sequence of vectors
encoded_video = LSTM(256)(encoded_frame_sequence) # the output will be a vector

# This is a model-level representation of the question encoder, recusing the same weights as before:
question_encoder = Model(inputs=question_input, putputs=encoded_question)

# Let's use it to encode the question:
video_question_input = Input(shape=(100,), dtype='int32')
encoded_video_question = question_encoder(video_question_input)

# And this is our video question answering model:
merged = keras.layers.concatenate([encoded_video, encoded_video_question])
output = Dense(1000, activation='softmax')(merged)
video_qa_model = Model(inputs=[video_input, video_question_input], outputs=output)
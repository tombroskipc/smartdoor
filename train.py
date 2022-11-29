from recognize import load_model, train_svm_model

facenet_model = load_model('model/facenet_keras.h5')
svm_model = train_svm_model(facenet_model)
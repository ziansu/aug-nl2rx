from sklearn.model_selection import train_test_split


def process_NL_RX():
    with open('../NL-RX-Turk/src.txt', 'r') as f1, open('../NL-RX-Turk/targ.txt', 'r') as f2:
        X = f1.readlines()
        Y = f2.readlines()
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=1)
        X_train, X_valid, Y_train, Y_valid = train_test_split(X_train, Y_train, test_size=0.133333, random_state=1)
        with open('NL-RX-Turk.train.X.txt', 'w') as f:
            f.writelines(X_train)
        with open('NL-RX-Turk.train.Y.txt', 'w') as f:
            f.writelines(Y_train)
        with open('NL-RX-Turk.valid.X.txt', 'w') as f:
            f.writelines(X_valid)
        with open('NL-RX-Turk.valid.Y.txt', 'w') as f:
            f.writelines(Y_valid)
        with open('NL-RX-Turk.test.X.txt', 'w') as f:
            f.writelines(X_test)
        with open('NL-RX-Turk.test.Y.txt', 'w') as f:
            f.writelines(Y_test)

def process_StructureRegex():
    pass
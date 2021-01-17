from __future__ import print_function
import torch
import torch.nn.functional as F
import torch.optim as optim
import logging
from torch.autograd import Variable
import numpy as np

from net import Net


def load_data():
    aa = np.load("/mnist_data/party1/data.npz")
    bb = np.load("/mnist_data/party2/data.npz")

    X_test = np.vstack((aa["x_test"].astype('float32'), bb["x_test"].astype('float32')))
    Y_test = np.hstack((aa["y_test"], bb["y_test"]))

    return X_test, Y_test


def __test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            data = Variable(data.view((-1, 1, 28, 28)))
            target = Variable(target)
            output = model(data)
            test_loss += F.cross_entropy(
                output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(
                dim=1,
                keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    logging.info(
        '\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss, correct, len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))

    metrics = {
        'loss': test_loss,
        'accuracy:': (100. * correct / len(test_loader.dataset))
    }
    return metrics


def test(test_batch_size=128, no_cuda=False, seed=1, resume=''):
    """
    PyTorch MNIST Example
    output: output checkpoint filename
    batch_size: input batch size for training (default: 64)
    test_batch_size: input batch size for testing (default: 1000)
    epochs: number of epochs to train (default: 10)
    lr: learning rate (default: 1.0)
    gamma: Learning rate step gamma (default: 0.7)')
    no_cuda: disables CUDA training
    seed: random seed (default: 1)
    log_interval: how many batches to wait before logging training status
    resume: filename of resume from checkpoint
    """
    use_cuda = not no_cuda and torch.cuda.is_available()

    torch.manual_seed(seed)

    device = torch.device("cuda" if use_cuda else "cpu")

    logging.info("[MNIST] Testing data loading...")
    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

    X_test, Y_test = load_data()
    featuresTest = torch.from_numpy(X_test)
    targetsTest = torch.from_numpy(Y_test).type(torch.LongTensor)  # data type is long

    testing_data = torch.utils.data.TensorDataset(featuresTest, targetsTest)

    test_loader = torch.utils.data.DataLoader(testing_data,
                                              batch_size=test_batch_size,
                                              shuffle=True,
                                              **kwargs)
    model = Net().to(device)
    optimizer = optim.Adam(model.parameters())

    try:
        model.load_state_dict(torch.load(resume))
    except Exception as err:
        logging.info("Load resume fails [%s]", err)
        return {}
    try:
        if 'optimizaer_state_dict' in resume:
            optimizer.load_state_dict(resume['optimizer_state_dict'])
    except Exception as err:
        logging.info("Load optimizaer_state_dict fails [%s]", err)

    logging.info("[MNIST] Testing...")
    metrics = __test(model, device, test_loader)
    return metrics

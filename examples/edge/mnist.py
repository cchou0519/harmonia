from __future__ import print_function
import torch
import torch.nn.functional as F
import torch.optim as optim
import logging
from torch.autograd import Variable
import numpy as np

from net import Net


def __train(model, device, train_loader, optimizer, epoch, log_interval):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        data = Variable(data.view((-1, 1, 28, 28)))
        target = Variable(target)
        optimizer.zero_grad()
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            logging.info('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))


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


def train(output: str, batch_size=128, test_batch_size=128,
          epochs=1, lr=1.0, gamma=0.7, no_cuda=False, seed=1,
          log_interval=10, resume=''):
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

    logging.info("[MNIST] Training data loading...")
    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

    aa = np.load("/mnist_data/data.npz")

    X_train = aa["x_train"].astype('float32')
    X_test = aa["x_test"].astype('float32')

    featuresTrain = torch.from_numpy(X_train)
    targetsTrain = torch.from_numpy(aa["y_train"]).type(torch.LongTensor)  # data type is long

    featuresTest = torch.from_numpy(X_test)
    targetsTest = torch.from_numpy(aa["y_test"]).type(torch.LongTensor)  # data type is long

    training_data = torch.utils.data.TensorDataset(featuresTrain, targetsTrain)

    testing_data = torch.utils.data.TensorDataset(featuresTest, targetsTest)

    train_loader = torch.utils.data.DataLoader(training_data,
                                               batch_size=batch_size,
                                               shuffle=True,
                                               **kwargs)
    test_loader = torch.utils.data.DataLoader(testing_data,
                                              batch_size=test_batch_size,
                                              shuffle=True,
                                              **kwargs)
    model = Net().to(device)
    optimizer = optim.Adam(model.parameters())

    try:
        model.load_state_dict(torch.load(resume))
        if 'optimizaer_state_dict' in resume:
            optimizer.load_state_dict(resume['optimizer_state_dict'])
        if 'epoch' in resume:
            epoch = resume['epoch']
        train_loader = torch.utils.data.DataLoader(training_data,
                                                   batch_size=batch_size,
                                                   shuffle=True,
                                                   **kwargs)
    except Exception as err:
        logging.info("Load resume fails [%s]", err)

    logging.info("[MNIST] Training...")
    model.train()

    metrics = {}
    for epoch in range(1, epochs + 1):
        __train(model, device, train_loader, optimizer, epoch, log_interval)
        metrics = __test(model, device, test_loader)

    logging.info("[MNIST] Save Weights... [{}]".format(output))
    torch.save(model.state_dict(), output)
    return metrics

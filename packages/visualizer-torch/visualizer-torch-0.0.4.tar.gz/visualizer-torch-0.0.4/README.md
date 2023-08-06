This module is designed to help you visualize pytorch model

Example usage:
    from Visualizer import Visualizer
    from ExampleNet import ExampleNet

    vis = Visualizer()

    model = ExampleNet()  # the model you want to visualize

    params = vis._get_learnable_parts(model)
    print(params)
    # Out[]: <generator object Visualizer._get_learnable_parts at 0x00000262852F3740>

    for param, name in params:
        print(param, "\t", name)

    # Out[]:
    # Conv2d(1, 8, kernel_size=(5, 5), stride=(1, 1))                            ExampleNet.0.Conv2d.seq_block.Conv2d
    # MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False) ExampleNet.1.MaxPool2d.seq_block.MaxPool2d
    # ReLU(inplace=True)                                                         ExampleNet.2.ReLU.seq_block.ReLU
    # Conv2d(8, 16, kernel_size=(5, 5), stride=(1, 1))                           ExampleNet.3.Conv2d.seq_block.Conv2d
    # MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False) ExampleNet.4.MaxPool2d.seq_block.MaxPool2d
    # ReLU(inplace=True)                                                         ExampleNet.5.ReLU.seq_block.ReLU
    # Linear(in_features=144, out_features=72, bias=True)                        ExampleNet.0.Linear.fc.Linear
    # Linear(in_features=72, out_features=10, bias=True)                         ExampleNet.1.Linear.fc.Linear

Example usage in a loop:
    from Visualizer import Visualizer
    from ExampleNet import ExampleNet

    vis = Visualizer()

    model = ExampleNet()  # the model you want to visualize

    (...)
    for ep in range(epochs):
        (...)
        vis.visualize_loop(ep, model, total_loss=total_loss, other_params={"Some param": ["some_value"]})
    vis.close_writer()

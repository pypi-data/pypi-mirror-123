from torch.utils.tensorboard import SummaryWriter


class Visualizer:
    def __init__(self, model=None, name=None):
        self.tb = SummaryWriter()
        if model is not None:
            self.model = model
        if name is not None:
            self.model_name = name

    def visualize_loop(self, epoch: int, model=None, total_loss=None, total_correct=None, accuracy=None,
                       other_params: dict = None):
        """
        :param epoch: epoch number
        :param model: the model you want to visualize, if None then the class one will be used
        :param total_loss: scalar for tensorboard
        :param total_correct: scalar for tensorboard
        :param accuracy:  scalar for tensorboard
        :param other_params: a list containing other parameters to add as scalars
        :return SummaryWriter instance, use it to close the writer when loop is over
        example usage in README.md
        """
        if total_loss is not None:
            self.tb.add_scalar("Loss", total_loss, epoch)
        if total_correct is not None:
            self.tb.add_scalar("Correct", total_correct, epoch)
        if accuracy is not None:
            self.tb.add_scalar("Accuracy", accuracy, epoch)
        if other_params is not None:
            for param in other_params:
                self.tb.add_scalar(param, other_params[param])

        net = model if model is not None else self.model
        learnable_parts = self._get_learnable_parts(net)
        for part, name in learnable_parts:
            self.tb.add_histogram(name, part, epoch)

    def close_writer(self):
        self.tb.close()

    def _flatten_model(self, modules, start_name):
        def flatten_list(_2d_list):
            flat_list = []
            for element in _2d_list:
                if type(element) is list:
                    for item in element:
                        flat_list.append(item)
                else:
                    flat_list.append(element)
            return flat_list

        ret = []
        names = []
        if str(modules._modules.items()) == "odict_items([])":  # so its an element and not a struct
            ret.append(modules)
            names = [start_name]
        else:
            for name, n in modules._modules.items():
                r, o = self._flatten_model(n, start_name)
                ret.append(r)
                names.append(
                    [x + "." + name + "." + str(r[o.index(x)].__class__).split(".")[-1].replace("'>", "") for x in o])

        return flatten_list(ret), flatten_list(names)

    def _get_learnable_parts(self, net, get_weights=True, basename=None):
        if basename is None:
            basename = str(net.__class__).split(".")[-1].replace("'>", "")
        parts, names = self._flatten_model(net, basename)
        for p in parts:
            if not get_weights:
                yield p, names[parts.index(p)]
            else:
                try:
                    yield p.bias, names[parts.index(p)] + ".bias"
                    yield p.weight, names[parts.index(p)]
                except:
                    pass

    def flatten_model(self):
        return self._flatten_model(self.model, self.model_name)

    def get_learnable_parts(self, use_name=None):
        if use_name is None:
            return self._get_learnable_parts(self.model, self.model_name)
        else:
            return self._get_learnable_parts(self.model, use_name)

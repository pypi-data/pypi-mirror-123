# ------------------------------------------------------------------------------
#  MIT License
#
#  Copyright (c) 2021 Hieu Pham. All rights reserved.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# ------------------------------------------------------------------------------

from copy import copy
from typing import Union, Dict
from cerebro.refactoring.datastructs.trees import Tree


class Component(Tree):
    """
    Compose objects into tree structures and then work with these structures
    as if they were individual objects.
    ---------
    @author:    Hieu Pham.
    @created:   15.10.2021.
    @updated:   17.10.2021.
    """

    def __init__(self, prior: int = 1, sociable: bool = True, **kwargs):
        """
        Create new instance.
        :param prior:       priority of process.
        :param sociable:    update result from mates.
        :param kwargs:      keyword arguments.
        """
        super().__init__(**kwargs)
        self.prior = prior
        self.sociable = sociable

    def __call__(self, *args, **kwargs) -> Union[None, dict]:
        """
        Override call function treats object instance as callable function.
        :param args:    arguments to be passed.
        :param kwargs:  keyword arguments to be passed.
        :return:        result data.
        """
        inputs = copy(kwargs)
        if self.prior < 0:
            kwargs.update(self.process(**kwargs))
        for child in self._children:
            kwargs.update(child(**kwargs) if child.sociable else child(**inputs))
        if self.prior > 0:
            kwargs.update(self.process(**kwargs))
        return kwargs

    def process(self, **kwargs) -> Union[None, Dict]:
        """
        Applies processing steps.
        :param kwargs:  keyword arguments.
        :return:        result data.
        """
        return None

    def data(self, **kwargs) -> dict:
        """
        Get object data.
        :param kwargs:  keyword arguments.
        :return:        object data.
        """
        data = {'prior': self.prior, 'sociable': self.sociable}
        data.update(super().data(**kwargs))
        return data

    def attach(self, children=None, **kwargs):
        """
        Attach other components.
        :param children:    children component(s) to be attached.
        :param kwargs:      additional keyword arguments to be passed.
        :return:            children component(s).
        """
        # Attach single component.
        if children is None or isinstance(children, Component):
            return super().attach(children, **kwargs)
        # Attach list of components.
        elif isinstance(children, list):
            return [self.attach(child, **kwargs) for child in children]
        # Raise error if children is not valid.
        raise TypeError('Component can only attach component(s).')

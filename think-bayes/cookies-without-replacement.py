"""# 2.8  Exercises #
http://www.greenteapress.com/thinkbayes/html/thinkbayes003.html#sec25

## Exercise 1 ##

In Section 2.3 I said that the solution to the cookie problem
generalizes to the case where we draw multiple cookies with
replacement.  But in the more likely scenario where we eat the cookies
we draw, the likelihood of each draw depends on the previous draws.

Modify the solution in this chapter to handle selection without
replacement. Hint: add instance variables to Cookie to represent the
hypothetical state of the bowls, and modify Likelihood
accordingly. You might want to define a Bowl object.

### Notes ###

Code modified from ThinkBayes2/code/cookie3.py -- cookie3.py was
already a solution to the exercise, which I didn't immediately
realize. Ended up learning about the Hist class and reading
thinkbayes2.py and wrote the solution I would have anyway. The
original solution (in cookie3.py) mutated state in Likelihood, but
this method should not have side-effects because it's used to
Normalize, which should be idempotent.

Future Work -- What if the framework was fundamentally functional
instead of assuming iterative mutation (e.g. `suite.Update` would
return a new Suite)?

"""

from __future__ import print_function, division

import thinkbayes2

class Bowl(thinkbayes2.Hist):
    """Use Hist to represent the content of a bowl."""

class Cookie(thinkbayes2.Suite):
    """Suite to represent bowls of cookies."""

    def __init__(self, *args, **kwargs):
        super(Cookie, self).__init__(*args, **kwargs)

        # Cookies removed from the experiment are added to another
        # bowl for snacking on later.
        self.taken = Bowl({})

    def Take(self, data):
        for bowl in self.Values():
            self.AssertEnoughCookies(data, bowl)

        self.Update(data)
        self.taken.Incr(data)

    def AssertEnoughCookies(self, data, hypo):
        if (hypo[data] - self.taken[data]) <= 0:
            raise ValueError('Too few `%s` cookies in the bowl for hypo=`%s`' % (data, hypo))

        if (hypo.Total() - self.taken.Total()) <= 0:
            raise ValueError('Too few total cookies in the bowl for hypo=`%s`' % (data, hypo))

    def Likelihood(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: string cookie type
        hypo: Hist of cookies
        """
        # compute the likelihood with the current bowls
        cookies = hypo[data] - self.taken[data]
        total = hypo.Total() - self.taken.Total()
        return cookies / total


def main():
    bowl1 = Bowl(dict(vanilla=30, chocolate=10))
    bowl2 = Bowl(dict(vanilla=20, chocolate=20))

    # instantiate the suite
    suite = Cookie([bowl1, bowl2])

    for cookie in ['vanilla', 'chocolate', 'vanilla']:
        suite.Take(cookie)
        print('\nAfter taking', suite.taken)
        for hypo, prob in suite.Items():
            print(hypo, prob)

if __name__ == '__main__':
    main()

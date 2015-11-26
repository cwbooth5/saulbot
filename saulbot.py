#!/usr/bin/env python

import sys
from twisted.words.protocols import irc
from twisted.internet import defer, protocol
from twisted.internet.task import react, deferLater

from pymarkovchain import MarkovChain

class SaulBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname

    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, target, msg):
        if not user or self.nickname not in msg:
            return
        sentence = self.factory.markov.generateString()
        deferLater(self.factory.reactor,
            len(sentence) / 500.0,
            self.msg, target, sentence)


class SaulBotFactory(protocol.ClientFactory):
    protocol = SaulBot

    def __init__(self, reactor, channel='', nickname=''):
        self.channel = channel
        self.nickname = nickname
        self.markov = MarkovChain("./tempchain")
        self.reactor = reactor

        with open('corpus.txt', 'r') as f:
            self.markov.generateDatabase(f.read())

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

def saulbot(reactor, argv)
    try:
        chan = argv[1]
    except IndexError:
        print "Please specify a channel name."

    # Allow for testing of the generated quips.
    if chan == 'test':
        print SaulBotFactory(reactor).markov.generateString()
        sys.exit()

    reactor.connectTCP('irc.catch22.org', 6667, SaulBotFactory(reactor, '#' + chan, 'saulbot'))
    # Return a deferred that never fires
    return defer.Deferred()

if __name__ == "__main__":
    react(main, sys.argv)

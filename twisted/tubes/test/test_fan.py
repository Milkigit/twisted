
from twisted.trial.unittest import SynchronousTestCase

from twisted.tubes.test.util import FakeFount, FakeDrain
from twisted.tubes.fan import Out


class FakeIntermediateDrain(FakeDrain):
    """
    
    """

    nextStep = FakeFount()

    def flowingFrom(self, something):
        """
        
        """
        super(FakeIntermediateDrain, self).flowingFrom(something)
        return self.nextStep



class FanOutTests(SynchronousTestCase):
    """
    Tests for L{twisted.tubes.fan.Out}
    """

    def test_outFountFlowTo(self):
        """
        L{Out.newFount}'s C{flowTo} calls C{flowingFrom} on its drain and
        returns the result.
        """
        out = Out()
        aFount = out.newFount()
        aFakeDrain = FakeIntermediateDrain()
        result = aFount.flowTo(aFakeDrain)
        self.assertIdentical(aFakeDrain.fount, aFount)
        self.assertIdentical(result, aFakeDrain.nextStep)


    def test_fanOut(self):
        """

        """
        ff = FakeFount()
        fdA = FakeDrain()
        fdB = FakeDrain()

        out = Out()
        fountA = out.newFount()
        fountB = out.newFount()
        nothing = ff.flowTo(out.drain)
        self.assertIdentical(nothing, None)

        fountA.flowTo(fdA)
        fountB.flowTo(fdB)
        ff.drain.receive("foo")

        self.assertEquals(fdA.received, ["foo"])
        self.assertEquals(fdB.received, ["foo"])


    def test_fanReceivesBeforeFountsHaveDrains(self):
        """
        
        """
        ff = FakeFount()
        fd = FakeDrain()

        out = Out()
        fount = out.newFount()

        ff.flowTo(out.drain)

        ff.drain.receive("foo")

        fount.flowTo(fd)
        self.assertEquals(fd.received, [])
        
        
    def test_oneFountPausesUpstreamFount(self):
        """
        
        """
        ff = FakeFount()
        out = Out()
        fount = out.newFount()

        ff.flowTo(out.drain)

        fount.pauseFlow()
        self.assertEquals(ff.flowIsPaused, 1)


    def test_oneFountStops(self):
        """
        
        """
        ff = FakeFount()
        out = Out()
        fountA = out.newFount()
        fountB = out.newFount()
        ff.flowTo(out.drain)

        fdA = FakeDrain()
        fdB = FakeDrain()

        fountA.flowTo(fdA)
        fountB.flowTo(fdB)

        ff.drain.receive("before")
        fdA.fount.stopFlow()
        ff.drain.receive("after")
        self.assertEqual(fdA.received, ["before"])
        self.assertEqual(fdB.received, ["before", "after"])


    def test_oneFountStopsInReceive(self):
        """
        
        """
        
    def test_outFountStartsDrains(self):
        """
        
        """
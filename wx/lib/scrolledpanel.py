#----------------------------------------------------------------------------
# Name:         scrolledpanel.py
# Author:       Will Sadkin
# Created:      03/21/2003
# Copyright:    (c) 2003 by Will Sadkin
# RCS-ID:       $Id$
# License:      wxWindows license
#----------------------------------------------------------------------------
# 12/11/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatability update.
#
# 12/21/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o wxScrolledPanel -> ScrolledPanel
#

import  wx


class ScrolledPanel( wx.ScrolledWindow ):
    """\
ScrolledPanel fills a "hole" in the implementation of wx.ScrolledWindow,
providing automatic scrollbar and scrolling behavior and the tab traversal
management that wxScrolledWindow lacks.  This code was based on the original
demo code showing how to do this, but is now available for general use
as a proper class (and the demo is now converted to just use it.)
"""
    def __init__(self, parent, id=-1,
                 pos = wx.DefaultPosition, size = wx.DefaultSize,
                 style = wx.TAB_TRAVERSAL, name = "scrolledpanel"):

        wx.ScrolledWindow.__init__(self, parent, -1,
                                  pos=pos, size=size,
                                  style=style, name=name)

        self.Bind(wx.EVT_CHILD_FOCUS, self.OnChildFocus)


    def SetupScrolling(self, scroll_x=True, scroll_y=True, rate_x=20, rate_y=20):
        """
        This function sets up the event handling necessary to handle
        scrolling properly. It should be called within the __init__
        function of any class that is derived from ScrolledPanel,
        once the controls on the panel have been constructed and
        thus the size of the scrolling area can be determined.

        """
        # The following is all that is needed to integrate the sizer and the
        # scrolled window.
        if not scroll_x: rate_x = 0
        if not scroll_y: rate_y = 0

        # Round up the virtual size to be a multiple of the scroll rate
        sizer = self.GetSizer()
        if sizer:
            w, h = sizer.GetMinSize()
            if rate_x:
                w += rate_x - (w % rate_x)
            if rate_y:
                h += rate_y - (h % rate_y)
            self.SetVirtualSize( (w, h) )
            self.SetVirtualSizeHints( w, h )

        self.SetScrollRate(rate_x, rate_y)
        wx.CallAfter(self.Scroll, 0, 0) # scroll back to top after initial events


    def OnChildFocus(self, evt):
        # If the child window that gets the focus is not visible,
        # this handler will try to scroll enough to see it.
        evt.Skip()
        child = evt.GetWindow()

        sppu_x, sppu_y = self.GetScrollPixelsPerUnit()
        vs_x, vs_y   = self.GetViewStart()
        cpos = child.GetPosition()
        csz  = child.GetSize()
        new_vs_x, new_vs_y = -1, -1

        # is it before the left edge?
        if cpos.x < 0 and sppu_x > 0:
            new_vs_x = vs_x + (cpos.x / sppu_x)

        # is it above the top?
        if cpos.y < 0 and sppu_y > 0:
            new_vs_y = vs_y + (cpos.y / sppu_y)

        clntsz = self.GetClientSize()

        # is it past the right edge ?
        if cpos.x + csz.width > clntsz.width and sppu_x > 0:
            diff = (cpos.x + csz.width - clntsz.width) / sppu_x
            new_vs_x = vs_x + diff + 1

        # is it below the bottom ?
        if cpos.y + csz.height > clntsz.height and sppu_y > 0:
            diff = (cpos.y + csz.height - clntsz.height) / sppu_y
            new_vs_y = vs_y + diff + 1

        # if we need to adjust
        if new_vs_x != -1 or new_vs_y != -1:
            self.Scroll(new_vs_x, new_vs_y)

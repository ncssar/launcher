# launcher
## NCSSAR application launcher for Windows desktop, to increase consistency, reliability, and user-friendliness

There is often confusion about 'which icon should I click' to run sartopo, or to run radiolog, or to start IAP-builder - especially when there are different users who may or may not have recent experience with the software tool in question.

We want this launcher to be prominent, but we do NOT want to take over the entire Windows desktop.  The user could choose to close the launcher, and they would still see all the necessary desktop icons as normal.  The launcher should not interfere with the Windows taskbar.

### VERY preliminary first thoughts on the GUI
(each button will show a large icon, with small text or no text; the right pane changes depending on what icon the mouse is hovering over)
![image](https://user-images.githubusercontent.com/18752102/209412397-23b953a3-2d1d-4edb-8102-7a46f90c4371.png)

This should look like a large window, taking up ~50%+ of the desktop, opening on startup.  It should contain extra-large icons for each commonly used SAR software tool.  Maybe with the icons taking up most of the area, and a right bar that shows explanation in large font when an icon is hovered - like a more prominent tooltip.

Icons to include:
- most commonly used:
  - sartopo (desktop-server vs desktop-localhost vs web - not all three exist for every computer)  Would this look like a group box of two or three icons?
  - radiolog
  - IAP-builder
- less commonly used
  - plans console
  - offline address search
  - others?


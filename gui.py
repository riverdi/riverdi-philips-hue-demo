from riverdi.displays.bt81x import ctp50
from bridgetek.bt81x import bt81x


#
# loadImage
#
def loadImage(image):
    bt81x.load_image(0, 0, image)


#
# showLogo
#
def showLogo():

    # start
    bt81x.dl_start()
    bt81x.clear_color(rgb=(0xff, 0xff, 0xff))
    bt81x.clear(1, 1, 1)

    # image
    image = bt81x.Bitmap(1, 0, (bt81x.ARGB4, 642 * 2), (bt81x.BILINEAR, bt81x.BORDER, bt81x.BORDER, 642, 144))
    image.prepare_draw()
    image.draw(((bt81x.display_conf.width - 642)//2, (bt81x.display_conf.height - 144)//2), vertex_fmt=0)

    # display
    bt81x.display()
    bt81x.swap_and_empty()


#
# showSpinner
#
def showSpinner(msg):

    # start
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)

    # text
    txt = bt81x.Text(400, 350, 30, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, msg, )
    bt81x.add_text(txt)

    # spinner
    bt81x.spinner(400, 240, bt81x.SPINNER_CIRCLE, 0)

    # display
    bt81x.display()
    bt81x.swap_and_empty()

    # wait a second - just to improve UI experience ;)
    sleep(1000)


#
# showAddrScreen
#
def showAddrScreen(ip):

    # start
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)

    # image
    image = bt81x.Bitmap(1, 0, (bt81x.ARGB4, 200 * 2), (bt81x.BILINEAR, bt81x.BORDER, bt81x.BORDER, 200, 200))
    image.prepare_draw()
    image.draw((0, 255), vertex_fmt=0)

    # text
    txt = bt81x.Text(225, 120, 29, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, "Enter IP address of HUE Bridge:", )
    bt81x.add_text(txt)
    txt.text = ip
    txt.x = 225
    txt.y = 195
    txt.font = 31
    bt81x.add_text(txt)

    # keys
    bt81x.track(450, 350, 280, 60, 0)
    bt81x.add_keys(450, 70, 280, 60, 30, 0, "123")
    bt81x.add_keys(450, 140, 280, 60, 30, 0, "456")
    bt81x.add_keys(450, 210, 280, 60, 30, 0, "789")
    bt81x.add_keys(450, 280, 280, 60, 30, 0, ".0C")

    # connect button
    btn = bt81x.Button(450, 350, 280, 60, 30, 0, "Connect")
    bt81x.tag(1)
    bt81x.add_button(btn)

    bt81x.display()
    bt81x.swap_and_empty()


#
# showAuthScreen
#
def showAuthScreen():

    # start
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)

    # image
    image = bt81x.Bitmap(1, 0, (bt81x.ARGB4, 420 * 2), (bt81x.BILINEAR, bt81x.BORDER, bt81x.BORDER, 420, 480))
    image.prepare_draw()
    image.draw((0, 0), vertex_fmt=0)

    # text
    txt = bt81x.Text(590, 220, 28, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, "Press the push-link button of the Hue", )
    bt81x.add_text(txt)
    txt.text = "bridge you want to connect to"
    txt.x = 590
    txt.y = 260
    bt81x.add_text(txt)

    # display
    bt81x.display()
    bt81x.swap_and_empty()


#
# MainMenu - buttons layout
#
buttons = [
    {
        "tag_id": 2,
        "text": "ON",
        "x_cord": 50,
        "y_cord": 200,
        "width": 170,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 3,
        "text": "OFF",
        "x_cord": 50,
        "y_cord": 300,
        "width": 170,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 4,
        "text": "ON",
        "x_cord": 280,
        "y_cord": 200,
        "width": 170,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 5,
        "text": "OFF",
        "x_cord": 280,
        "y_cord": 300,
        "width": 170,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 6,
        "text": "<",
        "x_cord": 520,
        "y_cord": 150,
        "width": 50,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 7,
        "text": "<",
        "x_cord": 520,
        "y_cord": 250,
        "width": 50,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 8,
        "text": "<",
        "x_cord": 520,
        "y_cord": 350,
        "width": 50,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 9,
        "text": ">",
        "x_cord": 675,
        "y_cord": 150,
        "width": 50,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 10,
        "text": ">",
        "x_cord": 675,
        "y_cord": 250,
        "width": 50,
        "height": 50,
        "size": 30
    },
    {
        "tag_id": 11,
        "text": ">",
        "x_cord": 675,
        "y_cord": 350,
        "width": 50,
        "height": 50,
        "size": 30
    },
]


#
# MainMenu - text labels layout
#
labels = [
    {
        "text": "Riverdi/Zerynth Lighting Demo",
        "x_cord": 400,
        "y_cord": 25,
        "size": 30,
        "options": bt81x.OPT_CENTER
    },
    {
        "text": "Kitchen",
        "x_cord": 136,
        "y_cord": 140,
        "size": 31,
        "options": bt81x.OPT_CENTER
    },
    {
        "text": "Bedroom",
        "x_cord": 364,
        "y_cord": 140,
        "size": 31,
        "options": bt81x.OPT_CENTER
    },
    {
        "text": "Saturation",
        "x_cord": 622,
        "y_cord": 130,
        "size": 28,
        "options": bt81x.OPT_CENTER
    },
    {
        "text": "Hue",
        "x_cord": 622,
        "y_cord": 230,
        "size": 28,
        "options": bt81x.OPT_CENTER
    },
    {
        "text": "Brightness",
        "x_cord": 622,
        "y_cord": 330,
        "size": 28,
        "options": bt81x.OPT_CENTER
    },
]


#
# showMainMenu
#
def showMainMenu(saturation, hue, brightness):

    # start
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)

    # image
    image = bt81x.Bitmap(1, 0, (bt81x.ARGB4, 800 * 2), (bt81x.BILINEAR, bt81x.BORDER, bt81x.BORDER, 800, 50))
    image.prepare_draw()
    image.draw((0, 0), vertex_fmt=0)

    # buttons
    btn = bt81x.Button(0, 0, 170, 70, 31, 0, "")
    for button in buttons:
        btn.text = button["text"]
        btn.font =  button["size"]
        btn.x = button["x_cord"]
        btn.y = button["y_cord"]
        btn.width =  button["width"]
        btn.height = button["height"]
        bt81x.track(btn.x, btn.y,  button["width"],  button["height"], button["tag_id"])
        bt81x.tag(button["tag_id"])
        bt81x.add_button(btn)

    # text labels
    txt = bt81x.Text(0, 0, 0, 30, "")
    for label in labels:
        txt.text = label["text"]
        txt.x = label["x_cord"]
        txt.y = label["y_cord"]
        txt.font = label["size"]
        txt.options = label["options"]
        bt81x.add_text(txt)

    # saturation value label
    txt.text = str(int((saturation/240)*100)) + '%'
    txt.x = 622
    txt.y = 175
    txt.font = 30
    txt.options = bt81x.OPT_CENTER
    bt81x.add_text(txt)

    # hue value label
    txt.text = str(int((hue/65500)*100)) + '%'
    txt.x = 622
    txt.y = 275
    txt.font = 30
    txt.options = bt81x.OPT_CENTER
    bt81x.add_text(txt)

    # brightness value label
    txt.text = str(int((brightness/240)*100)) + '%'
    txt.x = 622
    txt.y = 375
    txt.font = 30
    txt.options = bt81x.OPT_CENTER
    bt81x.add_text(txt)

    # display
    bt81x.display()
    bt81x.swap_and_empty()

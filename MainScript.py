# tetris game

# default canvas = 400 pixels
# default height = 300 pixels

import turtle
import time
import os
import random



#print(all(x == a[0] for x in a))

screenWidth = 700
screenHeight = 700
gameWidth = 300
gameHeight = 600

# block positions
posx_arr = []
posy_arr = []
for x in range(4):
    posx_arr.append(0)
for y in range(4):
    posy_arr.append(0)

# difficulty
speed = 0.5
speedHolder = 0.5
level = 1
levelTimeHolder = 10
levelTimeVariable = levelTimeHolder

# controls
horizontal_movement = 0

# time stuff
startingTime = 0
endingTime = 0
timeMeasured = speed


# conditional statements
passTheBlocks = True
rePositionBlocks = False
touchGround = False
gameStart = False
gamePause = False
shapeGround = ""
checkFilledLines = []
for i in range(20):
    checkFilledLines.append(0)
drawingInfo = []
for i in range(20):
    drawingInfo.append([])
    for j in range(10):
        drawingInfo[i].append("none")

        
# gameplay
score = 0
shapes = {
    0 : "O", 1 : "I", 2 : "S",
    3 : "Z", 4 : "L", 5 : "J",
    6 : "T"    
        }
currentShape = shapes[random.randrange(7)]
prev1 = shapes[random.randrange(7)]
prev2 = shapes[random.randrange(7)]
colors = {
    "O" : "gold", "I" : "lightblue", "S" : "red",
    "Z" : "green", "L" : "orange", "J" : "pink",
    "T" : "purple"
        }

screen = turtle.Screen()
screen.bgcolor("gray")
screen.setup(screenWidth, screenHeight)
screen.tracer(4)

# for drawing at the bottom                     # DRAW AT THE BOTTOM
rowTurtles = []
for row in range(20):
    rowTurtles.append(turtle.Turtle())
    rowTurtles[row].penup()
    rowTurtles[row].hideturtle()
    rowTurtles[row].color("white")

# setup area drawing turtle and draw gaming screen
areaPen = turtle.Turtle()
areaPen.hideturtle()
areaPen.width(5)
areaPen.color("white")
areaPen.speed(0)
areaPen.penup()
areaPen.setpos(-gameWidth/2, gameHeight/2)
areaPen.pendown()
areaPen.begin_fill()
for side in range(2):
    areaPen.forward(gameWidth)
    areaPen.right(90)
    areaPen.forward(gameHeight)
    areaPen.right(90)
areaPen.color("black")
areaPen.end_fill()
areaPen.penup()


# DEFINING TURTLE BLOCK SHAPES
blocks = []
for b in range(4):
    blocks.append(turtle.Turtle())
    blocks[b].hideturtle()
    blocks[b].shape("square")
    blocks[b].color("white", "lightblue")
    blocks[b].shapesize(1.5, 1.5, 3)
    blocks[b].speed(0)
    blocks[b].penup()
    
#levelpen stuff
levelPen = turtle.Turtle()
levelPen.penup()
levelPen.hideturtle()
levelPen.width(3)
levelPen.color("white")
levelPen.setpos(-50, 310)
levelPen.write("Level " + str(level), align = "Left", font=("Arial", 20))

#scorepen stuff
scorePen = turtle.Turtle()
scorePen.penup()
scorePen.hideturtle()
scorePen.width(3)
scorePen.color("gold")
scorePen.setpos(200, 20)
scorePen.write("Score \n" + str(score), align= "Left", font = ("Arial", 25))

#FUNCTIONS
# To do position indexing
def block_position(r, c):                   # PIXEL CONVERSION
    x = -135
    y = 285
    x += (c*30)
    y -= (r*30)
    return x, y


def pixelToBlock(posx, posy):               # BLOCK CONVERSION
    c = (posx+135)/30
    r = abs(posy-285)/30
    return r, c

# Define ground for each column             # DEFINING GROUND
groundRows = []
for gr in range(10):
    groundRows.append([])
    tempx, tempy = block_position(19, gr)
    groundRows[gr].append(tempx)
    groundRows[gr].append(tempy)
    
# To spawn shapes on top
def spawn_shape(letter):                    # SPAWN SHAPES
    global shapeGround
    global posx_arr, posy_arr
    if letter == "O":
        a1, b1, c1, d1 = 0, 0, 1, 1
        a2, b2, c2, d2 = 4, 5, 4, 5
        shapeGround = "23"
    elif letter == "I": 
        a1, b1, c1, d1 = 0, 1, 2, 3
        a2, b2, c2, d2 = 4, 4, 4, 4
        shapeGround = "3"
    elif letter == "S":
        a1, b1, c1, d1 = 0, 0, 1, 1
        a2, b2, c2, d2 = 4, 5, 3, 4
        shapeGround = "23"
    elif letter == "Z":
        a1, b1, c1, d1 = 0, 0, 1, 1
        a2, b2, c2, d2 = 4, 5, 5, 6
        shapeGround = "23"
    elif letter == "L":
        a1, b1, c1, d1 = 0, 1, 2, 2
        a2, b2, c2, d2 = 4, 4, 4, 5 
        shapeGround = "23"
    elif letter == "J":
        a1, b1, c1, d1 = 0, 1, 2, 2
        a2, b2, c2, d2 = 5, 5, 4, 5 
        shapeGround = "23"
    else:
        a1, b1, c1, d1 = 0, 0, 0, 1
        a2, b2, c2, d2 = 3, 4, 5, 4 
        shapeGround = "032"
    posx_arr[0], posy_arr[0] = block_position(a1,a2)
    posx_arr[1], posy_arr[1] = block_position(b1,b2)
    posx_arr[2], posy_arr[2] = block_position(c1,c2)
    posx_arr[3], posy_arr[3] = block_position(d1,d2)

        
        
def rotate_shape():                             # ROTATE SHAPES
    global shapeGround
    global currentShape
    global posx_arr, posy_arr
    r1, c1 = pixelToBlock(posx_arr[0], posy_arr[0])
    r2, c2 = pixelToBlock(posx_arr[1], posy_arr[1])
    r3, c3 = pixelToBlock(posx_arr[2], posy_arr[2])
    r4, c4 = pixelToBlock(posx_arr[3], posy_arr[3])
    if currentShape == "I":
        if r1 == r4:
            r1, r3, r4 = r1-1, r3+1, r4+2
            c1, c3, c4 = c1+1, c3-1, c4-2
            shapeGround = "3"
        else:
            r1, r3, r4 = r1+1, r3-1, r4-2
            c1, c3, c4 = c1-1, c3+1, c4+2
            shapeGround = "0123"
    elif currentShape == "S":
        if r1 == r2:
            r1, r3 = r1-1, r3-1
            c1, c2, c3 = c1-1, c2-2, c3+1
            shapeGround = "31"
        else:
            r1, r3 = r1+1, r3+1
            c1, c2, c3 = c1+1, c2+2, c3-1
            shapeGround = "23"
    elif currentShape == "Z":
        if r1 == r2:
            r1, r3 = r1-1, r3-1
            c1, c3, c4 = c1+2, c3+1, c4-1
            shapeGround = "32"
        else:
            r1, r3 = r1+1, r3+1
            c1, c3, c4 = c1-2, c3-1, c4+1
            shapeGround = "23"
    elif currentShape == "L":
        if c1 == c3:
            r1, r3 = r1+1, r3-1
            c1, c3, c4 = c1-1, c3+1, c4-2
            shapeGround = "312"
        elif r1 == r3:
            r1, r2 = r1-1, r2-1
            c3, c4 = c3-1, c4+1
            shapeGround = "03"
        elif c2 == c4:
            r2, r4 = r2+1, r4-1
            c1, c2, c4 = c1+2, c2-1, c4+1
            shapeGround = "123"
        else:
            r3, r4 = r3+1, r4+1
            c1, c2 = c1-1, c2+1
            shapeGround = "23"
    elif currentShape == "J":
        if c2 == c4:
            r3, r4 = r3-1, r4-1
            c1, c2, c3, c4 = c1-1, c2-1, c3+1, c4+1
            shapeGround = "123"
        elif c1 == c2:
            r2, r4 = r2-1, r2+1
            c1, c2, c4 = c1+1, c2+2, c4-1
            shapeGround = "31"
        elif c1 == c3:
            r1, r2 = r1+1, r2+1
            c1, c2, c3, c4 = c1-1, c2-1, c3+1, c3+1
            shapeGround = "013"
        else:
            r1, r3 = r1-1, r3+1
            c1, c3, c4 = c1+1, c3-2, c4-1
            shapeGround = "23"
    elif currentShape == "T":
        if r1 == r2:
            r1 = r1-1
            c1, c2, c3 = c1+1, c2-1, c3-1
            shapeGround = "13"
        elif c3 == c4:
            r4, c4 = r4-1, c4+1
            shapeGround = "123"
        elif c1 == c3:
            r4 = r4+1
            c2, c3, c4 = c2+1, c3+1, c4-1
            shapeGround = "32"
        else:
            r1, c1 = r1+1, c1-1
            shapeGround = "032"
            
    while c1 > 9 or c2 > 9 or c3 > 9 or c4 > 9:         # boundary checking
        c1, c2, c3, c4 = c1-1, c2-1, c3-1, c4-1
        
    while c1 < 0 or c2 < 0 or c3 < 0 or c4 < 0:
        c1, c2, c3, c4 = c1+1, c2+1, c3+1, c4+1
    
    while r1 > 19 or r2 > 19 or r3 > 19 or r4 > 19:
        r1, r2, r3, r4 = r1-1, r2-1, r3-1, r4-1
        
    posx_arr[0], posy_arr[0] = block_position(r1,c1)
    posx_arr[1], posy_arr[1] = block_position(r2,c2)
    posx_arr[2], posy_arr[2] = block_position(r3,c3)
    posx_arr[3], posy_arr[3] = block_position(r4,c4)
    
    
    
def draw_bottom(rows, cols, color):                 # BOTTOM DRAWING
    global score
    global groundRows, rePositionBlocks
    global checkFilledLines, drawingInfo
    checkRows = list(set(rows))
    
    for each in range(4):
        checkFilledLines[rows[each]] += 1
        drawingInfo[rows[each]][cols[each]] = color 

        centerx, centery = block_position(rows[each], cols[each])
        startx = centerx - 15
        starty = centery + 15
        rowTurtles[rows[each]].setpos(startx, starty)
        rowTurtles[rows[each]].color("white")
        rowTurtles[rows[each]].width(3)
        rowTurtles[rows[each]].pendown()
        rowTurtles[rows[each]].begin_fill()
        for side in range(4):
            rowTurtles[rows[each]].forward(30)
            rowTurtles[rows[each]].right(90)
        rowTurtles[rows[each]].color(color)
        rowTurtles[rows[each]].end_fill()
        rowTurtles[rows[each]].penup()
        
    # assing new ground values
    diffcols = list(set(cols))
    colIndexes = []
    for col in diffcols:    
        colIndexes.append([i for i, e in enumerate(cols) if e == col])
    lowestRows = []
    tempValue = 0
    for d1 in range(len(colIndexes)):
        for d2 in range(len(colIndexes[d1])):
            if d2 == 0:
                tempValue = rows[colIndexes[d1][d2]]
            if rows[colIndexes[d1][d2]] < tempValue:
                tempValue = rows[colIndexes[d1][d2]]
        lowestRows.append(tempValue)  
        # diffcols and lowestrows
    for c in range(len(diffcols)):
        tempxvalue1, tempyvalue1 = block_position(lowestRows[c]-1, diffcols[c])
        tempxvalue = int(tempxvalue1)
        tempyvalue = int(tempyvalue1)
        if tempyvalue > groundRows[diffcols[c]][1]:
            groundRows[diffcols[c]][0] = tempxvalue
            groundRows[diffcols[c]][1] = tempyvalue
    # clean up with score
    firstAssign = True 
    temp1 = 0
    temp2 = 0
    for row in checkRows:
        if checkFilledLines[row] == 10:
            rePositionBlocks = True
            if firstAssign == True:             # this is for assigning 
                firstAssign = False             # bottom and top filled, deleted lines
                temp1 = row
                temp2 = row
            if row > temp1:         
                temp1 = row
            if row < temp2:
                temp2 = row
            checkFilledLines[row] -= 10
            for index in range(10):
                groundRows[index][1] -= 30
                drawingInfo[row][index] = "none"
            rowTurtles[row].clear()
    if rePositionBlocks == True and temp1 != 19:
        for checkingRow in range(temp1+1, 20):
            if "none" in drawingInfo[checkingRow]:
                for scanIndex in range(10):
                    if drawingInfo[checkingRow][scanIndex] == "none":
                        groundRows[scanIndex][1] -= 30
    
    firstAssign = True
    
    # shift the drawings
    dataIndex = temp2-1                 # that will decrease with each iteration
    shift = 0
    while rePositionBlocks:
        if drawingInfo[dataIndex][0] == "none":
            if all(x == drawingInfo[dataIndex][0] for x in drawingInfo[dataIndex]):
                rePositionBlocks = False
                break
        shift = temp1-temp2+1
        currentC = 0
        overlap = 0
        checkFilledLines[dataIndex+shift] = checkFilledLines[dataIndex]
        checkFilledLines[dataIndex] = 0
        rowTurtles[dataIndex].clear()
        for data in drawingInfo[dataIndex]:
            drawingInfo[dataIndex+shift][overlap] = drawingInfo[dataIndex][overlap]
            drawingInfo[dataIndex][overlap] = "none"
            overlap+=1
            if data == "none":
                currentC+=1
                continue
            drawX, drawY = block_position(dataIndex+shift, currentC)
            drawX-=15
            drawY+=15
            
            rowTurtles[dataIndex+shift].setpos(drawX, drawY)
            rowTurtles[dataIndex+shift].color("white")
            rowTurtles[dataIndex+shift].width(3)
            rowTurtles[dataIndex+shift].pendown()
            rowTurtles[dataIndex+shift].begin_fill()
            for side in range(4):
                rowTurtles[dataIndex+shift].forward(30)
                rowTurtles[dataIndex+shift].right(90)
            rowTurtles[dataIndex+shift].color(data)
            rowTurtles[dataIndex+shift].end_fill()
            rowTurtles[dataIndex+shift].penup() 
            currentC+=1
            
        dataIndex-=1
    if shift == 4:
        score += 50
    else:
        score += shift*10
    scorePen.clear()
    scorePen.write("Score \n" + str(score), align= "Left", font = ("Arial", 25))
    
    os.system("cls")
    for something in range(10):
        cagr, cagc = pixelToBlock(groundRows[something][0],groundRows[something][1])
        print(something, " : ", cagr)
    print("line[17]: ", checkFilledLines[17])
    print("line[18]: ", checkFilledLines[18])
    print("line[19]: ", checkFilledLines[19])
    print("shift : ", shift)
    print("temp1(bottom) : ", temp1)
    print("temp2(top)   : ", temp2)
    print()
    print("drawingInfo")
    print("17 : ", drawingInfo[17])
    print("18 : ", drawingInfo[18])
    print("19 : ", drawingInfo[19])
    print()
    print("checkrows: ", checkRows)
    print()
    print("block positions")
    print("rows : ", rows)
    print("cols : ", cols)
    

            
    
        
def move_down(s):
    global posy_arr
    for y in range(4):
        posy_arr[y] -= 30
    
def move_right():
    global posx_arr
    for x in range(4):
        if posx_arr[x] == 135:
            return
    for x in range(4):
        posx_arr[x] += 30

def move_left():
    global posx_arr
    for x in range(4):
        if posx_arr[x] == -135:
            return
    for x in range(4):
        posx_arr[x] -= 30
    
def faster():
    global speed
    speed = 0.03
def normal_speed():
    global speed, speedHolder
    speed = speedHolder
       
def hide_turtles():
    for b in range(4):
        blocks[b].hideturtle()
    
def show_turtles():
    for b in range(4):
        blocks[b].showturtle()
    
def assign_color(color):
    for b in range(4):
        blocks[b].color("white", color)

def pause_game():
    global gamePause
    gamePause = True  
def continue_game():
    global gamePause
    gamePause = False
    


turtle.listen()
turtle.onkeypress(move_left, "Left")
turtle.onkeypress(move_right, "Right")

turtle.onkeypress(faster, "Down")
turtle.onkeyrelease(normal_speed, "Down")
turtle.onkey(rotate_shape, "space")

turtle.onkey(pause_game, "p")
turtle.onkey(continue_game, "s")


#currentShape = "I"
# GAME LOOP
while True:
    
    startingTime = time.time()

    if levelTimeVariable <= 0:
        if speedHolder >= 0.06:
            speedHolder -= 0.03
            levelTimeVariable = levelTimeHolder
            level += 1
            levelPen.clear()
            levelPen.write("Level " + str(level), align = "Left", font=("Arial", 20))
    
    if touchGround == True or gameStart == False:
        
        prev2 = prev1
        prev1 = currentShape
        while currentShape == prev1 or currentShape == prev2:
            currentShape = shapes[random.randrange(7)]            
        
        spawn_shape(currentShape)
        assign_color(colors[currentShape])
        show_turtles()
        touchGround = False
        gameStart = True
    
    if timeMeasured <= 0:
        rowIndexes = []
        columnIndexes = []   
        passTheBlocks = True
        for s in shapeGround:
            s_int = int(s)
            rowIndexRaw, colIndexRaw = pixelToBlock(posx_arr[s_int], posy_arr[s_int])
            colIndex = int(colIndexRaw)
            rowIndex = int(rowIndexRaw)
            if posy_arr[s_int] == groundRows[colIndex][1]:
                touchGround = True
                speed = speedHolder
                if passTheBlocks == True:
                    for block in range(4):
                        tmprraw, tmpcraw = pixelToBlock(posx_arr[block], posy_arr[block])
                        tmpr = int(tmprraw)
                        tmpc = int(tmpcraw)
                        rowIndexes.append(tmpr)
                        columnIndexes.append(tmpc)
                    passTheBlocks = False
        if gamePause == False:             
            if touchGround == True:
                draw_bottom(rowIndexes, columnIndexes, colors[currentShape])      
            move_down(speed)
        timeMeasured = speed
    
    for b in range(4):
        blocks[b].setpos(posx_arr[b], posy_arr[b])
        
    endingTime = time.time()
    timeMeasured -= endingTime - startingTime
    levelTimeVariable -= endingTime - startingTime
    
turtle.mainloop()

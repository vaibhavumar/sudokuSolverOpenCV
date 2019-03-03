import cv2
import numpy as np
import joblib
import sudoku2

font = cv2.FONT_HERSHEY_SIMPLEX
clf = joblib.load('classifier.pkl')

is_print = True
#=====================Grid Detection===================================
ratio2 = 3
kernel_size = 3
lowThreshold = 30

cv2.namedWindow("SUDOKU Solver")
#frame = cv2.imread('sudoku2.jpg')
vc = cv2.VideoCapture(0)
if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
while rval:
    
    sudoku1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sudoku1 = cv2.blur(sudoku1, (3, 3))

    edges = cv2.Canny(sudoku1, lowThreshold, lowThreshold*ratio2, kernel_size)
    lines = cv2.HoughLines(edges, 2, np.pi/180, 300, 0, 0)
    if lines is not None:
        #lines = lines[0]
        #lines = sorted(lines, key=lambda lines:lines[0])
        lines = sorted(lines, key = lambda line:line[0][0])
        pos_hori = 0
        pos_vert = 0
        New_lines = []
        Points = []
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                if b > 0.5:
                    if rho-pos_hori > 10:
                        pos_hori = rho
                        cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
                        New_lines.append([rho, theta, 0])
                else:
                    if rho-pos_vert > 10:
                        pos_vert = rho
                        cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
                        New_lines.append([rho, theta, 1])
        for i in range(len(New_lines)):
            if(New_lines[i][2] == 0):
                for j in range(len(New_lines)):
                    if (New_lines[j][2]==1):
                        theta1=New_lines[i][1]
                        theta2=New_lines[j][1]
                        p1=New_lines[i][0]
                        p2=New_lines[j][0]
                        xy = np.array([[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]])
                        p = np.array([p1,p2])
                        res = np.linalg.solve(xy, p)
                        Points.append(res)
        if(len(Points)==100):
            result = []
            board = []
            sudoku1 = cv2.adaptiveThreshold(sudoku1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 101, 1)
            for i in range(0,9):
                for j in range(0,9):
                    y1=int(Points[j+i*10][1]+5)
                    y2=int(Points[j+i*10+11][1]-5)
                    x1=int(Points[j+i*10][0]+5)
                    x2=int(Points[j+i*10+11][0]-5)

                    X = sudoku1[y1:y2,x1:x2]
                    if(X.size!=0):
                        X = cv2.resize(X,(36,36))
                        num = clf.predict(np.reshape(X, (1, -1)))

                        result.append(num)
                        board.append(num)
                        #if (num[0] != 0):
                         #   cv2.putText(frame,str(num[0]),(int(Points[j+i*10+10][0]+10), int(Points[j+i*10+10][1]-30)),font,1,(225,0,0),2)
                        #else:
                          #  cv2.putText(frame,str(num[0]),(int(Points[j+i*10+10][0]+10), int(Points[j+i*10+10][1]-15)),font,1,(225,0,0),2)
                    # Saving extracted block for training, uncomment for saving digit blocks
                    #cv2.imwrite(str((i+1)*(j+1))+".jpg", sudoku1[y1: y2,
                    #                                            x1: x2])
                    #cv2.rectangle(frame,(x1,y1),(x2, y2),(0,255,0),2)
            result = np.reshape(result, ( 9,9))
            board = np.reshape(board,(9,9))
            print("CHECKING SUDOKU")
            print(result)
            if sudoku2.randomised_sudokuSolver(result):
                print(result)
                for i in range(0,9):
                    for j in range(0,9):
                        if board[i][j] == 0:
                            cv2.putText(frame,str(result[i][j]),(int(Points[j+i*10+10][0]+15), int(Points[j+i*10+10][1]-10)),font,1,(225,0,0),2)
            cv2.imshow("Result", frame)
        

    cv2.imshow("SUDOKU Solver", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:
        break
vc.release()
cv2.destroyAllWindows()
#========================END OF GRID DETECTION======================================
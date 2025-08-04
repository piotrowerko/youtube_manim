︠2d3bc539-a879-4b1f-bac2-21a749a1f52bs︠
x = var('x')
y = var('y')
h = var('h')
Q1 = var('Q1')
Q2 = var('Q2')
Q3 = var('Q3')
Q4 = var('Q4')
Q5 = var('Q5')
Q6 = var('Q6')
Q7 = var('Q7')
Q8 = var('Q8')
Q9 = var('Q9')
Q10 = var('Q10')
Q11 = var('Q11')
Q12 = var('Q12')
R1 = var('R1')
R2 = var('R2')
R11 = var('R11')
R12 = var('R12')
a = var('a')
b = var('b')
print("..............................................................PROSTOKAT:............................................................................")
print("PRZYJMUJE UKLAD LOKALNY ZACZEPIONY SRODKU GEOMETRYCZNYM PROSTOKATA !")
print("Wymiary prostokata:")
a=2
b=3
a
b
print("")
print("Grubosc prosokata:")
h=0.15.n(prec=15)
h
print("")
print("Funkcje kształtu prostokata:")
Ni =1/4 * (1-2*x/ a) * (1-2*y/ b)
Nj =1/4 * (1+2*x/ a) * (1-2*y/ b)
Nk =1/4 * (1+2*x/ a) * (1+2*y/ b)
Nr =1/4 * (1-2*x/ a) * (1+2*y/ b)
Ni
Nj
Nk
Nr
print("")
print("Macierz funkcji kształtu prostokata:")
N1=matrix(2, 8, [Ni,0,Nj,0,Nk,0,Nr,0, 0,Ni,0,Nj,0,Nk,0,Nr])
N1
print("Pochodne funkcji kształtu prostokata:")
diff(Ni, x)
diff(Ni, y)
diff(Nj, x)
diff(Nj, y)
diff(Nk, x)
diff(Nk, y)
diff(Nr, x)
diff(Nr, y)
print("B: Iloczyn macierzy operatorów różniczkowych i funkcji kształtu:")
Bpio=matrix(3, 8, [diff(Ni, x),0,diff(Nj, x),0,diff(Nk, x),0,diff(Nr, x),0, 0,diff(Ni, y),0,diff(Nj, y),0,diff(Nk, y),0,diff(Nr, y), diff(Ni, y),diff(Ni, x),diff(Nj, y),diff(Nj, x),diff(Nk, y),diff(Nk, x),diff(Nr, y),diff(Nr, x)])
Bpio
Bpio.parent()
print("Transponowana B:")
Bpio.transpose()
BpioT=Bpio.transpose()
BpioT.parent()
Dpio=matrix(3, 3, [85.5,29.9,0, 29.9,85.5,0, 0,0,27.8])
print("D: Macierz sprężystoci- PODAJE W GPa !!:")
Dpio
Dpio.parent()
print("Bt*D*B*h:")
Bpio.transpose()*Dpio*Bpio*h
Docalki=Bpio.transpose()*Dpio*Bpio*h*1000000
Ksztel1=Docalki.apply_map(lambda e: integrate(integrate(e,x,-1,1), y,-1.5,1.5))
print("Macierz sztywności el. nr 1 (prostokat)- podwójna całka oznaczona z Bt*D*B*h*10^6:")
Ksztel1
print("")
print("Topel1: Macierz topologii elementu nr 1 (prostokat)")
print("liczba kolumn = liczba stopni swobody danego el.")
print("liczba wierszy = liczba stopni swobody całej struktury MES")
Topel1=matrix(12, 8, [0,0,1,0,0,0,0,0, 0,0,0,1,0,0,0,0, 0,0,0,0,1,0,0,0, 0,0,0,0,0,1,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,1,0,0,0,0,0,0,])
Topel1
print("")
Topel1T=Topel1.transpose()
print("")
print("Topel1T: Macierz transponowana topologii elementu nr 1 (prostokat)")
Topel1T
print("Ksztel1GUW: Macierz sztywności elementu nr 1 (prostokat) w GUW")
Ksztel1GUW=Topel1*Ksztel1*Topel1T
Ksztel1GUW
print("")
print("")

print(".................................................................TROJKAT - el. II:.............................................................................")
print("")
print("PRZYJMUJE UKLAD LOKALNY ZACZEPIONY W LEWYM DOLNYM WEZLE TROJKATA !")
print("")
ht = var('ht')
xi = var('xi')
yi = var('yi')
xj = var('xj')
yj = var('yj')
xk = var('xk')
yk = var('yk')
print("")
print("Macierz 'A' - skladowa iloczynu zmiennych z trojkta Pascala oraz niewiadomych wielomianu aproksymujacego:")
print("Macierz 'A' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)")
print("Macierz 'A' licza wierszy = liczba wspolrzednych stosowanego ukladu = liczba niewiadomych pojedynczego wezla")
A=matrix(2, 6, [1,x,y,0,0,0, 0,0,0,1,x,y])
print("A=")
A
print("")
print("Macierz 'Aw' - skladowa iloczynu zmiennych z projkta Pascla oraz niewiadomych wielomianu aproksymujacego po podstawieniu do A wspolrzednych wezlow:")
print("Macierz 'Aw' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)")
print("Macierz 'Aw' licza wierszy = liczba stopni swobody calego elementu")
Aw=matrix(6, 6, [1,xi,yi,0,0,0, 0,0,0,1,xi,yi, 1,xj,yj,0,0,0, 0,0,0,1,xj,yj, 1,xk,yk,0,0,0, 0,0,0,1,xk,yk])
print("Aw=")
Aw
print("")
print("Macierz 'N2' - Macierz funkcji kształtu")
print("Macierz 'N2' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)")
print("Macierz 'N2' licza wierszy = liczba wspolrzednych stosowanego ukladu = liczba niewiadomych pojedynczego wezla")
print("[N2]=[A]*([Aw]^-1)")
Awi=Aw.inverse()
N2=A*Awi
print("N2=")
N2
ht=0.15
xi = 0
yi = 0
xj = -2
yj = -2
xk = 0
yk = -2
A=matrix(2, 6, [1,x,y,0,0,0, 0,0,0,1,x,y])
Aw=matrix(6, 6, [1,xi,yi,0,0,0, 0,0,0,1,xi,yi, 1,xj,yj,0,0,0, 0,0,0,1,xj,yj, 1,xk,yk,0,0,0, 0,0,0,1,xk,yk])
Awi=Aw.inverse()
N2=A*Awi
print("")
print("N2 po podstawieniu=")
N2
print("")
print("Wyprowadzenie macierzy sztywności trojkata plaskiego:")
print("")
Nit=N2[1,1]
Njt=N2[1,3]
Nkt=N2[1,5]
print("Funcje kształtu (na podstawie wcześniej podanych wspolrzednych wezlow):")
Nit
Njt
Nkt
print("")
print("B- Iloczyn macierzy operatorów różniczkowych i funkcji kształtu:")
Bpiot=matrix(3, 6, [diff(Nit, x),0,diff(Njt, x),0,diff(Nkt, x),0, 0,diff(Nit, y),0,diff(Njt, y),0,diff(Nkt, y), diff(Nit, y),diff(Nit, x),diff(Njt, y),diff(Njt, x),diff(Nkt, y),diff(Nkt, x)])
Bpiot
print("")
print("D- Macierz sprężystości - PODAJE W GPa !!:")
Dpiot=matrix(3, 3, [85.5,29.9,0, 29.9,85.5,0, 0,0,27.8])
Dpiot
print("")
print("Transponowana B:")
Bpiot.transpose()
print("")
print("Bt*B*D*h:")
Docalkit=Bpiot.transpose()*Dpiot*Bpiot*ht*1000000
Docalkit
print("sprawdz:")
Sprawdzjaca=Docalkit*2
Sprawdzjaca
print("jak widać iloczyn Bt*B*D*h w trójkacie jest macierza samych liczb !")
print("")
Kszte2=Docalkit.apply_map(lambda e: integrate(integrate(e,y,-2,x), x,-2,0)) #to zakres calkowania zewnetrznej calki jest od -2 do x gdyz w elemencie trojkatnym w zadaniu ograniczenie z gory jest funkcja y=x !!
print("Macierz sztywności el. nr 2 (trojkat)- podwójna całka oznaczona z Bt*B*D*h*10^6:")
Kszte2
print("")
print("Topel1: Macierz topologii elementu nr 2 (trojkat)")
print("liczba kolumn = liczba stopni swobody danego el.")
print("liczba wierszy = liczba stopni swobody całej struktury MES")
Topel2=matrix(12, 6, [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,1,0, 0,0,0,0,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 1,0,0,0,0,0, 0,1,0,0,0,0, 0,0,1,0,0,0, 0,0,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,])
Topel2
print("")
Topel2T=Topel2.transpose()
print("")
print("Topel2T: Macierz transponowana topologii elementu nr 2 (trojkat)")
Topel2T
print("Kszte2GUW: Macierz sztywności elementu nr 2 (trojkat) w GUW")
Ksztel2GUW=Topel2*Kszte2*Topel2T
Ksztel2GUW
print(".................................................................TROJKAT - el III:.............................................................................")
print("")
print("PRZYJMUJE UKLAD LOKALNY ZACZEPIONY W LEWYM DOLNYM WEZLE TROJKATA !")
print("")
ht3 = var('ht3')
xi3 = var('xi3')
yi3 = var('yi3')
xj3 = var('xj3')
yj3 = var('yj3')
xk3 = var('xk3')
yk3 = var('yk3')
print("")
print("Macierz 'A3' - skladowa iloczynu zmiennych z trojkta Pascala oraz niewiadomych wielomianu aproksymujacego:")
print("Macierz 'A3' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)")
print("Macierz 'A3' licza wierszy = liczba wspolrzednych stosowanego ukladu = liczba niewiadomych pojedynczego wezla")
A3=matrix(2, 6, [1,x,y,0,0,0, 0,0,0,1,x,y])
print("A3=")
A3
print("")
print("Macierz 'Aw3' - skladowa iloczynu zmiennych z projkta Pascla oraz niewiadomych wielomianu aproksymujacego po podstawieniu do A wspolrzednych wezlow:")
print("Macierz 'Aw3' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)")
print("Macierz 'Aw3' licza wierszy = liczba stopni swobody calego elementu")
Aw3=matrix(6, 6, [1,xi3,yi3,0,0,0, 0,0,0,1,xi3,yi3, 1,xj3,yj3,0,0,0, 0,0,0,1,xj3,yj3, 1,xk3,yk3,0,0,0, 0,0,0,1,xk3,yk3])
print("Aw3=")
Aw3
print("")
print("Macierz 'N3' - Macierz funkcji kształtu")
print("Macierz 'N3' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)")
print("Macierz 'N3' licza wierszy = liczba wspolrzednych stosowanego ukladu = liczba niewiadomych pojedynczego wezla")
print("[N3]=[A3]*([Aw3]^-1)")
Awi3=Aw3.inverse()
N3=A3*Awi3
print("N3=")
N3
ht3=0.15
xi3 = 0
yi3 = 0
xj3 = 2
yj3 = 2
xk3 = 0
yk3 = 2
A3=matrix(2, 6, [1,x,y,0,0,0, 0,0,0,1,x,y])
Aw3=matrix(6, 6, [1,xi3,yi3,0,0,0, 0,0,0,1,xi3,yi3, 1,xj3,yj3,0,0,0, 0,0,0,1,xj3,yj3, 1,xk3,yk3,0,0,0, 0,0,0,1,xk3,yk3])
Awi3=Aw3.inverse()
N3=A3*Awi3
print("")
print("N3 po podstawieniu=")
N3
print("")
print("Wyprowadzenie macierzy sztywności trojkata plaskiego:")
print("")
Nit3=N3[1,1]
Njt3=N3[1,3]
Nkt3=N3[1,5]
print("Funcje kształtu (na podstawie wcześniej podanych wspolrzednych wezlow):")
Nit3
Njt3
Nkt3
print("")
print("B3- Iloczyn macierzy operatorów różniczkowych i funkcji kształtu:")
Bpiot3=matrix(3, 6, [diff(Nit3, x),0,diff(Njt3, x),0,diff(Nkt3, x),0, 0,diff(Nit3, y),0,diff(Njt3, y),0,diff(Nkt3, y), diff(Nit3, y),diff(Nit3, x),diff(Njt3, y),diff(Njt3, x),diff(Nkt3, y),diff(Nkt3, x)])
Bpiot3
print("")
print("D3- Macierz sprężystości - PODAJE W GPa !!:")
Dpiot3=matrix(3, 3, [85.5,29.9,0, 29.9,85.5,0, 0,0,27.8])
Dpiot3
print("")
print("Transponowana B3:")
Bpiot3.transpose()
print("")
print("Bt3*B3*D3*ht3:")
Docalkit3=Bpiot3.transpose()*Dpiot3*Bpiot3*ht3*1000000
Docalkit3
print("jak widać iloczyn Bt*B*D*h w trójkacie jest macierza samych liczb !")
print("")
Ksztel3=Docalkit3.apply_map(lambda e: integrate(integrate(e,y,x,2), x,0,2)) #to zakres calkowania zewnetrznej calki jest od x do 2 gdyz w elemencie trojkatnym nr III w zadaniu ograniczenie z dolu jest funkcja y=x !!
print("Macierz sztywności el. nr 3 (trojkat)- podwójna całka oznaczona z Bt*B*D*h*10^6:")
Ksztel3
print("")
print("Topel3: Macierz topologii elementu nr 3 (trojkat)")
print("liczba kolumn = liczba stopni swobody danego el.")
print("liczba wierszy = liczba stopni swobody całej struktury MES")
Topel3=matrix(12, 6, [0,0,0,0,0,0, 0,0,0,0,0,0, 1,0,0,0,0,0, 0,1,0,0,0,0, 0,0,1,0,0,0, 0,0,0,1,0,0, 0,0,0,0,1,0, 0,0,0,0,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,])
Topel3
print("")
Topel3T=Topel3.transpose()
print("")
print("Topel3T: Macierz transponowana topologii elementu nr 3 (trojkat)")
Topel3T
print("Kszte2GUW: Macierz sztywności elementu nr 3 (trojkat) w GUW")
Ksztel3GUW=Topel3*Ksztel3*Topel3T
Ksztel3GUW
print("")
print("Globalna macierz sztywności")
KsztGLOBAL=Ksztel1GUW+Ksztel2GUW+Ksztel3GUW
KsztGLOBAL
KsztGLOBAL_I=KsztGLOBAL.inverse()
print("")
print("")
︡b7777a70-8341-4b1b-83e1-1636905db03b︡{"stdout":"..............................................................PROSTOKAT:............................................................................\n"}︡{"stdout":"PRZYJMUJE UKLAD LOKALNY ZACZEPIONY SRODKU GEOMETRYCZNYM PROSTOKATA !\n"}︡{"stdout":"Wymiary prostokata:\n"}︡{"stdout":"2\n"}︡{"stdout":"3\n"}︡{"stdout":"\n"}︡{"stdout":"Grubosc prosokata:\n"}︡{"stdout":"0.1500\n"}︡{"stdout":"\n"}︡{"stdout":"Funkcje kształtu prostokata:\n"}︡{"stdout":"1/12*(x - 1)*(2*y - 3)\n"}︡{"stdout":"-1/12*(x + 1)*(2*y - 3)\n"}︡{"stdout":"1/12*(x + 1)*(2*y + 3)\n"}︡{"stdout":"-1/12*(x - 1)*(2*y + 3)\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz funkcji kształtu prostokata:\n"}︡{"stdout":"[ 1/12*(x - 1)*(2*y - 3)                       0 -1/12*(x + 1)*(2*y - 3)                       0  1/12*(x + 1)*(2*y + 3)                       0 -1/12*(x - 1)*(2*y + 3)                       0]\n[                      0  1/12*(x - 1)*(2*y - 3)                       0 -1/12*(x + 1)*(2*y - 3)                       0  1/12*(x + 1)*(2*y + 3)                       0 -1/12*(x - 1)*(2*y + 3)]\n"}︡{"stdout":"Pochodne funkcji kształtu prostokata:\n"}︡{"stdout":"1/6*y - 1/4\n"}︡{"stdout":"1/6*x - 1/6\n"}︡{"stdout":"-1/6*y + 1/4\n"}︡{"stdout":"-1/6*x - 1/6\n"}︡{"stdout":"1/6*y + 1/4\n"}︡{"stdout":"1/6*x + 1/6\n"}︡{"stdout":"-1/6*y - 1/4\n"}︡{"stdout":"-1/6*x + 1/6\n"}︡{"stdout":"B: Iloczyn macierzy operatorów różniczkowych i funkcji kształtu:\n"}︡{"stdout":"[ 1/6*y - 1/4            0 -1/6*y + 1/4            0  1/6*y + 1/4            0 -1/6*y - 1/4            0]\n[           0  1/6*x - 1/6            0 -1/6*x - 1/6            0  1/6*x + 1/6            0 -1/6*x + 1/6]\n[ 1/6*x - 1/6  1/6*y - 1/4 -1/6*x - 1/6 -1/6*y + 1/4  1/6*x + 1/6  1/6*y + 1/4 -1/6*x + 1/6 -1/6*y - 1/4]\n"}︡{"stdout":"Full MatrixSpace of 3 by 8 dense matrices over Symbolic Ring\n"}︡{"stdout":"Transponowana B:\n"}︡{"stdout":"[ 1/6*y - 1/4            0  1/6*x - 1/6]\n[           0  1/6*x - 1/6  1/6*y - 1/4]\n[-1/6*y + 1/4            0 -1/6*x - 1/6]\n[           0 -1/6*x - 1/6 -1/6*y + 1/4]\n[ 1/6*y + 1/4            0  1/6*x + 1/6]\n[           0  1/6*x + 1/6  1/6*y + 1/4]\n[-1/6*y - 1/4            0 -1/6*x + 1/6]\n[           0 -1/6*x + 1/6 -1/6*y - 1/4]\n"}︡{"stdout":"Full MatrixSpace of 8 by 3 dense matrices over Symbolic Ring\n"}︡{"stdout":"D: Macierz sprężystoci- PODAJE W GPa !!:\n"}︡{"stdout":"[ 85.5000000000000  29.9000000000000 0.000000000000000]\n[ 29.9000000000000  85.5000000000000 0.000000000000000]\n[0.000000000000000 0.000000000000000  27.8000000000000]\n"}︡{"stdout":"Full MatrixSpace of 3 by 3 dense matrices over Real Field with 53 bits of precision\n"}︡{"stdout":"Bt*D*B*h:\n"}︡{"stdout":"[   0.02500*(4.63333333333333*x - 4.63333333333333)*(x - 1) + 0.01250*(14.2500000000000*y - 21.3750000000000)*(2*y - 3)    0.02500*(x - 1)*(4.98333333333333*y - 7.47500000000000) + 0.01250*(4.63333333333333*x - 4.63333333333333)*(2*y - 3)   -0.02500*(4.63333333333333*x - 4.63333333333333)*(x + 1) - 0.01250*(14.2500000000000*y - 21.3750000000000)*(2*y - 3)   -0.02500*(x + 1)*(4.98333333333333*y - 7.47500000000000) - 0.01250*(4.63333333333333*x - 4.63333333333333)*(2*y - 3)    0.02500*(4.63333333333333*x - 4.63333333333333)*(x + 1) + 0.01250*(14.2500000000000*y - 21.3750000000000)*(2*y + 3)    0.02500*(x + 1)*(4.98333333333333*y - 7.47500000000000) + 0.01250*(4.63333333333333*x - 4.63333333333333)*(2*y + 3)   -0.02500*(4.63333333333333*x - 4.63333333333333)*(x - 1) - 0.01250*(14.2500000000000*y - 21.3750000000000)*(2*y + 3)   -0.02500*(x - 1)*(4.98333333333333*y - 7.47500000000000) - 0.01250*(4.63333333333333*x - 4.63333333333333)*(2*y + 3)]\n[   0.02500*(x - 1)*(4.63333333333333*y - 6.95000000000000) + 0.01250*(4.98333333333333*x - 4.98333333333333)*(2*y - 3)    0.02500*(14.2500000000000*x - 14.2500000000000)*(x - 1) + 0.01250*(4.63333333333333*y - 6.95000000000000)*(2*y - 3)   -0.02500*(x + 1)*(4.63333333333333*y - 6.95000000000000) - 0.01250*(4.98333333333333*x - 4.98333333333333)*(2*y - 3)   -0.02500*(14.2500000000000*x - 14.2500000000000)*(x + 1) - 0.01250*(4.63333333333333*y - 6.95000000000000)*(2*y - 3)    0.02500*(x + 1)*(4.63333333333333*y - 6.95000000000000) + 0.01250*(4.98333333333333*x - 4.98333333333333)*(2*y + 3)    0.02500*(14.2500000000000*x - 14.2500000000000)*(x + 1) + 0.01250*(4.63333333333333*y - 6.95000000000000)*(2*y + 3)   -0.02500*(x - 1)*(4.63333333333333*y - 6.95000000000000) - 0.01250*(4.98333333333333*x - 4.98333333333333)*(2*y + 3)   -0.02500*(14.2500000000000*x - 14.2500000000000)*(x - 1) - 0.01250*(4.63333333333333*y - 6.95000000000000)*(2*y + 3)]\n[ 0.02500*(x - 1)*(-4.63333333333333*x - 4.63333333333333) + 0.01250*(2*y - 3)*(-14.2500000000000*y + 21.3750000000000)  0.01250*(-4.63333333333333*x - 4.63333333333333)*(2*y - 3) + 0.02500*(x - 1)*(-4.98333333333333*y + 7.47500000000000) -0.02500*(x + 1)*(-4.63333333333333*x - 4.63333333333333) - 0.01250*(2*y - 3)*(-14.2500000000000*y + 21.3750000000000) -0.01250*(-4.63333333333333*x - 4.63333333333333)*(2*y - 3) - 0.02500*(x + 1)*(-4.98333333333333*y + 7.47500000000000)  0.02500*(x + 1)*(-4.63333333333333*x - 4.63333333333333) + 0.01250*(2*y + 3)*(-14.2500000000000*y + 21.3750000000000)  0.01250*(-4.63333333333333*x - 4.63333333333333)*(2*y + 3) + 0.02500*(x + 1)*(-4.98333333333333*y + 7.47500000000000) -0.02500*(x - 1)*(-4.63333333333333*x - 4.63333333333333) - 0.01250*(2*y + 3)*(-14.2500000000000*y + 21.3750000000000) -0.01250*(-4.63333333333333*x - 4.63333333333333)*(2*y + 3) - 0.02500*(x - 1)*(-4.98333333333333*y + 7.47500000000000)]\n[ 0.01250*(-4.98333333333333*x - 4.98333333333333)*(2*y - 3) + 0.02500*(x - 1)*(-4.63333333333333*y + 6.95000000000000)  0.02500*(x - 1)*(-14.2500000000000*x - 14.2500000000000) + 0.01250*(2*y - 3)*(-4.63333333333333*y + 6.95000000000000) -0.01250*(-4.98333333333333*x - 4.98333333333333)*(2*y - 3) - 0.02500*(x + 1)*(-4.63333333333333*y + 6.95000000000000) -0.02500*(x + 1)*(-14.2500000000000*x - 14.2500000000000) - 0.01250*(2*y - 3)*(-4.63333333333333*y + 6.95000000000000)  0.01250*(-4.98333333333333*x - 4.98333333333333)*(2*y + 3) + 0.02500*(x + 1)*(-4.63333333333333*y + 6.95000000000000)  0.02500*(x + 1)*(-14.2500000000000*x - 14.2500000000000) + 0.01250*(2*y + 3)*(-4.63333333333333*y + 6.95000000000000) -0.01250*(-4.98333333333333*x - 4.98333333333333)*(2*y + 3) - 0.02500*(x - 1)*(-4.63333333333333*y + 6.95000000000000) -0.02500*(x - 1)*(-14.2500000000000*x - 14.2500000000000) - 0.01250*(2*y + 3)*(-4.63333333333333*y + 6.95000000000000)]\n[   0.02500*(4.63333333333333*x + 4.63333333333333)*(x - 1) + 0.01250*(14.2500000000000*y + 21.3750000000000)*(2*y - 3)    0.02500*(x - 1)*(4.98333333333333*y + 7.47500000000000) + 0.01250*(4.63333333333333*x + 4.63333333333333)*(2*y - 3)   -0.02500*(4.63333333333333*x + 4.63333333333333)*(x + 1) - 0.01250*(14.2500000000000*y + 21.3750000000000)*(2*y - 3)   -0.02500*(x + 1)*(4.98333333333333*y + 7.47500000000000) - 0.01250*(4.63333333333333*x + 4.63333333333333)*(2*y - 3)    0.02500*(4.63333333333333*x + 4.63333333333333)*(x + 1) + 0.01250*(14.2500000000000*y + 21.3750000000000)*(2*y + 3)    0.02500*(x + 1)*(4.98333333333333*y + 7.47500000000000) + 0.01250*(4.63333333333333*x + 4.63333333333333)*(2*y + 3)   -0.02500*(4.63333333333333*x + 4.63333333333333)*(x - 1) - 0.01250*(14.2500000000000*y + 21.3750000000000)*(2*y + 3)   -0.02500*(x - 1)*(4.98333333333333*y + 7.47500000000000) - 0.01250*(4.63333333333333*x + 4.63333333333333)*(2*y + 3)]\n[   0.02500*(x - 1)*(4.63333333333333*y + 6.95000000000000) + 0.01250*(4.98333333333333*x + 4.98333333333333)*(2*y - 3)    0.02500*(14.2500000000000*x + 14.2500000000000)*(x - 1) + 0.01250*(4.63333333333333*y + 6.95000000000000)*(2*y - 3)   -0.02500*(x + 1)*(4.63333333333333*y + 6.95000000000000) - 0.01250*(4.98333333333333*x + 4.98333333333333)*(2*y - 3)   -0.02500*(14.2500000000000*x + 14.2500000000000)*(x + 1) - 0.01250*(4.63333333333333*y + 6.95000000000000)*(2*y - 3)    0.02500*(x + 1)*(4.63333333333333*y + 6.95000000000000) + 0.01250*(4.98333333333333*x + 4.98333333333333)*(2*y + 3)    0.02500*(14.2500000000000*x + 14.2500000000000)*(x + 1) + 0.01250*(4.63333333333333*y + 6.95000000000000)*(2*y + 3)   -0.02500*(x - 1)*(4.63333333333333*y + 6.95000000000000) - 0.01250*(4.98333333333333*x + 4.98333333333333)*(2*y + 3)   -0.02500*(14.2500000000000*x + 14.2500000000000)*(x - 1) - 0.01250*(4.63333333333333*y + 6.95000000000000)*(2*y + 3)]\n[ 0.02500*(x - 1)*(-4.63333333333333*x + 4.63333333333333) + 0.01250*(2*y - 3)*(-14.2500000000000*y - 21.3750000000000)  0.01250*(-4.63333333333333*x + 4.63333333333333)*(2*y - 3) + 0.02500*(x - 1)*(-4.98333333333333*y - 7.47500000000000) -0.02500*(x + 1)*(-4.63333333333333*x + 4.63333333333333) - 0.01250*(2*y - 3)*(-14.2500000000000*y - 21.3750000000000) -0.01250*(-4.63333333333333*x + 4.63333333333333)*(2*y - 3) - 0.02500*(x + 1)*(-4.98333333333333*y - 7.47500000000000)  0.02500*(x + 1)*(-4.63333333333333*x + 4.63333333333333) + 0.01250*(2*y + 3)*(-14.2500000000000*y - 21.3750000000000)  0.01250*(-4.63333333333333*x + 4.63333333333333)*(2*y + 3) + 0.02500*(x + 1)*(-4.98333333333333*y - 7.47500000000000) -0.02500*(x - 1)*(-4.63333333333333*x + 4.63333333333333) - 0.01250*(2*y + 3)*(-14.2500000000000*y - 21.3750000000000) -0.01250*(-4.63333333333333*x + 4.63333333333333)*(2*y + 3) - 0.02500*(x - 1)*(-4.98333333333333*y - 7.47500000000000)]\n[ 0.01250*(-4.98333333333333*x + 4.98333333333333)*(2*y - 3) + 0.02500*(x - 1)*(-4.63333333333333*y - 6.95000000000000)  0.02500*(x - 1)*(-14.2500000000000*x + 14.2500000000000) + 0.01250*(2*y - 3)*(-4.63333333333333*y - 6.95000000000000) -0.01250*(-4.98333333333333*x + 4.98333333333333)*(2*y - 3) - 0.02500*(x + 1)*(-4.63333333333333*y - 6.95000000000000) -0.02500*(x + 1)*(-14.2500000000000*x + 14.2500000000000) - 0.01250*(2*y - 3)*(-4.63333333333333*y - 6.95000000000000)  0.01250*(-4.98333333333333*x + 4.98333333333333)*(2*y + 3) + 0.02500*(x + 1)*(-4.63333333333333*y - 6.95000000000000)  0.02500*(x + 1)*(-14.2500000000000*x + 14.2500000000000) + 0.01250*(2*y + 3)*(-4.63333333333333*y - 6.95000000000000) -0.01250*(-4.98333333333333*x + 4.98333333333333)*(2*y + 3) - 0.02500*(x - 1)*(-4.63333333333333*y - 6.95000000000000) -0.02500*(x - 1)*(-14.2500000000000*x + 14.2500000000000) - 0.01250*(2*y + 3)*(-4.63333333333333*y - 6.95000000000000)]"}︡{"stdout":"\n"}︡{"stdout":"Macierz sztywności el. nr 1 (prostokat)- podwójna całka oznaczona z Bt*D*B*h*10^6:\n"}︡{"stdout":"[ 7339166.666666668          2163750.0 -5949166.666666666  78750.00000000017 -3669583.333333334         -2163750.0  2279583.333333333 -78750.00000000023]\n[         2163750.0          4935000.0 -78749.99999999983 -660000.0000000001         -2163750.0         -2467500.0  78749.99999999977         -1807500.0]\n[-5949166.666666666 -78750.00000000017  7339166.666666668         -2163750.0  2279583.333333333  78750.00000000023 -3669583.333333334          2163750.0]\n[ 78749.99999999983 -660000.0000000001         -2163750.0          4935000.0 -78749.99999999977         -1807500.0          2163750.0         -2467500.0]\n[-3669583.333333334         -2163750.0  2279583.333333333 -78750.00000000023  7339166.666666668          2163750.0 -5949166.666666666  78750.00000000017]\n[        -2163750.0         -2467500.0  78749.99999999977         -1807500.0          2163750.0          4935000.0 -78749.99999999983 -660000.0000000001]\n[ 2279583.333333333  78750.00000000023 -3669583.333333334          2163750.0 -5949166.666666666 -78750.00000000017  7339166.666666668         -2163750.0]\n[-78749.99999999977         -1807500.0          2163750.0         -2467500.0  78749.99999999983 -660000.0000000001         -2163750.0          4935000.0]\n"}︡{"stdout":"\n"}︡{"stdout":"Topel1: Macierz topologii elementu nr 1 (prostokat)\n"}︡{"stdout":"liczba kolumn = liczba stopni swobody danego el.\n"}︡{"stdout":"liczba wierszy = liczba stopni swobody całej struktury MES\n"}︡{"stdout":"[0 0 1 0 0 0 0 0]\n[0 0 0 1 0 0 0 0]\n[0 0 0 0 1 0 0 0]\n[0 0 0 0 0 1 0 0]\n[0 0 0 0 0 0 0 0]\n[0 0 0 0 0 0 0 0]\n[0 0 0 0 0 0 0 0]\n[0 0 0 0 0 0 0 0]\n[0 0 0 0 0 0 1 0]\n[0 0 0 0 0 0 0 1]\n[1 0 0 0 0 0 0 0]\n[0 1 0 0 0 0 0 0]\n"}︡{"stdout":"\n"}︡{"stdout":"\n"}︡{"stdout":"Topel1T: Macierz transponowana topologii elementu nr 1 (prostokat)\n"}︡{"stdout":"[0 0 0 0 0 0 0 0 0 0 1 0]\n[0 0 0 0 0 0 0 0 0 0 0 1]\n[1 0 0 0 0 0 0 0 0 0 0 0]\n[0 1 0 0 0 0 0 0 0 0 0 0]\n[0 0 1 0 0 0 0 0 0 0 0 0]\n[0 0 0 1 0 0 0 0 0 0 0 0]\n[0 0 0 0 0 0 0 0 1 0 0 0]\n[0 0 0 0 0 0 0 0 0 1 0 0]\n"}︡{"stdout":"Ksztel1GUW: Macierz sztywności elementu nr 1 (prostokat) w GUW\n"}︡{"stdout":"[ 7339166.666666668         -2163750.0  2279583.333333333  78750.00000000023                  0                  0                  0                  0 -3669583.333333334          2163750.0 -5949166.666666666 -78750.00000000017]\n[        -2163750.0          4935000.0 -78749.99999999977         -1807500.0                  0                  0                  0                  0          2163750.0         -2467500.0  78749.99999999983 -660000.0000000001]\n[ 2279583.333333333 -78750.00000000023  7339166.666666668          2163750.0                  0                  0                  0                  0 -5949166.666666666  78750.00000000017 -3669583.333333334         -2163750.0]\n[ 78749.99999999977         -1807500.0          2163750.0          4935000.0                  0                  0                  0                  0 -78749.99999999983 -660000.0000000001         -2163750.0         -2467500.0]\n[                 0                  0                  0                  0                  0                  0                  0                  0                  0                  0                  0                  0]\n[                 0                  0                  0                  0                  0                  0                  0                  0                  0                  0                  0                  0]\n[                 0                  0                  0                  0                  0                  0                  0                  0                  0                  0                  0                  0]\n[                 0                  0                  0                  0                  0                  0                  0                  0                  0                  0                  0                  0]\n[-3669583.333333334          2163750.0 -5949166.666666666 -78750.00000000017                  0                  0                  0                  0  7339166.666666668         -2163750.0  2279583.333333333  78750.00000000023]\n[         2163750.0         -2467500.0  78749.99999999983 -660000.0000000001                  0                  0                  0                  0         -2163750.0          4935000.0 -78749.99999999977         -1807500.0]\n[-5949166.666666666  78750.00000000017 -3669583.333333334         -2163750.0                  0                  0                  0                  0  2279583.333333333 -78750.00000000023  7339166.666666668          2163750.0]\n[-78749.99999999983 -660000.0000000001         -2163750.0         -2467500.0                  0                  0                  0                  0  78749.99999999977         -1807500.0          2163750.0          4935000.0]\n"}︡{"stdout":"\n"}︡{"stdout":"\n"}︡{"stdout":".................................................................TROJKAT - el. II:.............................................................................\n"}︡{"stdout":"\n"}︡{"stdout":"PRZYJMUJE UKLAD LOKALNY ZACZEPIONY W LEWYM DOLNYM WEZLE TROJKATA !\n"}︡{"stdout":"\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz 'A' - skladowa iloczynu zmiennych z trojkta Pascala oraz niewiadomych wielomianu aproksymujacego:\n"}︡{"stdout":"Macierz 'A' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)\n"}︡{"stdout":"Macierz 'A' licza wierszy = liczba wspolrzednych stosowanego ukladu = liczba niewiadomych pojedynczego wezla\n"}︡{"stdout":"A=\n"}︡{"stdout":"[1 x y 0 0 0]\n[0 0 0 1 x y]\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz 'Aw' - skladowa iloczynu zmiennych z projkta Pascla oraz niewiadomych wielomianu aproksymujacego po podstawieniu do A wspolrzednych wezlow:\n"}︡{"stdout":"Macierz 'Aw' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)\n"}︡{"stdout":"Macierz 'Aw' licza wierszy = liczba stopni swobody calego elementu\n"}︡{"stdout":"Aw=\n"}︡{"stdout":"[ 1 xi yi  0  0  0]\n[ 0  0  0  1 xi yi]\n[ 1 xj yj  0  0  0]\n[ 0  0  0  1 xj yj]\n[ 1 xk yk  0  0  0]\n[ 0  0  0  1 xk yk]\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz 'N2' - Macierz funkcji kształtu\n"}︡{"stdout":"Macierz 'N2' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)\n"}︡{"stdout":"Macierz 'N2' licza wierszy = liczba wspolrzednych stosowanego ukladu = liczba niewiadomych pojedynczego wezla\n"}︡{"stdout":"[N2]=[A]*([Aw]^-1)\n"}︡{"stdout":"N2=\n"}︡{"stdout":"[-x*((yi - yj)*((xi - xk)/(xi - xj) - 1)/((xi - xj)*((xi - xk)*(yi - yj)/(xi - xj) - yi + yk)) - 1/(xi - xj)) + y*((xi - xk)/(xi - xj) - 1)/((xi - xk)*(yi - yj)/(xi - xj) - yi + yk) + (xi*(yi - yj)/(xi - xj) - yi)*((xi - xk)/(xi - xj) - 1)/((xi - xk)*(yi - yj)/(xi - xj) - yi + yk) - xi/(xi - xj) + 1                                                                                                                                                                                                                                                                                                           0                           -x*(1/(xi - xj) - (xi - xk)*(yi - yj)/((xi - xj)^2*((xi - xk)*(yi - yj)/(xi - xj) - yi + yk))) + xi/(xi - xj) - (xi - xk)*y/((xi - xj)*((xi - xk)*(yi - yj)/(xi - xj) - yi + yk)) - (xi - xk)*(xi*(yi - yj)/(xi - xj) - yi)/((xi - xj)*((xi - xk)*(yi - yj)/(xi - xj) - yi + yk))                                                                                                                                                                                                                                                                                                           0                                                                                                                   y/((xi - xk)*(yi - yj)/(xi - xj) - yi + yk) + (xi*(yi - yj)/(xi - xj) - yi)/((xi - xk)*(yi - yj)/(xi - xj) - yi + yk) - x*(yi - yj)/((xi - xj)*((xi - xk)*(yi - yj)/(xi - xj) - yi + yk))                                                                                                                                                                                                                                                                                                           0]\n[                                                                                                                                                                                                                                                                                                          0                            x*(1/(xi - xj) - (xj - xk)*(yi - yj)/((xi - xj)^2*((xj - xk)*(yi - yj)/(xi - xj) - yj + yk))) - xj/(xi - xj) + (xj - xk)*y/((xi - xj)*((xj - xk)*(yi - yj)/(xi - xj) - yj + yk)) + (xj - xk)*(xj*(yi - yj)/(xi - xj) - yj)/((xi - xj)*((xj - xk)*(yi - yj)/(xi - xj) - yj + yk))                                                                                                                                                                                                                                                                                                           0  x*((yi - yj)*((xj - xk)/(xi - xj) + 1)/((xi - xj)*((xj - xk)*(yi - yj)/(xi - xj) - yj + yk)) - 1/(xi - xj)) - y*((xj - xk)/(xi - xj) + 1)/((xj - xk)*(yi - yj)/(xi - xj) - yj + yk) - (xj*(yi - yj)/(xi - xj) - yj)*((xj - xk)/(xi - xj) + 1)/((xj - xk)*(yi - yj)/(xi - xj) - yj + yk) + xj/(xi - xj) + 1                                                                                                                                                                                                                                                                                                           0                                                                                                                   y/((xj - xk)*(yi - yj)/(xi - xj) - yj + yk) + (xj*(yi - yj)/(xi - xj) - yj)/((xj - xk)*(yi - yj)/(xi - xj) - yj + yk) - x*(yi - yj)/((xi - xj)*((xj - xk)*(yi - yj)/(xi - xj) - yj + yk))]\n"}︡{"stdout":"\n"}︡{"stdout":"N2 po podstawieniu=\n"}︡{"stdout":"[    1/2*y + 1             0        -1/2*x             0 1/2*x - 1/2*y             0]\n[            0     1/2*y + 1             0        -1/2*x             0 1/2*x - 1/2*y]\n"}︡{"stdout":"\n"}︡{"stdout":"Wyprowadzenie macierzy sztywności trojkata plaskiego:\n"}︡{"stdout":"\n"}︡{"stdout":"Funcje kształtu (na podstawie wcześniej podanych wspolrzednych wezlow):\n"}︡{"stdout":"1/2*y + 1\n"}︡{"stdout":"-1/2*x\n"}︡{"stdout":"1/2*x - 1/2*y\n"}︡{"stdout":"\n"}︡{"stdout":"B- Iloczyn macierzy operatorów różniczkowych i funkcji kształtu:\n"}︡{"stdout":"[   0    0 -1/2    0  1/2    0]\n[   0  1/2    0    0    0 -1/2]\n[ 1/2    0    0 -1/2 -1/2  1/2]\n"}︡{"stdout":"\n"}︡{"stdout":"D- Macierz sprężystości - PODAJE W GPa !!:\n"}︡{"stdout":"[ 85.5000000000000  29.9000000000000 0.000000000000000]\n[ 29.9000000000000  85.5000000000000 0.000000000000000]\n[0.000000000000000 0.000000000000000  27.8000000000000]\n"}︡{"stdout":"\n"}︡{"stdout":"Transponowana B:\n"}︡{"stdout":"[   0    0  1/2]\n[   0  1/2    0]\n[-1/2    0    0]\n[   0    0 -1/2]\n[ 1/2    0 -1/2]\n[   0 -1/2  1/2]\n"}︡{"stdout":"\n"}︡{"stdout":"Bt*B*D*h:\n"}︡{"stdout":"[ 1.04250000000000e6                   0                   0 -1.04250000000000e6 -1.04250000000000e6  1.04250000000000e6]\n[                  0  3.20625000000000e6 -1.12125000000000e6                   0  1.12125000000000e6 -3.20625000000000e6]\n[                  0 -1.12125000000000e6  3.20625000000000e6                   0 -3.20625000000000e6  1.12125000000000e6]\n[-1.04250000000000e6                   0                   0  1.04250000000000e6  1.04250000000000e6 -1.04250000000000e6]\n[-1.04250000000000e6  1.12125000000000e6 -3.20625000000000e6  1.04250000000000e6  4.24875000000000e6 -2.16375000000000e6]\n[ 1.04250000000000e6 -3.20625000000000e6  1.12125000000000e6 -1.04250000000000e6 -2.16375000000000e6  4.24875000000000e6]\n"}︡{"stdout":"sprawdz:\n"}︡{"stdout":"[ 2.08500000000000e6                   0                   0 -2.08500000000000e6 -2.08500000000000e6  2.08500000000000e6]\n[                  0  6.41250000000000e6 -2.24250000000000e6                   0  2.24250000000000e6 -6.41250000000000e6]\n[                  0 -2.24250000000000e6  6.41250000000000e6                   0 -6.41250000000000e6  2.24250000000000e6]\n[-2.08500000000000e6                   0                   0  2.08500000000000e6  2.08500000000000e6 -2.08500000000000e6]\n[-2.08500000000000e6  2.24250000000000e6 -6.41250000000000e6  2.08500000000000e6  8.49750000000000e6 -4.32750000000000e6]\n[ 2.08500000000000e6 -6.41250000000000e6  2.24250000000000e6 -2.08500000000000e6 -4.32750000000000e6  8.49750000000000e6]\n"}︡{"stdout":"jak widać iloczyn Bt*B*D*h w trójkacie jest macierza samych liczb !\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz sztywności el. nr 2 (trojkat)- podwójna całka oznaczona z Bt*B*D*h*10^6:\n"}︡{"stdout":"[          2085000.0                   0                   0          -2085000.0          -2085000.0           2085000.0]\n[                  0           6412500.0 -2242499.9999999995                   0  2242499.9999999995          -6412500.0]\n[                  0 -2242499.9999999995           6412500.0                   0          -6412500.0  2242499.9999999995]\n[         -2085000.0                   0                   0           2085000.0           2085000.0          -2085000.0]\n[         -2085000.0  2242499.9999999995          -6412500.0           2085000.0   8497499.999999998          -4327500.0]\n[          2085000.0          -6412500.0  2242499.9999999995          -2085000.0          -4327500.0   8497499.999999998]\n"}︡{"stdout":"\n"}︡{"stdout":"Topel1: Macierz topologii elementu nr 2 (trojkat)\n"}︡{"stdout":"liczba kolumn = liczba stopni swobody danego el.\n"}︡{"stdout":"liczba wierszy = liczba stopni swobody całej struktury MES\n"}︡{"stdout":"[0 0 0 0 0 0]\n[0 0 0 0 0 0]\n[0 0 0 0 1 0]\n[0 0 0 0 0 1]\n[0 0 0 0 0 0]\n[0 0 0 0 0 0]\n[1 0 0 0 0 0]\n[0 1 0 0 0 0]\n[0 0 1 0 0 0]\n[0 0 0 1 0 0]\n[0 0 0 0 0 0]\n[0 0 0 0 0 0]\n"}︡{"stdout":"\n"}︡{"stdout":"\n"}︡{"stdout":"Topel2T: Macierz transponowana topologii elementu nr 2 (trojkat)\n"}︡{"stdout":"[0 0 0 0 0 0 1 0 0 0 0 0]\n[0 0 0 0 0 0 0 1 0 0 0 0]\n[0 0 0 0 0 0 0 0 1 0 0 0]\n[0 0 0 0 0 0 0 0 0 1 0 0]\n[0 0 1 0 0 0 0 0 0 0 0 0]\n[0 0 0 1 0 0 0 0 0 0 0 0]\n"}︡{"stdout":"Kszte2GUW: Macierz sztywności elementu nr 2 (trojkat) w GUW\n"}︡{"stdout":"[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0   8497499.999999998          -4327500.0                   0                   0          -2085000.0  2242499.9999999995          -6412500.0           2085000.0                   0                   0]\n[                  0                   0          -4327500.0   8497499.999999998                   0                   0           2085000.0          -6412500.0  2242499.9999999995          -2085000.0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0          -2085000.0           2085000.0                   0                   0           2085000.0                   0                   0          -2085000.0                   0                   0]\n[                  0                   0  2242499.9999999995          -6412500.0                   0                   0                   0           6412500.0 -2242499.9999999995                   0                   0                   0]\n[                  0                   0          -6412500.0  2242499.9999999995                   0                   0                   0 -2242499.9999999995           6412500.0                   0                   0                   0]\n[                  0                   0           2085000.0          -2085000.0                   0                   0          -2085000.0                   0                   0           2085000.0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n"}︡{"stdout":".................................................................TROJKAT - el III:.............................................................................\n"}︡{"stdout":"\n"}︡{"stdout":"PRZYJMUJE UKLAD LOKALNY ZACZEPIONY W LEWYM DOLNYM WEZLE TROJKATA !\n"}︡{"stdout":"\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz 'A3' - skladowa iloczynu zmiennych z trojkta Pascala oraz niewiadomych wielomianu aproksymujacego:\n"}︡{"stdout":"Macierz 'A3' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)\n"}︡{"stdout":"Macierz 'A3' licza wierszy = liczba wspolrzednych stosowanego ukladu = liczba niewiadomych pojedynczego wezla\n"}︡{"stdout":"A3=\n"}︡{"stdout":"[1 x y 0 0 0]\n[0 0 0 1 x y]\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz 'Aw3' - skladowa iloczynu zmiennych z projkta Pascla oraz niewiadomych wielomianu aproksymujacego po podstawieniu do A wspolrzednych wezlow:\n"}︡{"stdout":"Macierz 'Aw3' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)\n"}︡{"stdout":"Macierz 'Aw3' licza wierszy = liczba stopni swobody calego elementu\n"}︡{"stdout":"Aw3=\n"}︡{"stdout":"[  1 xi3 yi3   0   0   0]\n[  0   0   0   1 xi3 yi3]\n[  1 xj3 yj3   0   0   0]\n[  0   0   0   1 xj3 yj3]\n[  1 xk3 yk3   0   0   0]\n[  0   0   0   1 xk3 yk3]\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz 'N3' - Macierz funkcji kształtu\n"}︡{"stdout":"Macierz 'N3' licza kolumn = liczba skladników wielomianu*liczba wspolrzednych stosowanego ukladu = liczba stopni swobody calego elementu)\n"}︡{"stdout":"Macierz 'N3' licza wierszy = liczba wspolrzednych stosowanego ukladu = liczba niewiadomych pojedynczego wezla\n"}︡{"stdout":"[N3]=[A3]*([Aw3]^-1)\n"}︡{"stdout":"N3=\n"}︡{"stdout":"[-x*((yi3 - yj3)*((xi3 - xk3)/(xi3 - xj3) - 1)/((xi3 - xj3)*((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3)) - 1/(xi3 - xj3)) + y*((xi3 - xk3)/(xi3 - xj3) - 1)/((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3) + (xi3*(yi3 - yj3)/(xi3 - xj3) - yi3)*((xi3 - xk3)/(xi3 - xj3) - 1)/((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3) - xi3/(xi3 - xj3) + 1                                                                                                                                                                                                                                                                                                                                                              0                             -x*(1/(xi3 - xj3) - (xi3 - xk3)*(yi3 - yj3)/((xi3 - xj3)^2*((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3))) + xi3/(xi3 - xj3) - (xi3 - xk3)*y/((xi3 - xj3)*((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3)) - (xi3 - xk3)*(xi3*(yi3 - yj3)/(xi3 - xj3) - yi3)/((xi3 - xj3)*((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3))                                                                                                                                                                                                                                                                                                                                                              0                                                                                                                                    y/((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3) + (xi3*(yi3 - yj3)/(xi3 - xj3) - yi3)/((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3) - x*(yi3 - yj3)/((xi3 - xj3)*((xi3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yi3 + yk3))                                                                                                                                                                                                                                                                                                                                                              0]\n[                                                                                                                                                                                                                                                                                                                                                             0                              x*(1/(xi3 - xj3) - (xj3 - xk3)*(yi3 - yj3)/((xi3 - xj3)^2*((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3))) - xj3/(xi3 - xj3) + (xj3 - xk3)*y/((xi3 - xj3)*((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3)) + (xj3 - xk3)*(xj3*(yi3 - yj3)/(xi3 - xj3) - yj3)/((xi3 - xj3)*((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3))                                                                                                                                                                                                                                                                                                                                                              0  x*((yi3 - yj3)*((xj3 - xk3)/(xi3 - xj3) + 1)/((xi3 - xj3)*((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3)) - 1/(xi3 - xj3)) - y*((xj3 - xk3)/(xi3 - xj3) + 1)/((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3) - (xj3*(yi3 - yj3)/(xi3 - xj3) - yj3)*((xj3 - xk3)/(xi3 - xj3) + 1)/((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3) + xj3/(xi3 - xj3) + 1                                                                                                                                                                                                                                                                                                                                                              0                                                                                                                                    y/((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3) + (xj3*(yi3 - yj3)/(xi3 - xj3) - yj3)/((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3) - x*(yi3 - yj3)/((xi3 - xj3)*((xj3 - xk3)*(yi3 - yj3)/(xi3 - xj3) - yj3 + yk3))]"}︡{"stdout":"\n"}︡{"stdout":"\n"}︡{"stdout":"N3 po podstawieniu=\n"}︡{"stdout":"[    -1/2*y + 1              0          1/2*x              0 -1/2*x + 1/2*y              0]\n[             0     -1/2*y + 1              0          1/2*x              0 -1/2*x + 1/2*y]\n"}︡{"stdout":"\n"}︡{"stdout":"Wyprowadzenie macierzy sztywności trojkata plaskiego:\n"}︡{"stdout":"\n"}︡{"stdout":"Funcje kształtu (na podstawie wcześniej podanych wspolrzednych wezlow):\n"}︡{"stdout":"-1/2*y + 1\n"}︡{"stdout":"1/2*x\n"}︡{"stdout":"-1/2*x + 1/2*y\n"}︡{"stdout":"\n"}︡{"stdout":"B3- Iloczyn macierzy operatorów różniczkowych i funkcji kształtu:\n"}︡{"stdout":"[   0    0  1/2    0 -1/2    0]\n[   0 -1/2    0    0    0  1/2]\n[-1/2    0    0  1/2  1/2 -1/2]\n"}︡{"stdout":"\n"}︡{"stdout":"D3- Macierz sprężystości - PODAJE W GPa !!:\n"}︡{"stdout":"[ 85.5000000000000  29.9000000000000 0.000000000000000]\n[ 29.9000000000000  85.5000000000000 0.000000000000000]\n[0.000000000000000 0.000000000000000  27.8000000000000]\n"}︡{"stdout":"\n"}︡{"stdout":"Transponowana B3:\n"}︡{"stdout":"[   0    0 -1/2]\n[   0 -1/2    0]\n[ 1/2    0    0]\n[   0    0  1/2]\n[-1/2    0  1/2]\n[   0  1/2 -1/2]\n"}︡{"stdout":"\n"}︡{"stdout":"Bt3*B3*D3*ht3:\n"}︡{"stdout":"[ 1.04250000000000e6                   0                   0 -1.04250000000000e6 -1.04250000000000e6  1.04250000000000e6]\n[                  0  3.20625000000000e6 -1.12125000000000e6                   0  1.12125000000000e6 -3.20625000000000e6]\n[                  0 -1.12125000000000e6  3.20625000000000e6                   0 -3.20625000000000e6  1.12125000000000e6]\n[-1.04250000000000e6                   0                   0  1.04250000000000e6  1.04250000000000e6 -1.04250000000000e6]\n[-1.04250000000000e6  1.12125000000000e6 -3.20625000000000e6  1.04250000000000e6  4.24875000000000e6 -2.16375000000000e6]\n[ 1.04250000000000e6 -3.20625000000000e6  1.12125000000000e6 -1.04250000000000e6 -2.16375000000000e6  4.24875000000000e6]\n"}︡{"stdout":"jak widać iloczyn Bt*B*D*h w trójkacie jest macierza samych liczb !\n"}︡{"stdout":"\n"}︡{"stdout":"Macierz sztywności el. nr 3 (trojkat)- podwójna całka oznaczona z Bt*B*D*h*10^6:\n"}︡{"stdout":"[          2085000.0                   0                   0          -2085000.0          -2085000.0           2085000.0]\n[                  0           6412500.0 -2242499.9999999995                   0  2242499.9999999995          -6412500.0]\n[                  0 -2242499.9999999995           6412500.0                   0          -6412500.0  2242499.9999999995]\n[         -2085000.0                   0                   0           2085000.0           2085000.0          -2085000.0]\n[         -2085000.0  2242499.9999999995          -6412500.0           2085000.0   8497499.999999998          -4327500.0]\n[          2085000.0          -6412500.0  2242499.9999999995          -2085000.0          -4327500.0   8497499.999999998]\n"}︡{"stdout":"\n"}︡{"stdout":"Topel3: Macierz topologii elementu nr 3 (trojkat)\n"}︡{"stdout":"liczba kolumn = liczba stopni swobody danego el.\n"}︡{"stdout":"liczba wierszy = liczba stopni swobody całej struktury MES\n"}︡{"stdout":"[0 0 0 0 0 0]\n[0 0 0 0 0 0]\n[1 0 0 0 0 0]\n[0 1 0 0 0 0]\n[0 0 1 0 0 0]\n[0 0 0 1 0 0]\n[0 0 0 0 1 0]\n[0 0 0 0 0 1]\n[0 0 0 0 0 0]\n[0 0 0 0 0 0]\n[0 0 0 0 0 0]\n[0 0 0 0 0 0]\n"}︡{"stdout":"\n"}︡{"stdout":"\n"}︡{"stdout":"Topel3T: Macierz transponowana topologii elementu nr 3 (trojkat)\n"}︡{"stdout":"[0 0 1 0 0 0 0 0 0 0 0 0]\n[0 0 0 1 0 0 0 0 0 0 0 0]\n[0 0 0 0 1 0 0 0 0 0 0 0]\n[0 0 0 0 0 1 0 0 0 0 0 0]\n[0 0 0 0 0 0 1 0 0 0 0 0]\n[0 0 0 0 0 0 0 1 0 0 0 0]\n"}︡{"stdout":"Kszte2GUW: Macierz sztywności elementu nr 3 (trojkat) w GUW\n"}︡{"stdout":"[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0           2085000.0                   0                   0          -2085000.0          -2085000.0           2085000.0                   0                   0                   0                   0]\n[                  0                   0                   0           6412500.0 -2242499.9999999995                   0  2242499.9999999995          -6412500.0                   0                   0                   0                   0]\n[                  0                   0                   0 -2242499.9999999995           6412500.0                   0          -6412500.0  2242499.9999999995                   0                   0                   0                   0]\n[                  0                   0          -2085000.0                   0                   0           2085000.0           2085000.0          -2085000.0                   0                   0                   0                   0]\n[                  0                   0          -2085000.0  2242499.9999999995          -6412500.0           2085000.0   8497499.999999998          -4327500.0                   0                   0                   0                   0]\n[                  0                   0           2085000.0          -6412500.0  2242499.9999999995          -2085000.0          -4327500.0   8497499.999999998                   0                   0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n[                  0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0                   0]\n"}︡{"stdout":"\n"}︡{"stdout":"Globalna macierz sztywności\n"}︡{"stdout":"[  7339166.666666668          -2163750.0   2279583.333333333   78750.00000000023                   0                   0                   0                   0  -3669583.333333334           2163750.0  -5949166.666666666  -78750.00000000017]\n[         -2163750.0           4935000.0  -78749.99999999977          -1807500.0                   0                   0                   0                   0           2163750.0          -2467500.0   78749.99999999983  -660000.0000000001]\n[  2279583.333333333  -78750.00000000023  17921666.666666664          -2163750.0                   0          -2085000.0          -4170000.0           4327500.0 -12361666.666666666           2163750.0  -3669583.333333334          -2163750.0]\n[  78749.99999999977          -1807500.0          -2163750.0          19845000.0 -2242499.9999999995                   0           4327500.0         -12825000.0  2163749.9999999995          -2745000.0          -2163750.0          -2467500.0]\n[                  0                   0                   0 -2242499.9999999995           6412500.0                   0          -6412500.0  2242499.9999999995                   0                   0                   0                   0]\n[                  0                   0          -2085000.0                   0                   0           2085000.0           2085000.0          -2085000.0                   0                   0                   0                   0]\n[                  0                   0          -4170000.0           4327500.0          -6412500.0           2085000.0  10582499.999999998          -4327500.0                   0          -2085000.0                   0                   0]\n[                  0                   0           4327500.0         -12825000.0  2242499.9999999995          -2085000.0          -4327500.0  14909999.999999998 -2242499.9999999995                   0                   0                   0]\n[ -3669583.333333334           2163750.0 -12361666.666666666  2163749.9999999995                   0                   0                   0 -2242499.9999999995  13751666.666666668          -2163750.0   2279583.333333333   78750.00000000023]\n[          2163750.0          -2467500.0           2163750.0          -2745000.0                   0                   0          -2085000.0                   0          -2163750.0           7020000.0  -78749.99999999977          -1807500.0]\n[ -5949166.666666666   78750.00000000017  -3669583.333333334          -2163750.0                   0                   0                   0                   0   2279583.333333333  -78750.00000000023   7339166.666666668           2163750.0]\n[ -78749.99999999983  -660000.0000000001          -2163750.0          -2467500.0                   0                   0                   0                   0   78749.99999999977          -1807500.0           2163750.0           4935000.0]\n"}︡{"stdout":"\n"}︡{"stdout":"\n"}︡{"done":true}
︠e78a97a4-b552-4aa5-802f-630723d11782s︠

print(".................................................................Obciazenia:.............................................................................")
print("")
print("Obliczenia wektora obciazen wezłowych przylozonych na krawedzi elementu nr 3 (trojkata):")
print("")
N3_y2=N3(y=2)
N3_y2
N3_y2TR=N3_y2.transpose()
N3_y2TR
Obc3=matrix(2,1, [0, x*4-16])
Obc3
Obc3DOCALKI=N3_y2TR*Obc3
Wektobc3=Obc3DOCALKI.apply_map(lambda e: integrate(e,x,0,2))
print("Wektor obciazen wezlowych przylozonych na krawedzi elementu nr 3 (trojkata):")
Wektobc3
print("")
print("Wektor wiezi podporowych elementu nr 1 (prostokata):") # zgodnie z dyskretyzacja, numeracja lokalna (i, j, k , r)
print("zostanie wyliczony od razu w ukladzie globalnym")
print("Wektor wiezi podporowych elementu nr 2 (trojkata):") # zgodnie z dyskretyzacja, numeracja lokalna (i, j, k)
print("jest zerowy")
print("")
print("Wektor obciazen wezłowych el.3 w ukladzie globalnym:")
Wektobc3GUW=Topel3*Wektobc3
Wektobc3GUW
print("")
print("Globalny wektor obciazen:")
WektobcGUW=Wektobc3GUW
WektobcGUW
print("")
print("Globalny wektor reakcji:")
WektReak=matrix(12,1, [R1, R2, 0, 0, 0, 0, 0, 0, 0, 0, R11, R12])
WektReak
print("")
print("Globalny wektor reakcji+obciazen:")
print("")
WektReaObc=WektReak+WektobcGUW
WektReaObc
print("Globalny wektor przemieszczen z uwzglednieniem warunkow brzegowych:")
print("")
WektPrzem=matrix(12,1, [0, 0, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, 0, 0])
WektPrzem
print("")
print("Wyliczenie lewej strony glownego rownania K*Q:")
Lewa=KsztGLOBAL*WektPrzem
Lewa
print("")
print("Wyliczenie prawej strony glownego rownania P+R:")
Prawa=WektReaObc
Prawa
print("")
print("..................................................................WYLICZENIE GLOBALNEGO RÓWNANIA K*Q=P+R................................")
print("")
solve([i==j for i,j in zip(Lewa.list(), Prawa.list())], Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,R1,R2,R11,R12)

sols=solve([i==j for i,j in zip(Lewa.list(), Prawa.list())], R1,R2,R11,R12,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10, solution_dict=True) #zapisuje wyniki operacji solve w postaci słownikowej, a nie symbolicznej
Q3prim=sols[0][Q3].n(prec=20)
Q4prim=sols[0][Q4].n(prec=20)
Q5prim=sols[0][Q5].n(prec=20)
Q6prim=sols[0][Q6].n(prec=20)
Q7prim=sols[0][Q7].n(prec=20)
Q8prim=sols[0][Q8].n(prec=20)
Q9prim=sols[0][Q9].n(prec=20)
Q10prim=sols[0][Q10].n(prec=20)
R1prim=sols[0][R1].n(prec=20)
R2prim=sols[0][R2].n(prec=20)
R11prim=sols[0][R11].n(prec=20)
R12prim=sols[0][R12].n(prec=20)
Q3prim
Q4prim
Q5prim
Q6prim
Q7prim
Q8prim
Q9prim
Q10prim
R1prim
R2prim
R11prim
R12prim
print("")
print("A więc globalny wektor przemieszczeń ma postac:")
WektPrzem_END=matrix(12,1, [0, 0, Q3prim, Q4prim, Q5prim, Q6prim, Q7prim, Q8prim, Q9prim, Q10prim, 0, 0])
WektPrzem_END
print("")
print("Z kolei globalny wektor reakcji ma postac:")
WektReak_END=matrix(12,1, [R1prim, R2prim, 0, 0, 0, 0, 0, 0, 0, 0, R11prim, R12prim])
WektReak_END
︡8b5ad8fe-7bca-4e21-88db-bae61eef7e43︡{"stdout":".................................................................Obciazenia:.............................................................................\n"}︡{"stdout":"\n"}︡{"stdout":"Obliczenia wektora obciazen wezłowych przylozonych na krawedzi elementu nr 3 (trojkata):\n"}︡{"stdout":"\n"}︡{"stdout":"[         0          0      1/2*x          0 -1/2*x + 1          0]\n[         0          0          0      1/2*x          0 -1/2*x + 1]\n"}︡{"stdout":"[         0          0]\n[         0          0]\n[     1/2*x          0]\n[         0      1/2*x]\n[-1/2*x + 1          0]\n[         0 -1/2*x + 1]\n"}︡{"stdout":"[       0]\n[4*x - 16]\n"}︡{"stdout":"Wektor obciazen wezlowych przylozonych na krawedzi elementu nr 3 (trojkata):\n"}︡{"stdout":"[    0]\n[    0]\n[    0]\n[-32/3]\n[    0]\n[-40/3]\n"}︡{"stdout":"\n"}︡{"stdout":"Wektor wiezi podporowych elementu nr 1 (prostokata):\n"}︡{"stdout":"zostanie wyliczony od razu w ukladzie globalnym\n"}︡{"stdout":"Wektor wiezi podporowych elementu nr 2 (trojkata):\n"}︡{"stdout":"jest zerowy\n"}︡{"stdout":"\n"}︡{"stdout":"Wektor obciazen wezłowych el.3 w ukladzie globalnym:\n"}︡{"stdout":"[    0]\n[    0]\n[    0]\n[    0]\n[    0]\n[-32/3]\n[    0]\n[-40/3]\n[    0]\n[    0]\n[    0]\n[    0]\n"}︡{"stdout":"\n"}︡{"stdout":"Globalny wektor obciazen:\n"}︡{"stdout":"[    0]\n[    0]\n[    0]\n[    0]\n[    0]\n[-32/3]\n[    0]\n[-40/3]\n[    0]\n[    0]\n[    0]\n[    0]\n"}︡{"stdout":"\n"}︡{"stdout":"Globalny wektor reakcji:\n"}︡{"stdout":"[ R1]\n[ R2]\n[  0]\n[  0]\n[  0]\n[  0]\n[  0]\n[  0]\n[  0]\n[  0]\n[R11]\n[R12]\n"}︡{"stdout":"\n"}︡{"stdout":"Globalny wektor reakcji+obciazen:\n"}︡{"stdout":"\n"}︡{"stdout":"[   R1]\n[   R2]\n[    0]\n[    0]\n[    0]\n[-32/3]\n[    0]\n[-40/3]\n[    0]\n[    0]\n[  R11]\n[  R12]\n"}︡{"stdout":"Globalny wektor przemieszczen z uwzglednieniem warunkow brzegowych:\n"}︡{"stdout":"\n"}︡{"stdout":"[  0]\n[  0]\n[ Q3]\n[ Q4]\n[ Q5]\n[ Q6]\n[ Q7]\n[ Q8]\n[ Q9]\n[Q10]\n[  0]\n[  0]\n"}︡{"stdout":"\n"}︡{"stdout":"Wyliczenie lewej strony glownego rownania K*Q:\n"}︡{"stdout":"[                                                2163750.0*Q10 + 2279583.333333333*Q3 + 78750.00000000023*Q4 - 3669583.333333334*Q9]\n[                                                               -2467500.0*Q10 - 78749.99999999977*Q3 - 1807500.0*Q4 + 2163750.0*Q9]\n[         2163750.0*Q10 + 17921666.666666664*Q3 - 2163750.0*Q4 - 2085000.0*Q6 - 4170000.0*Q7 + 4327500.0*Q8 - 12361666.666666666*Q9]\n[      -2745000.0*Q10 - 2163750.0*Q3 + 19845000.0*Q4 - 2242499.9999999995*Q5 + 4327500.0*Q7 - 12825000.0*Q8 + 2163749.9999999995*Q9]\n[                                                      -2242499.9999999995*Q4 + 6412500.0*Q5 - 6412500.0*Q7 + 2242499.9999999995*Q8]\n[                                                                        -2085000.0*Q3 + 2085000.0*Q6 + 2085000.0*Q7 - 2085000.0*Q8]\n[                 -2085000.0*Q10 - 4170000.0*Q3 + 4327500.0*Q4 - 6412500.0*Q5 + 2085000.0*Q6 + 10582499.999999998*Q7 - 4327500.0*Q8]\n[4327500.0*Q3 - 12825000.0*Q4 + 2242499.9999999995*Q5 - 2085000.0*Q6 - 4327500.0*Q7 + 14909999.999999998*Q8 - 2242499.9999999995*Q9]\n[                    -2163750.0*Q10 - 12361666.666666666*Q3 + 2163749.9999999995*Q4 - 2242499.9999999995*Q8 + 13751666.666666668*Q9]\n[                                                         7020000.0*Q10 + 2163750.0*Q3 - 2745000.0*Q4 - 2085000.0*Q7 - 2163750.0*Q9]\n[                                               -78750.00000000023*Q10 - 3669583.333333334*Q3 - 2163750.0*Q4 + 2279583.333333333*Q9]\n[                                                               -1807500.0*Q10 - 2163750.0*Q3 - 2467500.0*Q4 + 78749.99999999977*Q9]\n"}︡{"stdout":"\n"}︡{"stdout":"Wyliczenie prawej strony glownego rownania P+R:\n"}︡{"stdout":"[   R1]\n[   R2]\n[    0]\n[    0]\n[    0]\n[-32/3]\n[    0]\n[-40/3]\n[    0]\n[    0]\n[  R11]\n[  R12]\n"}︡{"stdout":"\n"}︡{"stdout":"..................................................................WYLICZENIE GLOBALNEGO RÓWNANIA K*Q=P+R................................\n"}︡{"stdout":"\n"}︡{"stdout":"[[Q3 == (18912404194849/1329447841802666250), Q4 == (-24383512273927/1994171762703999375), Q5 == (7108823022984623/184793250010570608750), Q6 == (-95333277620347/2217519000126847305), Q7 == (6969262608033263/184793250010570608750), Q8 == (-28690103361127/1994171762703999375), Q9 == (17724861556957/1329447841802666250), Q10 == (12253753477879/1994171762703999375), R1 == (-5093723987739901868702530561/1223557500488621406289920000), R2 == (65981471152822987570821968283/1903311667869893690385208750), R11 == (35656067914179276443651962121/8564902503420349844029440000), R12 == (-20301991123945538605729412319/1903311667869893690385208750)]]\n"}︡{"stdout":"0.000014226\n"}︡{"stdout":"-0.000012227\n"}︡{"stdout":"0.000038469\n"}︡{"stdout":"-0.000042991\n"}︡{"stdout":"0.000037714\n"}︡{"stdout":"-0.000014387\n"}︡{"stdout":"0.000013332\n"}︡{"stdout":"6.1448e-6\n"}︡{"stdout":"-4.1630\n"}︡{"stdout":"34.667\n"}︡{"stdout":"4.1630\n"}︡{"stdout":"-10.667\n"}︡{"stdout":"\n"}︡{"stdout":"A więc globalny wektor przemieszczeń ma postac:\n"}︡{"stdout":"[     0.00000]\n[     0.00000]\n[ 0.000014226]\n[-0.000012227]\n[ 0.000038469]\n[-0.000042991]\n[ 0.000037714]\n[-0.000014387]\n[ 0.000013332]\n[   6.1448e-6]\n[     0.00000]\n[     0.00000]\n"}︡{"stdout":"\n"}︡{"stdout":"Z kolei globalny wektor reakcji ma postac:\n"}︡{"stdout":"[-4.1630]\n[ 34.667]\n[0.00000]\n[0.00000]\n[0.00000]\n[0.00000]\n[0.00000]\n[0.00000]\n[0.00000]\n[0.00000]\n[ 4.1630]\n[-10.667]\n"}︡{"done":true}
︠b2b93a17-baf6-4675-98ff-e801a4d827c4s︠
print("..................................................................REEMIGRACJA DO ELEMENTU NR 1 - PROSTOKAT................................")
print("")
print("Wektor przemieszczeń wezlow el nr 1 w ukladzie lokalnym:")
WektPrzem_el1_LOK_END=matrix(8,1, [0, 0, 0, 0, Q3prim, Q4prim, Q9prim, Q10prim])
WektPrzem_el1_LOK_END
print("")
print("Wyznaczenie tensora odkształceń elementu nr 1 - prostokat; e=B_lok*Q_lok:")
Tensor_e=Bpio*WektPrzem_el1_LOK_END
Tensor_e
print("")
print("podstawmy wspolrzedne srodka elementu; x=0 oraz y=0; wzgl. lok. ukl wspolrzednych do macierzy B_lok:")
Bpio.substitute(x=0,y=0)#bo liczymy oksztalcenia w srodku elementu, a przy wyprowadzaniu macierzy sztywności przyjelismy uklad lokalny wlasnie w srodku
print("")
Tensor_e=Bpio.substitute(x=0,y=0)*WektPrzem_el1_LOK_END
print("Ostatecznie tensor oksztalcen elementu nr 1 przyjmie postac:")
Tensor_e
print("")
print("Teraz mozemy policzyc tensor naprezen elementu nr 1; Tensor_sigma=D*e")
Tensor_sigma=Dpio*Tensor_e*1000
Tensor_sigma.n(prec=15)
print("WYNIK W MPa !!")
︡04c75d9a-5e82-4d4d-b62f-b778df4828f6︡{"stdout":"..................................................................REEMIGRACJA DO ELEMENTU NR 1 - PROSTOKAT................................\n"}︡{"stdout":"\n"}︡{"stdout":"Wektor przemieszczeń wezlow el nr 1 w ukladzie lokalnym:\n"}︡{"stdout":"[     0.00000]\n[     0.00000]\n[     0.00000]\n[     0.00000]\n[ 0.000014226]\n[-0.000012227]\n[ 0.000013332]\n[   6.1448e-6]\n"}︡{"stdout":"\n"}︡{"stdout":"Wyznaczenie tensora odkształceń elementu nr 1 - prostokat; e=B_lok*Q_lok:\n"}︡{"stdout":"[                 (1.4888e-7)*y + 2.2332e-7]\n[                -(3.0620e-6)*x - 1.0138e-6]\n[(1.4888e-7)*x - (3.0620e-6)*y + 1.8190e-12]\n"}︡{"stdout":"\n"}︡{"stdout":"podstawmy wspolrzedne srodka elementu; x=0 oraz y=0; wzgl. lok. ukl wspolrzednych do macierzy B_lok:\n"}︡{"stdout":"[-1/4    0  1/4    0  1/4    0 -1/4    0]\n[   0 -1/6    0 -1/6    0  1/6    0  1/6]\n[-1/6 -1/4 -1/6  1/4  1/6  1/4  1/6 -1/4]\n"}︡{"stdout":"\n"}︡{"stdout":"Ostatecznie tensor oksztalcen elementu nr 1 przyjmie postac:\n"}︡{"stdout":"[ 2.2332e-7]\n[-1.0138e-6]\n[1.8190e-12]\n"}︡{"stdout":"\n"}︡{"stdout":"Teraz mozemy policzyc tensor naprezen elementu nr 1; Tensor_sigma=D*e\n"}︡{"stdout":"[-0.01122]\n[-0.08000]\n[5.057e-8]\n"}︡{"stdout":"WYNIK W MPa !!\n"}︡{"done":true}
︠fc2dfc3a-cdff-4b81-ab25-bc489e5c54e0︠
print("..................................................................REEMIGRACJA DO ELEMENTU NR 2 - TROJKAT.......................................................................")
print("")
print("Wektor przemieszczeń wezlow el nr 2 w ukladzie lokalnym:")
WektPrzem_el2_LOK_END=matrix(6,1, [Q7prim, Q8prim, Q9prim, Q10prim, Q3prim, Q4prim])
WektPrzem_el2_LOK_END
print("")
print("Wyznaczenie tensora odkształceń elementu nr 2 - trojkat; e2=B_lok2*Q_lok2:")
Tensor_e2=Bpiot*WektPrzem_el2_LOK_END
Tensor_e2
print("")
print("podstawmy wspolrzedne srodka elementu; x=-2/3 oraz y=-4/3; wzgl. lok. ukl wspolrzednych do macierzy B_lok:")
Bpiot.substitute(x=-2/3,y=-4/3)#bo liczymy oksztalcenia w srodku elementu, a przy wyprowadzaniu macierzy sztywności przyjelismy PRAWYM, GORNYM ROGU TROJKATA
print("")
Tensor_e2=Bpiot.substitute(x=-2/3,y=-4/3)*WektPrzem_el2_LOK_END
print("Ostatecznie tensor oksztalcen elementu nr 2 przyjmie postac:")
Tensor_e2
print("")
print("Teraz mozemy policzyc tensor naprezen elementu nr 2; Tensor_sigma2=D2*e2")
Tensor_sigma2=Dpiot*Tensor_e2*1000
Tensor_sigma2.n(prec=15)
print("WYNIK W MPa !!")
print("")
︡316fab7b-5e79-4e89-b773-fce115ea81d7︡{"stdout":"..................................................................REEMIGRACJA DO ELEMENTU NR 2 - TROJKAT.......................................................................\n"}︡{"stdout":"\n"}︡{"stdout":"Wektor przemieszczeń wezlow el nr 2 w ukladzie lokalnym:\n"}︡{"stdout":"[ 0.000037714]\n[-0.000014387]\n[ 0.000013332]\n[   6.1448e-6]\n[ 0.000014226]\n[-0.000012227]\n"}︡{"stdout":"\n"}︡{"stdout":"Wyznaczenie tensora odkształceń elementu nr 2 - trojkat; e2=B_lok2*Q_lok2:\n"}︡{"stdout":"[ 4.4663e-7]\n[-1.0798e-6]\n[ 2.5579e-6]\n"}︡{"stdout":"\n"}︡{"stdout":"podstawmy wspolrzedne srodka elementu; x=-2/3 oraz y=-4/3; wzgl. lok. ukl wspolrzednych do macierzy B_lok:\n"}︡{"stdout":"[   0    0 -1/2    0  1/2    0]\n[   0  1/2    0    0    0 -1/2]\n[ 1/2    0    0 -1/2 -1/2  1/2]\n"}︡{"stdout":"\n"}︡{"stdout":"Ostatecznie tensor oksztalcen elementu nr 2 przyjmie postac:\n"}︡{"stdout":"[ 4.4663e-7]\n[-1.0798e-6]\n[ 2.5579e-6]\n"}︡{"stdout":"\n"}︡{"stdout":"Teraz mozemy policzyc tensor naprezen elementu nr 2; Tensor_sigma2=D2*e2\n"}︡{"stdout":"[0.005901]\n[-0.07897]\n[ 0.07111]\n"}︡{"stdout":"WYNIK W MPa !!\n"}︡{"stdout":"\n"}︡{"done":true}︡
︠ce8969df-a935-4e45-8c68-765c9683ee80s︠
print("..................................................................REEMIGRACJA DO ELEMENTU NR 3 - TROJKAT.......................................................................")
print("")
print("Wektor przemieszczeń wezlow el nr 3 w ukladzie lokalnym:")
WektPrzem_el3_LOK_END=matrix(6,1, [Q3prim, Q4prim, Q5prim, Q6prim, Q7prim, Q8prim])
WektPrzem_el3_LOK_END
print("")
print("Wyznaczenie tensora odkształceń elementu nr 3 - trojkat; e3=B_lok3*Q_lok3:")
Tensor_e3=Bpiot3*WektPrzem_el3_LOK_END
Tensor_e3
print("")
print("podstawmy wspolrzedne srodka elementu; x=2/3 oraz y=4/3; wzgl. lok. ukl wspolrzednych do macierzy B_lok3:")
Bpiot3.substitute(x=0,y=0)#bo liczymy oksztalcenia w srodku elementu, a przy wyprowadzaniu macierzy sztywności przyjelismy LEWYM DOLNYM ROGU TROJKATA
print("")
Tensor_e3=Bpiot3.substitute(x=1/3,y=4/3)*WektPrzem_el3_LOK_END
print("Ostatecznie tensor oksztalcen elementu nr 3 przyjmie postac:")
Tensor_e3
print("")
print("Teraz mozemy policzyc tensor naprezen elementu nr 3; Tensor_sigma3=D3*e3")
Tensor_sigma3=Dpiot3*Tensor_e3*1000
Tensor_sigma3.n(prec=15)
print("WYNIK W MPa !!")
print("")
print("....................................................................KONIEC OBLICZEN !...........................................................................................")
print("")
︡879beb49-2f40-4fe6-b2cf-f16d383b0353︡{"stdout":"..................................................................REEMIGRACJA DO ELEMENTU NR 3 - TROJKAT.......................................................................\n"}︡{"stdout":"\n"}︡{"stdout":"Wektor przemieszczeń wezlow el nr 3 w ukladzie lokalnym:\n"}︡{"stdout":"[ 0.000014226]\n[-0.000012227]\n[ 0.000038469]\n[-0.000042991]\n[ 0.000037714]\n[-0.000014387]\n"}︡{"stdout":"\n"}︡{"stdout":"Wyznaczenie tensora odkształceń elementu nr 3 - trojkat; e3=B_lok3*Q_lok3:\n"}︡{"stdout":"[ 3.7759e-7]\n[-1.0798e-6]\n[-2.5580e-6]\n"}︡{"stdout":"\n"}︡{"stdout":"podstawmy wspolrzedne srodka elementu; x=2/3 oraz y=4/3; wzgl. lok. ukl wspolrzednych do macierzy B_lok3:\n"}︡{"stdout":"[   0    0  1/2    0 -1/2    0]\n[   0 -1/2    0    0    0  1/2]\n[-1/2    0    0  1/2  1/2 -1/2]\n"}︡{"stdout":"\n"}︡{"stdout":"Ostatecznie tensor oksztalcen elementu nr 3 przyjmie postac:\n"}︡{"stdout":"[ 3.7759e-7]\n[-1.0798e-6]\n[-2.5580e-6]\n"}︡{"stdout":"\n"}︡{"stdout":"Teraz mozemy policzyc tensor naprezen elementu nr 3; Tensor_sigma3=D3*e3\n"}︡{"stdout":"[-1.688e-6]\n[ -0.08103]\n[ -0.07111]\n"}︡{"stdout":"WYNIK W MPa !!\n"}︡{"stdout":"\n"}︡{"stdout":"....................................................................KONIEC OBLICZEN !...........................................................................................\n"}︡{"stdout":"\n"}︡{"done":true}
︠451ad1d3-bd73-4fb0-8580-039ac81bbdb8︠
︡4d5937fa-a147-4115-b94c-1731d746282c︡{"done":true}










eq = 13
ep = 10

seedbytes = 32
noise_seedbytes = 32

n = 256

LightSaber = False
#LightSaber = True
Saber      = False
#Saber      = True
#FireSaber  = False
FireSaber  = True

if LightSaber:
    l = 2
    et = 3
    mu = 10

elif Saber:
    l = 3
    et = 4
    mu = 8

elif FireSaber:
    l = 4
    et = 6
    mu = 6

p = 2 ** ep
q = 2 ** eq
t = 2 ** et

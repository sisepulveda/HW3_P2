import numpy as np
from quad4_2t import quad4, quad4_post
from scipy.sparse import csr_matrix, csc_matrix, lil_matrix, coo_matrix
from scipy.sparse.linalg import spsolve
fid = open("placa_plana_b.msh", "r")

LINE_ELEMENT = 1
TRI_ELEMENT = 2
QUAD_ELEMENT = 3

Empotrado = 1
BordeNatural = 2
Placa = 3
Extremos = 4

while True:
    line = fid.readline()

    if line.find("$Nodes") >= 0:
        break

Nnodes = int(fid.readline())

xy = lil_matrix(np.zeros([Nnodes, 2]))

print(0)

for i in range(Nnodes):
    line = fid.readline()
    sl = line.split()
    xy[i, 0] = float(sl[1])
    xy[i, 1] = float(sl[2])

while True:
    line = fid.readline()

    if line.find("$Elements") >= 0:
        break

Nelements = int(fid.readline())

conec = np.zeros((Nelements, 4), dtype=np.int32)

fixed_nodes = []

Nquads = 0
Quadrangles = []
QExt = []
nodos_borde_nat = []
tipo = []

for i in range(Nelements):
    line = fid.readline()
    sl = line.split()
    element_number = np.int32(sl[0]) -1
    element_type = np.int32(sl[1])
    physical_grp = np.int32(sl[3])
    entity_number = np.int32(sl[4])


    if element_type == LINE_ELEMENT and \
            physical_grp == Empotrado: #linea
        n1 = np.int32(sl[5]) - 1
        n2 = np.int32(sl[6]) - 1
        fixed_nodes += [n1, n2]

    if element_type == LINE_ELEMENT and \
            physical_grp == BordeNatural:
        n1 = np.int32(sl[5]) - 1
        n2 = np.int32(sl[6]) - 1
        nodos_borde_nat.append([n1, n2])

    if element_type == QUAD_ELEMENT and \
            (physical_grp == Placa or physical_grp == Extremos):
        n0 = np.int32(sl[5]) - 1
        n1 = np.int32(sl[6]) - 1
        n2 = np.int32(sl[7]) - 1
        n3 = np.int32(sl[8]) - 1
        tipo.append(physical_grp)
        conec[element_number, :] = [n0, n1, n2, n3]
        if physical_grp == Extremos:
            QExt.append(element_number)
        Quadrangles.append(element_number)
        Nquads += 1


#print(f"Nnodes = {Nnodes}")
#print(conec)
#print(f"Ntriangles = {Ntriangles}")
NDOFs = 2*Nnodes

properties = {}

rho = 2500.
g = 9.81

properties["E"] = 20e9
properties["nu"] = .25
properties["bx"] = 0.
properties["by"] = 0.
properties["t1"] = 4e-3
properties["t2"] = 5e-3

K = lil_matrix(np.zeros((NDOFs, NDOFs)))
f = lil_matrix(np.zeros((NDOFs, 1)))
espesor = 0.
fact = 0

for e in Quadrangles:
    ni = conec[e,0]
    nj = conec[e,1]
    nk = conec[e,2]
    nl = conec[e,3]

    #print(f"e = {e} ni = {ni} nj = {nj}  nk = {nk}")

    xy_e = xy[[ni, nj, nk, nl], :]

    if tipo[fact] == Placa:
        espesor = 4e-3
    else:
        espesor = 5e-3
    properties["t"] = espesor
    fact += 1
    ke, fe = quad4(xy_e, properties, QExt, Nelements)

    #print(f"e = {e} ke = {ke}")

    # Node k ---> [ 3*k, 3*k+1, 3+k+2 ]

    d = [2*ni, 2*ni+1, 2*nj, 2*nj+1, 2*nk, 2*nk+1, 2*nl, 2*nl+1]    #global DOFS from local DOFS

    #Direct stiffness method
    for i in range(8):
        p = d[i]
        for j in range(8):
            q = d[j]
            K[p, q] += ke[i, j]
        f[p] += fe[i]
f = f.toarray()
#########################################################
properties_load = {}
properties_load["t"] = properties["t2"]
properties_load["tx"] = 1000/((properties_load["t"])*4)
properties_load["ty"] = 0.
from nodal_loads import nodal_loads
#print(nodos_borde_nat)
for nn in nodos_borde_nat:
    ni = nn[0]
    nj = nn[1]

    xy_e = xy[[ni,nj], :]
    xy_e = xy_e.toarray()

    #print(f"ni = {ni}; nj = {nj}; xy_e = {xy_e}")

    fe = nodal_loads(xy_e, properties_load)
    d = [2*ni, 2*ni+1, 2*nj, 2*nj+1]    #global DOFS from local DOFS
    for i in range(4):
        p = d[i]
        f[p] += fe[i]
#print(f"f = {f}")
################################################################################

fixed_nodes = np.unique(fixed_nodes)
print(4)

constrained_DOFs = []

for n in fixed_nodes:
    constrained_DOFs += [2*n, 2*n+1]

free_DOFs = np.arange(NDOFs)
free_DOFs = np.setdiff1d(free_DOFs, constrained_DOFs)

#print(f"fixed_nodes = {fixed_nodes}")
#print(f"constrained_DOFs = {constrained_DOFs}")
#print(f"free_DOFs = {free_DOFs}")

import matplotlib.pylab as plt

print(5)

#for i in range(NDOFs):
    #if abs(K[i,i]) < 1e-8:
        #print(f"i = {i}; K[i,i] = {K[i,i]}")

print(6)
#plt.matshow(K)
#plt.show()

#SOLUCION
Kff = csc_matrix(K[np.ix_(free_DOFs, free_DOFs)])
Kfc = lil_matrix(K[np.ix_(free_DOFs, constrained_DOFs)])
Kcf = lil_matrix(K[np.ix_(constrained_DOFs, free_DOFs)])
Kcc = lil_matrix(K[np.ix_(constrained_DOFs, constrained_DOFs)])

ff = csc_matrix(f[free_DOFs])
fc = lil_matrix(f[constrained_DOFs])

print(7)

# Solve
from scipy.linalg import solve
u = csc_matrix(np.zeros((NDOFs, 1)))

print(8)

u[free_DOFs] = spsolve(Kff, ff)

print(9)
u = u.tolil()
Kff = Kff.tolil()
ff = ff.tolil()
print(10)

#Get reaction forces
R = Kcf @ u[free_DOFs] + Kcc @ u[constrained_DOFs] - fc

print(11)
#print(f"u = {u}")
#print(f"R = {R}")

factor = 2e6

u = u.toarray()
uv = u.reshape([-1,2])
xy = xy.toarray()
#plt.plot(xy[:,0] + factor*uv[:,0], xy[:,1] + factor*uv[:,1], ".")
xy = lil_matrix(xy)
u = lil_matrix(u)
uv = lil_matrix(uv)

#plt.plot(xy[:,0], xy[:,1], ".")

#plt.plot(xy[:,0] + factor*uv[:,0], xy[:,1] + factor*uv[:,1], ".")
co = lil_matrix(conec)
for e in Quadrangles: #range(1,Nelements):
    ni = co[e,0]
    nj = co[e,1]
    nk = co[e,2]
    nl = co[e,3]
    #xy_e = xy[[ni, nj, nk, nl, ni], :]  #estatico
    xy_e = xy[[ni, nj, nk, nl, ni], :] + factor*uv[[ni, nj, nk, nl, ni], :]    #def

    xy_e = xy_e.toarray()
    a = xy_e[:,0]
    b = xy_e[:,1]

    plt.plot(a, b, "k")


plt.axis("equal")
plt.show()

print(12)


from gmsh_post import write_node_data, write_node_data_2, write_element_data

uv = uv.toarray()

nodes = np.arange(1, Nnodes+1)
write_node_data("uxMP.msh", nodes, uv[:,0], "Despl. X")
write_node_data("uyMP.msh", nodes, uv[:,1], "Despl. Y")
write_node_data_2("desplMP.msh", nodes, uv[:,0], uv[:,1], "Despl")

print(10)
#Calculo de Tensiones

uv = lil_matrix(uv)
sigmaxx = np.zeros(Nquads+1)
sigmayy = np.zeros(Nquads+1)
sigmaxy = np.zeros(Nquads+1)

print(11)

i = 0
for e in Quadrangles: #range(1,Nelements):

    ni = co[e,0]
    nj = co[e,1]
    nk = co[e,2]
    nl = co[e,3]

    xy_e = xy[[ni, nj, nk, nl, ni], :]
    uv_e = uv[[ni, nj, nk, nl], :]    #def
    uv_e = uv_e.toarray()
    u_e = uv_e.reshape((-1))
    uv_e = lil_matrix(uv_e)

    xy_e = xy_e.toarray()
    #u_e = u_e.todense()

    epsilon_e, sigma_e = quad4_post(xy_e, u_e, properties)

    print(f"sigma_e = {sigma_e}")
    sigmaxx[i] = sigma_e[0]
    sigmayy[i] = sigma_e[1]
    sigmaxy[i] = sigma_e[2]

    i += 1


u_e = lil_matrix(u_e)
xy_e = lil_matrix(xy_e)
print(12)

elementos = np.array(Quadrangles)+1

#sigmaxx = sigmaxx.toarray()
write_element_data("sigma_xMP.msh", elementos, sigmaxx, "Sigma_x")

print(13)

despl = []
NN = len(nodes)
#print(NN)
for q in range(NN):
    desplA = ((uv[q,0]**2) + (uv[q,1]**2))**0.5
    despl.append(desplA)
print(14)

#print(f"sigmaxx1_1 = {max(sigmaxx)}")
#print(f"despl1_1 = {max(despl)}")
#print(f"desply1_1 ={min(uv[:,1])}")
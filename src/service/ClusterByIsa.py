import numpy as np
from src.Exceptions import ComplexError


# Die Funktion cluster_by_isa klassifiziert dynamische Daten anhand von NoOfClus
# Eigenvektoren (Evs) der Uebergangsmatrix. NoOfClus (default=2) legt dabei
# fest, wieviele Cluster es geben soll. Die verwendete Methode: Inner Simplex
# Algorithmus.
#
# Restriktion: Evs muss mindestens NoOfClus Eigenvektoren beinhalten.
#
# Beispiele:
#
# cluster_by_isa(Evs,NoOfClus)
# --> Ausgabe: Gibt einen Vektor cF aus, der zu jeder Zeile der Uebergangsmatrix
#              eine Clusterzuordnung vornimmt.
#
# [Chi, ind] = cluster_by_isa(Evs,NoOfClus)
# --> Ausgabe: Gibt einen Vektor cF aus, der zu jeder Zeile der Uebergangsmatrix
#              eine Clusterzuordnung vornimmt.
#
# [cF, indic, Chi, RotMat] = cluster_by_isa (Evs, NoOfClus)
# --> Ausgabe:  cF ist wieder der Zuordnungsvektor. indic liefert den Indikator
#               fuer die Eindeutigkeit der Zuordnung. Dieser Zahlenwert sollte
#               ungefaehr Null sein. Chi gibt fuer jeden Cluster einen Vektor von
#               Zugehoerigkeitsgraden im Sinne der Fuzzy-Theorie an.
#               RotMat ist diejenige lineare Transformation, die Evs in Chi
#               ueberfuehrt, sie sollte eine wohlkonditionierte Matrix sein.
#               ind gibt die Eckenindizes aus
def get_chi(q: np.ndarray) -> np.ndarray:
    evs = isa_preparation(q)
    no_of_clus = 2
    # end
    #
    # Eigentlicher
    # ISA - Algorithmus
    #
    c = evs[:, 0:no_of_clus]  # C = Evs(:, 1:NoOfClus);
    ortho_sys = c.copy()  # OrthoSys = C;
    maxdist = 0.0  # maxdist = 0.0;
    #
    # Erste beiden Repraesentanten
    # mit maximalem Abstand
    #
    ind = np.zeros(no_of_clus)
    ind = ind.astype(int)
    # for i=1:size(Evs, 1)
    for i in range(0, evs.shape[0]):
        # if norm(C(i,: )) > maxdist
        if np.linalg.norm(c[i, :]) > maxdist:
            maxdist = np.linalg.norm(c[i, :])  # maxdist = norm(C(i,:));
            ind[0] = i  # ind(1) = i;
        # end
    # end
    # for i=1:size(Evs, 1)
    for i in range(0, evs.shape[0]):
        ortho_sys[i, :] = ortho_sys[i, :] - c[ind[0], :]  # OrthoSys(i,:)=OrthoSys(i,:)-C(ind(1),:);
    # end
    #
    # Weitere Repraesentanten ueber
    # Gram - Schmidt Orthogonalisierung
    #
    # for k = 2:NoOfClus
    maxdist = 0.0  # maxdist = 0.0;
    temp = ortho_sys[ind[0], :]  # temp = OrthoSys(ind(k - 1),:);
    # for i=1:size(Evs, 1)
    for i in range(0, evs.shape[0]):
        # OrthoSys(i,:)=OrthoSys(i,:)-(temp * transpose(OrthoSys(i,:)))*temp;
        ortho_sys[i, :] = ortho_sys[i, :] - (temp * ortho_sys[i, :].T) * temp
        distt = np.linalg.norm(ortho_sys[i, :])  # distt = norm(OrthoSys(i,:));
        # if distt > maxdist
        if distt > maxdist:
            maxdist = distt  # maxdist = distt;
            ind[1] = i  # ind(k) = i;
        # end
    # end
    rot_mat = np.linalg.inv(c[ind, :])  # RotMat = inv(C(ind,:));
    chi = np.dot(c, rot_mat)  # Chi = C * RotMat;
    return chi


def isa_preparation(u: np.ndarray) -> np.ndarray:
    eigval, tmp = np.linalg.eig(u.T)

    min_ind = np.argmin(eigval)
    max_ind = np.argmax(eigval)
    # min_ind, max_ind = get_maxmin_real(eigval)
    ind = np.argmin(tmp[min_ind, :] * tmp[max_ind, :])
    if tmp[:, ind].all().imag or tmp[min_ind, ind].imag != 0:
        raise ComplexError('eigvec in isa_preparation has an imaginary part')
    evs = np.ones([tmp.shape[0], 2])
    evs[:, 1] = tmp[:, ind].real * np.sign(tmp[min_ind, ind].real)
    return evs

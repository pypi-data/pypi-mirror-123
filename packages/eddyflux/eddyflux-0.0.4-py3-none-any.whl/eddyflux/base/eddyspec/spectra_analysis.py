import numpy as np
import pandas as pd
from copy import deepcopy
from functools import reduce
from .specutils import numlist2arr

def SelectStructure(data, bins):
    data = deepcopy(data)
    binidx = np.where(bins != 99)[0]
    if isinstance(data, pd.DataFrame):
        return data.iloc[binidx, :]
    elif isinstance(data, dict):
        data_out = {}
        for key, val in data.items():
            if isinstance(val, pd.Series):
                data_out[key] = val[binidx]
            elif isinstance(val, pd.DataFrame):
                data_out[key] = val.iloc[binidx, :]
            elif isinstance(val, np.ndarray):
                data_out[key] = val[binidx, :]
            else:
                raise(Exception('Wrong type!'))
        return data_out
    else:
        raise(Exception('None correct type of data!'))

def CalcLambda(Gas, LPM, IR, P):
    # --------- Lambda value for tube attenuation --------------------
    # P     = tube pressure
    # LPM   = flow rate       (low limit of 0.1 lpm)
    # IR    = tube internal radius  (low limit of 0.000005 m)
    # Gas   = 'CO2', 'CH4', 

    LPM = numlist2arr(LPM)
    IR = numlist2arr(IR)
    P = numlist2arr(P)
    
    U  = LPM / (1000 * 60 * np.pi * IR**2)
    v  = (3.719815 - (0.0358737 * P) + (0.0001342 * P**2)) / 100000
    Re = (2 * IR * U) / v

    Dif = np.ones(U.shape)
    D0 = np.ones(U.shape)
    Da = np.ones(U.shape)
    Db = np.ones(U.shape)
    Dc = np.ones(U.shape)
    Dd = np.ones(U.shape)
    if Gas == 'CO2':
        Dif = Dif * 0.0000139
        D0  = D0 * 0.977616284023198
        Da  = Da * -40511.5062176583
        Db  = Db * 742694287.9160520
        Dc  = Dc * -3394928055533.75
        Dd  = Dd * 4991471292069380.0
    elif Gas == 'H2O':
        Dif = Dif * 0.0000239     
        D0  = D0 * 0.490851295350703
        Da  = Da * -12093.7897865916
        Db  = Db * 325341636.671577
        Dc  = Dc * -1502053321310.87
        Dd  = Dd * 2244127770065660.0
    elif Gas == 'CH4':
        Dif = Dif * 0.0000239
        D0  = D0 * 0.523609894456971
        Da  = Da * -13944.2741193251
        Db  = Db * 352263929.4320020
        Dc  = Dc * -1621482983243.50
        Dd  = Dd * 2416389615565820.0
    else:
        Dif = Dif * 0.0000239
        D0  = D0 * 0.977616284023198
        Da  = Da * -40511.5062176583
        Db  = Db * 742694287.9160520
        Dc  = Dc * -3394928055533.75
        Dd  = Dd * 4991471292069380.0

    idL = np.where(Re <= 2300)
    idT = np.where(Re >  2300)


    Lam = np.ones(U.shape)

    # calc non-turbulent lambda
    Lam[idL] = (0.0104 * v[idL] * Re[idL]) / Dif[idL]

    # calc turbulent lambda
    Lam[idT] = D0[idT] + Da[idT] / Re[idT] + Db[idT] / Re[idT]**2 + Dc[idT] / Re[idT]**3 + Dd[idT] / Re[idT]**4

    return [Lam, U, Re]

def TubeAtten(Gas,P,LPM,L,ID):
    # --------- Frequency response correction --------------------
    #  P     = tube pressure
    #  LPM   = flow rate       (low limit of 0.1 lpm)
    #  L     = tube length, m  (low limit of 0.1 m)
    #  ID    = tube internal diameter  (low limit of 0.00001 m)
    #  Gas   = 'CO2', 'CH4', 
    LPM = np.array(LPM)
    L = np.array(L)
    ID = np.array(ID)
    
    d4pi2  = (2 * 3.14159265)**2
    LPM[LPM <= 0.0] = 0.1
    L[L <= 0.0] = 0.1
    ID[ID <= 0.0] = 0.00001
    IR = ID / 2
    [Lam, U, Re] = CalcLambda(Gas, LPM, IR, P)
    Tatten = (d4pi2 * Lam * L * IR) / (U * U)
    return Tatten

def FreqResp2(Modelo, F, Zo, Do, Uo, ZLo, RLo, SSo, Pv1o, Pv2o, Ps1o, Ps2o, Tau1o, Tau2o, G1o, G2o):
    # --------- Frequency response correction --------------------
    #  Modelo = spectral type can be 'U', 'V', 'W', 'X', 'UW','UX' or 'WX'
    #  F     = frequency                (NxM vector)
    #  Zo    = height                   (Nx1 vector)
    #  Do    = zero plane displacement  (Nx1 vector)
    #  Uo    = wind speed               (Nx1 vector)
    #  ZLo   = stability                (Nx1 vector)
    #  RLo   = run length               (Nx1 vector)
    #  Pvo   = vector path length       (Nx1 vector)
    #  Pso   = scalar path length       (Nx1 vector)
    #  Tau1o = time constant            (Nx1 vector)
    #  Tau2o = time constant            (Nx1 vector)
    #  Go    = tube atten coef          (Nx1 vector)
    #  SSo   = sensor separation        (Nx1 vector)
    
    def repeat2vector(val, c1):
        val = numlist2arr(val).reshape(-1, 1)
        return np.tile(val, (1, c1))

    if F.ndim == 1: F = F.reshape(1, -1)
    [r1, c1] = F.shape
    
    Z = repeat2vector(Zo, c1)
    D = repeat2vector(Do, c1)
    U = repeat2vector(Uo, c1)
    ZL = repeat2vector(ZLo, c1)
    RL = repeat2vector(RLo, c1)
    Pv1 = repeat2vector(Pv1o, c1)
    Pv2 = repeat2vector(Pv2o, c1)
    Ps1 = repeat2vector(Ps1o, c1)
    Ps2 = repeat2vector(Ps2o, c1)
    Tau1 = repeat2vector(Tau1o, c1)
    Tau2 = repeat2vector(Tau2o, c1)
    G1 = repeat2vector(G1o, c1)
    G2 = repeat2vector(G2o, c1)
    SS = repeat2vector(SSo, c1)
    
    # calculate spectra
    Zi = 1000 * np.ones(Z.shape)
    Spec =  VectorModelSpectra(Modelo,F,ZL,U,Z,D,Zi)

    # calculate frequency response curve
    # BlockAvg
    A  = np.pi * F * RL * 60
    FR = 1 - (np.sin(A) / A)**2
    
    # Scalar Path 1
    if np.min(Ps1) > 0:
        A  = 2.0 * np.pi * F * Ps1 / U
        B  = np.exp(-1.0 * A)
        C  = (3 + B - (4 / A) * (1-B)) / A
        FR = FR * np.sqrt(C)
    # Scalar Path2
    if np.min(Ps2) > 0:
        A  = 2.0 * np.pi * F * Ps2 / U
        B  = np.exp(-1.0 * A)
        C  = (3 + B - (4 / A) * (1 - B)) / A
        FR = FR * np.sqrt(C)

    # Vector Path 1
    if np.min(Pv1) > 0:
        A = 2 * np.pi * F * Pv1 / U
        B = np.exp(-1 * A)
        C = (2 / A) * (2 + B - (3 * (1 - B) / A))
        FR = FR * np.sqrt(C)

    # Vector Path 2
    if np.min(Pv2) > 0:
        A = 2 * np.pi * F * Pv2 / U
        B = np.exp(-1 * A)
        C = (2 / A) * (2 + B - (3 * (1 - B) / A))
        FR = FR * np.sqrt(C)

    # Time Response 1
    if np.min(Tau1) > 0:
        A  = (2 * np.pi * F * Tau1)**2
        FR = FR * (1 / np.sqrt(1 + A))
 
    # Time Response 2
    if np.min(Tau2) > 0:
        A  = (2 * np.pi * F * Tau2)**2
        FR = FR * (1 / np.sqrt(1 + A))

    # Time Response differences
    if (np.min(Tau1) > 0) & (np.min(Tau2) > 0):
        A  = (2 * np.pi * F)**2
        FR = FR * ((1 + A * Tau1 * Tau2) / (np.sqrt(1 + A * Tau1**2) * np.sqrt(1 + A * Tau2**2)))

    # Tube Attenuation 1
    if np.min(G1) > 0:
        A = (F)**2
        B = np.exp(-1 * G1 * A)
        # If (B < 0.0000000001) Then B := 0.0000000001;
        FR = FR * B

    # Tube Attenuation 2
    if np.min(G2) > 0:
        A = (F)**2
        B = np.exp(-1 * G2 * A)
        # If (B < 0.0000000001) Then B := 0.0000000001;
        FR = FR * B

    # Sensor Separation
    if np.min(SS) > 0:
        A  = F * SS / U
        #  If (dA > 4.0) Then  dA := 4.0;
        if (A <= 4).all(): # ASK TIM, all or any?
            B = np.exp(-9.9 * A**1.5)
            FR = FR * B
    #
    SpecAtten = Spec * FR
    FRcor =  np.trapz(Spec, np.log(F)) / np.trapz(SpecAtten, np.log(F))

    return [FRcor, F, Spec, SpecAtten, FR]

def VectorModelSpectra(model,freq,ZOL,U,Z,Dz,Zi):
    # ------------------------------------------------------------------------
    #   S =  ModelSpectra(type,freq,ZOL,U,Z,Zi);

    #   ModelSpectra returns an array holding Kaimal model spectra or cospectra 
    #     passed parameters are:
    #         model  -  can be 'U', 'V', 'W', 'X', 'UW','UX' or 'WX'
    #         freq   - a vector of natural frequency values for which spectra
    #                  will be calculated
    #         ZOL    - Monin-Obhukov stability
    #           U    - Wind speed  in m/s
    #           Z    - Sensor height in m 
    #           Dz   - Canopy zero plane displacement in m
    #           Zi   - Boundary layer height in m

    # ------------------------------------------------------------------------
    
    # if (freq.ndim == 2) & (np.min(freq.shape) == 1):
    #     freq = freq.flatten()
    # get number of freq points and set size of model output
    # Notice here, all variavels are row vectors:
    freq = freq.ravel()
    ZOL = ZOL.ravel()
    U = U.ravel()
    Z = Z.ravel()
    Dz = Dz.ravel()
    Zi = Zi.ravel()
    
    S = np.zeros(freq.shape)

    # Calc normalized freq - handle no z/L or no Ubar
    #limit z/L values
    U[np.where(U <= 0.0)] = 0.01; 
    #limit z/L values
    ZOL[np.where(ZOL > 3.0)] = 3; 
    ZOL[np.where(ZOL < -3.0)] = -3; 

    freq = freq * ((Z-Dz) / U)

    # Find stable and unstable conditions
    idu = np.where(ZOL <= 0)
    ids = np.where(ZOL >  0)
    # calculate unstable U spectra   (Hojstrop 1981)
    if model == 'U': 
        # unstable U  
        A = -1 * ZOL[idu]**(2/3)
        B = (Z[idu] / Zi[idu])**(5/3)
        C = 9.546 + (1.235 * A / B**(2/5))
        C = 1 / C
        D = 210 * freq[idu]
        E = 1 + 33 * freq[idu]**(5/3)
        F = freq[idu] * A
        G = B + 2.2 * freq[idu]**(5/3)
        S[idu] = C * (D / E + F / G)
        # stable U
        A = 0.1676 + 0.2344 * ZOL[ids]
        B = 3.124 / (A**(2/3))
        C = A + B * freq[ids]**(5/3)
        S[ids] = freq[ids] / C

    # calculate unstable V spectra   (Hojstrop 1981)
    if model == 'V':
        # unstable V  
        aa = (Zi[idu] - Dz[idu]) / (Z[idu]-Dz[idu])   
        F = freq[idu] * aa
        A = (-1 * ZOL[idu] * aa)**(2/3)
        B = 0.32 * F * A;
        C = 1.0 + 1.1 * F**(5/3)
        D = 17 * freq[idu]
        E = (1 + 9.5 * freq[idu])**(5/3)
        S[idu] = B / C + D / E
        # stable V  
        A = ZOL[ids] * (0.74 + 4.7 * ZOL[ids]) / ((1 + 4.7 * ZOL[ids])**2)
        B = freq[ids] / (1.5 * A)
        C = 0.164 * B
        D = 1 + 0.164 * B**(5/3)
        S[ids] = C / D

    # calculate unstable W spectra  (Hojstrop 1981)
    if model == 'W':
        # unstable W  
        A = (-1 * ZOL[idu])**(2/3)
        B = 0.7285 + 1.4115 *A
        C = 1 / B
        D = freq[idu]
        E = 1 + 5.3 * freq[idu]**(5/3)
        F = 16 * freq[idu] * A
        G = (1 + 17 * freq[idu])**(5/3)
        S[idu] = C * (D / E + F / G)
        # stable W  
        A = 0.838 + 1.172 * ZOL[ids]
        B = 3.124 / (A**(2/3))
        C = A + B * freq[ids]**(5/3)
        S[ids] = freq[ids] / C

    # calculate  X spectra  (Moore 1981)
    if model == 'X': 
        # Find stable and unstable conditions
        iduLo = np.union1d(np.where(ZOL <= 0), np.where(freq <= 0.15))
        iduHi = np.union1d(np.where(ZOL <= 0), np.where(freq >  0.15))
        #  unstable X 
        A = 14.94 * freq[iduLo]
        B = (1 + 24 * freq[iduLo])**(5/3)
        S[iduLo] = A / B
        A = 6.827 * freq[iduHi]
        B = (1 + 12.5 * freq[iduHi])**(5/3)
        S[iduHi] = A / B
        #  unstable X 
        A = 0.0961 + 0.644 * ZOL[ids]**0.6
        B = 3.124 / (A**(2/3))
        C = A + B * freq[ids]**(5/3)
        S[ids] = freq[ids] / C

    # calculate UW spectra        - Moore 86 (Kaimal )
    if model == 'UW': 
        # Find stable and unstable conditions
        iduLo = np.union1d(np.where(ZOL <= 0), np.where(freq <= 0.24))
        iduHi = np.union1d(np.where(ZOL <= 0), np.where(freq >  0.24))
        #  unstable UW
        A = 20.78 * freq[iduLo]
        B = (1 + 31 * freq[iduLo])**1.575
        S[iduLo] = A / B
        A = 12.66 * freq[iduHi]
        B = (1 + 9.6 * freq[iduHi])**2.4;
        S[iduHi] = A / B
        # unstable UW
        A = 0.124 * (1 + 7.9 * ZOL[ids])**0.75
        B = 2.34 * A**(-1.1)
        C = A + B * freq[ids]**2.1
        S[ids] = freq[ids] / C

    # calculate unstable UX spectra
    if model == 'UX': 
        #  unstable UX
        A = 40 * freq[idu]
        B = (1 + 14 * freq[idu])**2.6
        S[idu] = A / B

        # calculate stable UX cospectra  Kaimal 73
        # cospec is normalized multiply by cov to compare with other cospec???????????????????
        A = ZOL[ids] * (0.74 + 4.7 * ZOL[ids]) / ((1 + 4.7 * ZOL[ids])**2)
        B = 2 * A
        C = (0.85 * freq[ids]) / (B + (1.7 * (freq[ids]**2.2) / (B**1.2)))
        S[ids] =  C

    # calculate unstable WX spectra      // Moore 86 (Kaimal 72)
    if model == 'WX': 
        # Find stable and unstable conditions
        iduLo = np.union1d(np.where(ZOL <= 0), np.where(freq <= 0.54))
        iduHi = np.union1d(np.where(ZOL <= 0), np.where(freq >  0.54))
        A = 12.92 * freq[iduLo]
        B = (1 + 26.7 * freq[iduLo])**1.375
        S[iduLo] = A / B
        A = 4.378 * freq[iduHi]
        B = (1 + 3.8 * freq[iduHi])**2.4
        S[iduHi] = A / B

        # calculate stable WX cospectra    Moore 86, after Kaimal 72
        A = 0.284 * (1 + 6.4 * ZOL[ids])**0.75
        B = 2.34 * A**(-1.1)
        C = A + B * freq[ids]**2.1
        S[ids] = freq[ids] / C

    return S.reshape(1, -1) # convert to row vector

def AvgSpectra(Grp,Frq,Spec,Cvar,Norm,fmin,fmax,bin_num,Slim,smean):
    # Remove nan data
    d = [
        np.where(~np.isnan(Grp))[0], 
        np.where(~np.isnan(Spec))[0],
        np.where(~np.isnan(Frq))[0],
        np.where(~np.isnan(Cvar))[0],
        np.where(np.abs(Cvar) >= Slim)[0]
    ]

    noNan = reduce(np.intersect1d, d)
    Gx = Grp[noNan]
    Frq = Frq[noNan,:]
    Spec = Spec[noNan,:]
    Cvar = Cvar[noNan]


    gkeys = np.sort(np.unique(Gx))

    # gkeys = sort(unique(Gx(:,1)));

    rg = gkeys.shape

    [rf, cf] = Frq.shape
    [rs, cs] = Spec.shape

    assert (rs == rf) & (cs == cf), 'mismatch in frequency and spectra matrix sizes'

    # make matrix of grouping values
    G1 = np.tile(Gx.reshape(-1, 1), (1, cf))

    # Make frequency key ranges
    logfmin = np.log10(fmin)
    logfmax = np.log10(fmax)

    # dlogn = (logfmax - logfmin)/bin_num
    # fkeys = np.arange(logfmin, logfmax, step = dlogn)
    fkeys = np.linspace(logfmin, logfmax, num = bin_num + 1, endpoint = True)

    fkey_edges = [-np.inf] + fkeys.tolist() + [np.inf]

    # take log10 of frequencies for averaging
    Frq = np.log10(Frq)

    if Norm == 'pre':
        Spec = Spec / np.tile(Cvar, (1, cs))


    freq_means = []
    freq_stds = []

    spec_means = []
    spec_stds = []

    counts = []

    idxs = []
    for i in range(len(fkeys) + 1):
        low = fkey_edges[i]
        up = fkey_edges[i + 1]
        idx = np.where((Frq > low) & (Frq < up))
        freq_means.append(np.nanmedian(Frq[idx]))
        freq_stds.append(np.nanstd(Frq[idx]))

        spec_means.append(np.nanmedian(Spec[idx]))
        spec_stds.append(np.nanstd(Spec[idx]))

        counts.append(len(idx[0]))
        idxs.append(low)

    #     break
    freq_means = np.array(freq_means).reshape(-1, 1)
    freq_stds = np.array(freq_stds).reshape(-1, 1)
    spec_means = np.array(spec_means).reshape(-1, 1)
    spec_stds = np.array(spec_stds).reshape(-1, 1)
    counts = np.array(counts).reshape(-1, 1)

    freq_means = 10**freq_means
    freq_stds = 10**freq_stds
    
    M = pd.DataFrame(
        np.hstack([freq_means, freq_stds, spec_means, spec_stds, counts]), 
        columns = ['Freq_mean', 'Freq_sd', 'Spec_mean', 'Spec_sd', 'Count'],
        index = idxs
    )
    
    return M
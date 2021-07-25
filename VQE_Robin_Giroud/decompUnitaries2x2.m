function output = decompUnitaries2x2(U)
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here
    syms var1 var2 var3 var4
    Y = [0, -i
        i, 0];
    Z = [1, 0
        0, -1];
    ID = [1, 0
        0, 1];
    RY(var2) = expm(-i*Y*var2);
    RZ(var3) = expm(-i*Z*var3);
    equ = exp(i*var1)*RZ(var2)*RY(var3)*RZ(var4);
    sol = solve(equ == U);
    val_alpha = simplify(sol.var1(1,1));
    val_beta = simplify(sol.var2(1,1));
    val_gamma = simplify(sol.var3(1,1));
    val_delta = simplify(sol.var4(1,1));
    output(:,:,1) = ID*exp(i*val_alpha);
    output(:,:,2) = RZ(val_beta);
    output(:,:,3) = RY(val_gamma);
    output(:,:,4) = RZ(val_delta);
end


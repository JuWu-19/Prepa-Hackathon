function [U_,temp] = decompNC(U)
n = length(U);

temp = U;

for i = 1:n
    U_(:,:,i) = eye(n);
end

for i = 2:n
%     U_(1,1,i-1) = 1/temp(1,1);

    if temp(i,1) ~= 0
       U_(1,1,i-1) = temp(1,1)/sqrt(temp(1,1)^2+temp(i,1)^2);
       U_(1,i,i-1) = temp(i,1)/sqrt(temp(1,1)^2+temp(i,1)^2);
       U_(i,1,i-1) = temp(i,1)/sqrt(temp(1,1)^2+temp(i,1)^2);
       U_(i,i,i-1) = -temp(1,1)/sqrt(temp(1,1)^2+temp(i,1)^2);
    end
    if temp(i,1) == 0 & temp(1,1) == -1
        U_(1,1,i-1) = -1;
    end
    
    temp = U;
    for j = 1:n-1
    	temp = U_(:,:,j)*temp;
    end
end

    subm = temp(2:n,2:n);
    U_(2:n,2:n,n) = inv(subm);
    temp = U_(:,:,n)*temp;
    
    
end


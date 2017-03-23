load time_dif values
%values=xlsread('qwe.xls')
fprintf('标准差')
SER=nanstd(values)

%nanstd忽略矩阵中的NAN，求各列标准差
%var(X)不忽略NAN  std(X,0,1) 求每列方差 std(X,0,2) 求每行方差

fprintf('期望')
BER=nanmean(values)
%mean不忽略NAN

eb = 1:8;

% Create a y-axis semilog plot using the semilogy function
% Plot SER data in blue and BER data in red
figure
semilogy(eb, SER, 'bo-')
hold on
semilogy(eb, BER, 'r^-')

% Turn on the grid
grid on

% Add title and axis labels
title('Mean and Standard deviation of every process')
xlabel('Security process')
ylabel('Value')

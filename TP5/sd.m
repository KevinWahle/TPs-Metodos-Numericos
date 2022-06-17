%Steepest-Descent
%
%[x,iter] = sd(func,grad,xo,tol,maxiter)
%
%Argumentos de entrada:
%=====================
%func 		= función a minimizar
%grad		= gradiente de dicha función
%xo 		= punto inicial
%tol 		= tolerancia (en el gradiente)
%maxiter 	= número máximo de iteraciones
%
%Argumentos de salida:
%====================
%x 			= locación del mínimo
%iter 		= número de iteraciones realizadas

function [x,iter] = sd(func,grad,xo,tol,maxiter)

x = xo;

for iter = 1:maxiter
	%la dirección es la opuesta al gradiente
    d = -1*feval(grad,x);
	
    if norm(d) < tol
      break;
    end
	%se realiza una minimización lineal
	%en la dirección de búsqueda
    alpha = minimizalpha(func,grad,x,d);
    x = x+alpha*d;
end


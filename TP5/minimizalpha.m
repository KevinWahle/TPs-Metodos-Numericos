%Búsqueda lineal aproximada
%
%[ alpha ] = minimizalpha(func,grad,x,d)
%
%Se busca una aproximación al mínimo de una función
%func en la dirección d. Se utiliza interpolación
%cuadrática.
%
%Argumentos de entrada:
%=====================
%func 		= función a minimizar
%grad		= gradiente de dicha función
%x	 		= punto inicial
%d	 		= dirección de búsqueda
%
%Argumentos de salida:
%====================
%alpha		= locación del mínimo


function [ alpha ] = minimizalpha(func,grad,x,d)

a = 0;
fa= feval(func,x+a*d);
b = 1;
fb= feval(func,x+b*d);
c = 1/2;
fc= feval(func,x+c*d);

k = 1;
while 1
	%(a,fa) - (c,fc) - (b,fb):
	%¿tiene forma de sonrisa?
	
	if fa > fc
		%no, sigue "bajando"
		if fc > fb
			c  = b;
			fc = fb;
			b  = 2*b;
			fb = feval(func,x+b*d);
		else
			break;
		end
	else 
		%no, está aumentando
		b  = c;
		fb = fc;
		c  = 1/2*c;
		fc = feval(func,x+c*d);
	end

	%si el intervalo es demasiado chico o
	%demasiado grande, comencemos nuevamente...
	if (b < 1e-6) || (b > 1e6)
		k = k + 1;
 		if k == 100
			break;
		end
		b = rand;
		c = b/2;
	end
end

%Si, después de muchas iteraciones, no llegamos a nada,
%devuelvo algo al azar entre 0 y 1.
if k == 100
  alpha = rand;
else
  alpha = c*((4*fc-fb-3*fa)/(4*fc-2*fb-2*fa));
end


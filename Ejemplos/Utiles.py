from itertools import cycle

class RutResult:
    
    def __init__(self, rutN, digito, esValido):
        self.RutN = rutN
        self.Digito = digito
        self.EsValido = esValido

class Util:
    
    def __init__(self) -> None:
        pass
    
    def validarRut(self, rut):
                
        rut = rut.upper()
        rut = rut.replace("-","")
        rut = rut.replace(".","")
        aux = rut[:-1]
        dv = rut[-1:]

        revertido = map(int, reversed(str(aux)))
        factors = cycle(range(2,8))
        s = sum(d * f for d, f in zip(revertido,factors))
        res = (-s)%11
        
        rutValido = None
        if str(res) == dv:
            rutValido =  True
        elif dv=="K" and res==10:
            rutValido = True
        else:
            rutValido = False
        
        return RutResult(aux, dv, rutValido)
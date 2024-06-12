from typing import Final

KEYWORDS: frozenset = frozenset({
    'algoritmo', 'principal', 'variaveis',
    'constantes', 'registro', 'funcao',
    'retorno', 'vazio', 'se', 'senao',
    'enquanto', 'leia', 'escreva', 'inteiro',
    'real', 'booleano', 'char', 'cadeia',
    'verdadeiro', 'falso'
})

DELIMITERS: frozenset = frozenset({
    ',', '.', ';', '(', ')', '[', ']', '{', '}',
    '>', '>=', '<', '<=', '!=', '==', '=',
    '+', '-', '*', '/', '++', '--',
    '\n', ' ', '!', '&&', '||'
})

INVALID_TOKENS: frozenset = frozenset({
    '#', '$', '%', '\'', ':', '@',
    '\\', '^', '`', '_', '~', '?', 
})

TOKEN_MAL_FORMADO: Final = "TMF"
PALAVRA_RESERVADA: Final = "PRE"
INDENTIFICADOR: Final = "IDE"
NUMERO: Final = "NRO"
COMENTARIO: Final = "CoM"
CADEIA_DE_CARACTERES: Final = "CAC"
CADEIA_MAL_FORMADA: Final = "CMF"
OPERADOR_RELACIONAL: Final = "REL"
OPERADOR_LOGICO: Final = "LOG"
OPERADOR_ARITMETICO: Final = "ART"
DELIMITADOR: Final = "DEL"
COMENTARIO_MAL_FORMADO: Final = "CoMF"
NUMERO_MAL_FORMADO: Final = "NMF"
INDENTIFICADOR_MAL_FORMADO: Final = "IMF"
UNKNOWN_TOKEN: Final = "UNKNOWN"

__TOKENS: set[str] = {
    'TMF', 'PRE', 'IDE', 'NRO',
    'CoM', 'CAC', 'CMF', 'REL',
    'LOG', 'ART', 'DEL', 'CoMF',
    'NMF', 'IMF'
}

__TOKENS_DICT: dict[str, str] = {"t":'t'}

TOKENS: frozenset = frozenset(__TOKENS)

# VALID_SYMBOL: Final = lambda char: 126 <= ord(char) <= 32 and ord(char) != 34
# INVALID_SYMBOL: Final = True
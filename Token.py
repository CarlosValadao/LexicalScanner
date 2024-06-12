from constants import TOKENS, UNKNOWN_TOKEN

class Token:
    def __init__(self) -> None:
        self._lexeme: str = ''
        self._token_type: str = ''
        self._line_number: int = 0
    
    def get_token_type(self) -> str:
        return self._token_type

    def get_lexeme(self) -> str:
        return self._lexeme

    def get_line_number(self) -> int:
        return self._line_number

    # return the token as a string
    # formated
    # lineNumber typeToken lexeme 
    def get_ftoken(self) -> str:
        return ''
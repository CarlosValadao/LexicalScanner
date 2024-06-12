from typing import TextIO
import constants
from os import chdir, path, sep
import Tools

# A verificacao se existencia dos arquivos nao cabe ao analisador lexico,
# e sim, na minha concepcao, ao parser de linha de comando

# A cabeca representa a posicao do cursor na linha atual (lida) do arquivo
# ela indica a coluna, ou seja, em que coluna o possivel lexema se inicia ou termina

# lexema representa o lexema encontrado

# infiles sao os nomes dos arquivos de entrada, que devem ser analisados

# delimiters sao os delimitadores da linguagem

# tokens e uma lista de tokens que sao identificados, em cada linha lida

# A cada linha lida, os tokens serao gravados no arquivo de saida


class LexcialScanner:
    def __init__(self, infiles: list[str], outfiles:list[str]) -> None:
        self.loaded_files: list[list[str]] = []
        self.__cabeca: int = 0
        self.__numero_linha: int = 1
        self.__lexema: str = ''
        # self.__EOF: bool = False
        # self.__EOL: bool = False
        self.__first_CoM_ocurrence_line = -1
        self.__file_id: int = 0
        self.__infiles: list[str] = infiles
        self.__current_input_file: TextIO = open(infiles[self.__file_id], 'r')
        self._increment_file_id()
        # list_temp = list(self.__current_file.readline())
        # self.__empty_file: bool = False
        # if not list_temp:
        #     self.__EOF = True
        #     self.__empty_file = True
        #     # self.__current_file.close()
        #     return
        # list_tempn = list_temp.copy()
        # list_tempn.append('\n')
        self.__empty_file: bool = Tools.is_empty_text_file(self.__current_input_file.fileno())
        self.__EOF = self.__empty_file
        self.__EOL = self.__empty_file
        self.__fita: list[str] = self.__get_line_from_curr_infile()
        self.__size_fita: int = len(self.__fita)
        self.__DELIMITERS: frozenset = constants.DELIMITERS
        self.__KEY_WORDS: frozenset = constants.KEYWORDS
        self.__INVALID_TOKENS: frozenset = constants.INVALID_TOKENS
        self.__scanning_block_comment:bool = False
        self.__right_tokens: list[str] = []
        self.__wrong_tokens:list[str] = []
        # self.__outfiles: list[str] = outfiles if outfiles is not None else self._get_outputfiles_names(infiles)
        self.__outfiles: list[str] = outfiles
        self.__last_token:str = constants.UNKNOWN_TOKEN

    def run(self) -> None:
        if self.__empty_file:
            print('Arquivo vazio')
            return
        else:
            while not self.__EOF:
                print("FITA -> ", self.__fita)
                while self._q0():
                    pass
                self._set_next_line_current_file()
            print(self.__right_tokens)
            print(self.__wrong_tokens)
            self._write_tokens_in_respective_outfile()
        self.__current_input_file.close()
        
    def _set_next_line_current_file(self) -> None:
        # self.__fita = list(self.__current_file.readline())
        self.__fita = self.__get_line_from_curr_infile()
        if not self.__fita:
            self.__EOF = True
        # if self.__fita and self.__fita[-1] != '\n':
        #     self.__fita.append('\n')
        self.__numero_linha += 1
        # self.__reset_line_presets()
        self.__EOL = False
        self.__size_fita = len(self.__fita)
        self.__cabeca = 0
    
    # def __reset_line_presets(self) -> None:

        # self.__last_token = constants.UNKNOWN_TOKEN
    
    def __reset_afd(self, fp:TextIO, outfilename: list[str]) -> None:
        # self.__reset_line_presets()
        # self._set_new_curr_file(input_file=fp, outfilename=outfilename)
        return
    
    # Cria a pasta files se ela nao existe na
    # pasta de trabalho e mudar o diretorio de trabalho para
    # ./files
    # def _create_files_dir(self) -> None:
    #     # get_directories = lambda file: path.isdir(file)
    #     # working_dir_files = listdir(path.abspath('.'))
    #     # dirs = list(filter(get_directories, working_dir_files))
    #     files_path = path.abspath('.') + sep + 'files'
    #     # if not 'files' in dirs:
    #     #     mkdir(files_path)
    #     chdir(files_path)
    
    def load_files(self, input_files: list[str], output_files: list[str]) -> None:
        self.loaded_files.append(input_files)
        self.loaded_files.append(output_files)
        print(self.loaded_files[0])
        print(self.loaded_files[1])
    
    def exec(self, input_files:list[str], output_files: list[str]) -> None:
        size_files = len(input_files)
        for k in range(size_files):
            self._set_new_curr_file(input_files[k], [output_files[k]])
            self.run()
    
    def _set_new_curr_file(self, input_file: str, outfilename: list[str]) -> None:
        # self._increment_file_id()
        self.__current_input_file = open(input_file, 'r')
        self.__fita = self.__get_line_from_curr_infile()
        self.__empty_file = Tools.is_empty_text_file(self.__current_input_file.fileno())
        self.__EOL = self.__empty_file
        self.__EOF = self.__empty_file
        self.__size_fita = len(self.__fita)
        self.__lexema = ''
        self.__cabeca = 0
        self.__numero_linha = 1
        self.__right_tokens = []
        self.__wrong_tokens = []
        self.__scanning_block_comment = False
        self.__first_CoM_ocurrence_line = -1
        self.__last_token = constants.UNKNOWN_TOKEN
        self.__outfiles = outfilename

    def __get_line_from_curr_infile(self) -> list[str]:
        file_line = list(self.__current_input_file.readline())
        if file_line:
            if Tools.endswithnewline(file_line):
                return file_line
            else:
                file_line.append('\n')
                return file_line
        else:
            return []

    # def _get_outputfiles_names(self, input_files:list[str]) -> list[str]:
    #     output_files_name = list(map(self._add_filename_suffix, input_files))
    #     return output_files_name
    
    # def _add_filename_suffix(self, filename:str) -> str:
    #     (filename, extension) = filename.split(sep='.')
    #     new_filename = f"{filename}-saida.{extension}"
    #     return new_filename

    def _write_tokens_in_respective_outfile(self) -> None:
        print("OUTPUT FILENAMES-> ", self.__outfiles)
        fp = open(self.__outfiles[self.__file_id-1], 'w')
        fp.writelines(self.__right_tokens)
        if not self.__wrong_tokens:
            fp.write('Sucesso!\n')
            fp.close()
            return
        else:
            fp.write('\n')
        fp.writelines(self.__wrong_tokens)
        fp.close()
        # self.__current_file.close()
    # Gera um token no seguinte formato:
    # LINHA TIPO_TOKEN LEXEMA, por ex:
    # 1, ART +
    # O token e gerado com base nas informacoes
    # guardadas nos atributos lexema, numero linha no
    # momento em que esta funcao e chamada
    def _generate_token(self, type:str) -> str:
        line = self.__first_CoM_ocurrence_line if self.__scanning_block_comment else self.__numero_linha
        return f"{line} {type} {self.__lexema}\n"

    def _set_eof(self) -> None:
        pass

    def _increment_file_id(self) -> None:
        self.__file_id += 1

    def _update_eol(self) -> None:
        self.__EOL = self.__cabeca >= self.__size_fita

    # Remove os dados temporarios guardados devida
    # a analise lexica, tais como
    # lexema, valor da cabeca
    # recebe o valor a ser incrementado na cabeca
    def _wipe_lexical_scanner(self, head_increment:int) -> None:
        self.__cabeca += head_increment
        self.__lexema = ''

    def _isvalidsymbol(self, symbol:str) -> bool:
        decimal_ascii_symbol = ord(symbol)
        return 32 <= decimal_ascii_symbol <= 126 and decimal_ascii_symbol != 34

    def _open_infile(self, infile):
        pass

    def _type_token(self, token:str) -> str:
        if 'DEL' in token:
            return 'DEL'
        elif 'REL' in token:
            return 'REL'
        elif 'LOG' in token:
            return 'LOG'
        elif 'IDE' in token:
            return 'IDE'
        elif 'IMF' in token:
            return 'IMF'
        elif 'CAC' in token:
            return 'CAC'
        elif 'CMF' in token:
            return 'CMF'
        elif 'ART' in token:
            return 'ART'
        elif 'CoM' in token:
            return 'CoM'
        elif 'CoMF' in token:
            return 'CoMF'
        elif 'TMF' in token:
            return 'TMF'
        elif 'PRE' in token:
            return 'PRE'
        else:
            return 'UNKNOWN'

    def _decrement_head(self, value:int=1) -> None:
        if self.__EOL:
            self.__EOL = False
        self.__cabeca -= value

    def _update_file_id(self) -> None:
        self.__file_id += 1

    def _update_head(self) -> None:
        self.__cabeca += 1
    
    def _update_line(self) -> None:
        self.__numero_linha += 1

    def _add_token(self, token:str) -> None:
        self.__right_tokens.append(token)
    
    def _add_wrong_token(self, token:str) -> None:
        self.__wrong_tokens.append(token)
    
    def _set_fita(self) -> None:
        self.__fita = list(self.__current_input_file.readline())
        self.__size_fita = len(self.__fita)
        self.__numero_linha += 1

    def _get_char(self, pos:int) -> str:
        if self.__EOL:
            return '\n'
        else:
            return self.__fita[self.__cabeca]

    def _get_next_char(self) -> str:
        notEOL = self.__cabeca < self.__size_fita
        if notEOL:
            char = self.__fita[self.__cabeca]
            self._update_head()
            self._update_eol()
            return char
        else:
            self.__EOL = True
            return '\n'
    
    # Pega o token a partir da posicao atual da cabeca
    # criada para fazer com que _q0 seja invocada de forma
    # esporadica no programa, mais em especifico
    # para "ver" o proximo token ao encontrar o caractere
    # menos, para determinar se ele sera um ART ou um NRO
    def _get_token(self) -> None:
        self._q0()
    
    def _set_last_token(self, token:str) -> None:
        self.__last_token = token
    
    # Responsavel por gerar um token e armazena-lo
    # na lista de tokens do objeto e corrigir a posicao
    # da cabeca de leitura ao formar um lexema
    # o tipo do token e fornecido tem type
    # e o incremento da cabeca de leitura em head_increment
    def _handle_token(self, type:str, wrong_token:bool, head_increment:int = 0) -> None:
        token = self._generate_token(type)
        if wrong_token:
            self._add_wrong_token(token)
        else:
            self._add_token(token)
        self._wipe_lexical_scanner(head_increment)
        self.__last_token = token
    
    # eu fiz uma adaptacao nessa funcao para que ela funcione
    # retornando um bool para que eu consiga saber o final da linha
    # para poder para o laco que roda na funca run (self.__run)
    # Entao esta funcao retorna False quando chegou ao final da linha
    # pois nesta fase esta sendo testada apenas a primeira linha do arquivo,
    # e True caso contrario
    
    # Estado inicial
    def _q0(self) -> bool:
        char = self._get_next_char()
        if char == '\n':
            return False
        #Espaco em branco (que e ignorado)
        if char == " ":
            return True
        # Final da linha do arquivo
        # elif char == '\n':
        #     return False
        elif self._isvalidsymbol(char):
            self.__lexema += char
            #----------- Operadores relacionais -----------
            if char == '>':
                self._q1()
            elif char == '=':
                self._q2()
            elif char == '!':
                self._q3()
            elif char == '<':
                self._q4()
            #----------- Operadores logicos -----------
            elif char == '|':
                self._q5()
            elif char == '&':
                self._q6()
            #----------- Delimitadores -----------
            elif char == ',':
                self._DEL()
            elif char == '.':
                self._DEL()
            elif char == ';':
                self._DEL()
            elif char == '(':
                self._DEL()
            elif char == ')':
                self._DEL()
            elif char == '[':
                self._DEL()
            elif char == ']':
                self._DEL()
            elif char == '{':
                self._DEL()
            elif char == '}':
                self._DEL()
            #----------- Indentificadores -----------
            elif char.isalpha():
                self._q7()
            #----------- Operadores Aritmeticos ou Comentarios -----------
            elif char == '+':
                self._q18()
            elif char == '-':
                self._q19()
            elif char == '*':
                self._q20()
            elif char == '/':
                self._q21()
            #----------- Numeros (sem sinal) -----------
            elif char.isdecimal():
                self._q9()
            elif char in self.__INVALID_TOKENS:
                self._TMF()
        #----------- Cadeia de caracteres -----------
        elif char == '"':
            self.__lexema = char
            self._q12()
        #--------------------------------------------
        elif char == '\t':
            pass
        else:
            self.__lexema += char
            self._TMF()
            return True
        if self.__EOL:
            self._set_next_line_current_file()
        # End Of Current File
        if self.__EOF:
            self._write_tokens_in_respective_outfile()
            return False
        return True

    def _q1(self) -> None:
        char = self._get_next_char()
        if char == '=':
            self.__lexema += char
            self._REL()
            # token = self._generate_token(type="REL")
            # self._add_token(token)
            # self.__lexema = ''
            # self._q0()
        elif char != '=':
            self._REL()
            # token = self._generate_token(type="REL")
            # self._add_token(token)
            # self.__cabeca -= 1
            # self.__lexema = ''
            # self._q0() 

    def _q2(self) -> None:
        char = self._get_next_char()
        if char == '=':
            self.__lexema += char
            self._REL()
        elif char != '=':
            self._REL()

    def _q3(self) -> None:
        char = self._get_next_char()
        if char == '=':
            self.__lexema += char
            self._REL()
            # token = self._generate_token(type="REL")
            # self._add_token(token)
            # self.__lexema = ''
            # self._q0()
        elif char != '=':
            # token = self._generate_token(type="LOG")
            # self._add_token(token)
            # self.__lexema = ''
            # self.__cabeca -= 1
            # self._q0()
            self._LOG()
            
    def _q4(self) -> None:
        char = self._get_next_char()
        if char == '=':
            self.__lexema += char
            self._REL()
        elif char != '=':
            self._REL()

    def _REL(self) -> None:
        token = self._generate_token(type="REL")
        self._add_token(token)
        head_increment = -1 if len(self.__lexema) == 1 else 0
        self._wipe_lexical_scanner(head_increment=head_increment)
        self._set_last_token(token=token)

    def _LOG(self) -> None:
        token = self._generate_token(type="LOG")
        self._add_token(token)
        head_increment = -1 if self.__lexema == '!' else 0
        self._wipe_lexical_scanner(head_increment=head_increment)
        self._set_last_token(token=token)

    def _TMF(self) -> None:
        self._handle_token(type="TMF", wrong_token=True)
        # token = self._generate_token(type="TMF")
        # self._add_token(token)
        # head_increment = 0
        # self._wipe_lexical_scanner(head_increment=head_increment)
        # self._update_head()
    
    def _ART(self) -> None:
        token = self._generate_token(type="ART")
        self._add_token(token)
        # FAlta estudar e definir
        head_increment = 0
        self._wipe_lexical_scanner(head_increment=head_increment)
        self._set_last_token(token=token)
        
    def _IDE(self) -> None:
        token_type = "PRE" if self.__lexema in self.__KEY_WORDS else "IDE"
        token = self._generate_token(type=token_type)
        self._add_token(token)
        self._wipe_lexical_scanner(0)
        self._set_last_token(token=token)
    
    # Acho que nao precisa de implementar este metodo
    # por agora ou talvez nunca
    def _KEYW(self) -> None:
        pass
    
    def _IMF(self) -> None:
        self._handle_token(type="IMF", wrong_token=True)
        # token = self._generate_token(type="IMF")
        # self._add_token(token)
        # head_increment = 0
        # self._wipe_lexical_scanner(head_increment=head_increment)
    
    def _DEL(self) -> None:
        token = self._generate_token(type="DEL")
        self._add_token(token)
        head_increment = 0
        self._wipe_lexical_scanner(head_increment=head_increment)
        self._set_last_token(token=token)
        
    def _CAC(self) -> None:
        token_type = "CAC"
        self._handle_token(token_type, wrong_token=False)
    
    def _CMF(self) -> None:
        self.__lexema = self.__lexema[:-1] if self.__lexema[-1] == '\n' else self.__lexema
        self._handle_token(type="CMF", wrong_token=True)
    
    def _CoMF(self) -> None:
        # token = self._generate_token("CoMF")
        # self._add_wrong_token(token)
        # self._set_next_current_file()
        self._handle_token(type="CoMF", wrong_token=True)
    
    def _CoM(self) -> None:
        self.__first_CoM_ocurrence_line = -1
        self.__scanning_block_comment = False
        self.__lexema = ''
    
    def _NRO(self) -> None:
        self._handle_token(type="NRO", wrong_token=False)
        self.__last_token = 'NRO'
    
    def _NMF(self) -> None:
        self._handle_token(type="NMF", wrong_token=True)
        self.__last_token = 'NMF'
        
    def _q5(self) -> None:
        char = self._get_next_char()
        if char == '|':
            self.__lexema += char
            self._LOG()
        elif char != '|':
            self._TMF()

    def _q6(self) -> None:
        char = self._get_next_char()
        if char == '&':
            self.__lexema += char
            self._LOG()
        elif char != '&':
            self._TMF()

    def _q7(self) -> None:
        char = self._get_next_char()
        isalpha = char.isalpha()
        isdigit = char.isdecimal()
        isunderline = char == '_'
        has_delimiter = char in self.__DELIMITERS or \
            (char + self._get_char(self.__cabeca+1)) in self.__DELIMITERS
        if isalpha or isdigit or isunderline:
            self.__lexema += char
            self._q7()
        elif has_delimiter:
            # self.__cabeca -= 1
            self._decrement_head()
            self._IDE()
        elif not isalpha and not isdigit and not isunderline and char not in self.__DELIMITERS:
            self.__lexema += char
            self._q8()

    # Este metodo que faz a parte
    # de quando ha um IDM (Identificador Mal Formado)
    # Ele e o handle handle IDM
    def _q8(self) -> None:
        char = self._get_next_char()
        if char not in self.__DELIMITERS:
            self.__lexema += char
            self._q8()
        elif char in self.__DELIMITERS:
            self._IMF()
        
    def _q9(self) -> None:
        char = self._get_next_char()
        char_in_delimiter = char in self.__DELIMITERS
        char_and_next_char_in_delimiter = (char + self._get_char(self.__cabeca+1)) in self.__DELIMITERS
        if char.isdecimal():
            self.__lexema += char
            self._q9()
        elif char == '.':
            self.__lexema += char
            self._q10()
        elif char_in_delimiter or char_and_next_char_in_delimiter:
            if char != '\n':
                self._decrement_head()
            # self.__cabeca -= 1
            self._NRO()
        elif not char_in_delimiter and not char_and_next_char_in_delimiter and not char.isdecimal():
            self.__lexema += char
            self._q11()

    def _q10(self) -> None:
        char = self._get_next_char()
        char_in_delimiter = char in self.__DELIMITERS
        char_and_next_char_in_delimiter = (char + self._get_char(self.__cabeca+1)) in self.__DELIMITERS
        if char.isdecimal():
            self.__lexema += char
            self._q10()
        elif char == '.':
            self.__lexema += char
            self._q11()
        elif char_in_delimiter or char_and_next_char_in_delimiter:
            self._decrement_head()
            self._NRO()
        elif not char_in_delimiter and not char_and_next_char_in_delimiter and not char.isdecimal():
            self.__lexema += char
            self._q11()

    def _q11(self) -> None:
        char = self._get_next_char()
        char_in_delimiter = char in self.__DELIMITERS
        char_and_next_char_in_delimiter = (char + self._get_char(self.__cabeca+1)) in self.__DELIMITERS
        if char_in_delimiter or char_and_next_char_in_delimiter:
            self._decrement_head()
            self.__EOL = False
            self._NMF()
        elif not char_in_delimiter and not char_and_next_char_in_delimiter:
            self.__lexema += char
            self._q11()

    def _q12(self) -> None:
        char = self._get_next_char()
        if char == '\n':
            self._CMF()
        elif self._isvalidsymbol(char):
            self.__lexema += char
            self._q12()
        elif char == '"':
            self.__lexema += char
            self._CAC()
        elif not self._isvalidsymbol(char):
            self.__lexema += char
            self._q13()
    
    def _q13(self) -> None:
        char = self._get_next_char()
        if char == '"':
            self.__lexema += char
            self._CMF()
        elif char == '\n':
            self._CMF()
        else:
            self.__lexema += char
            self._q13()
    
    def _q14(self) -> None:
        pass

    def _q15(self) -> None:
        char = self._get_next_char()
        self.__lexema += char
        while not self.__EOL:
            char = self._get_next_char()
            self.__lexema += char
        self._CoM()
           
    def _q16(self) -> None:
        char = self._get_next_char()
        if char == '/':
            self._CoM()
        elif char != '/':
            self._q17()
        
    def _q17(self) -> None:
        char = self._get_next_char()
        self.__lexema += char
        while not self.__EOL and char != '*':
            char = self._get_next_char()
            self.__lexema += char
        if self.__EOF:
            self._CoMF()
        elif self.__EOL:
            self._set_next_line_current_file()
            self._q17()
        elif char == '*':
            self._q16() 
    
    def _q18(self) -> None:
        char = self._get_next_char()
        if char == '+':
            self.__lexema += char
            self._ART()
        else:
            self._decrement_head()
            self._ART()
    
    def _q19(self) -> None:
        char = self._get_next_char()
        type_last_token = self.__last_token
        next_char = self._get_char(self.__cabeca)
        if self.__last_token == 'UNKNOWN' and char.isdecimal():
            self.__lexema += char
            self._q9()
        elif self.__last_token == 'UNKNOWN' and not char.isdecimal():
            self._decrement_head()
            self._ART()
        elif char == '-':
            self.__lexema += char
            self._ART()
        elif type_last_token == 'IDE' or type_last_token == 'IMF':
            self._decrement_head()
            self._ART()
        elif type_last_token == 'NRO' or type_last_token == 'NMF':
            self._decrement_head()
            self._ART()
        elif type_last_token != 'NRO' and type_last_token != 'NMF' and \
            type_last_token != 'IDE' and type_last_token != 'IMF':
                if char.isdecimal():
                    self.__lexema = '-' + char
                    self._q9()
                # Logica para pegar o proximo token
                elif char.isalpha():
                    self._decrement_head()
                    self._ART()
                    # llxema = char
                    # char = self._get_next_char()
                    # while char.isalpha() or char.isdecimal() or char == '_':
                    #     llxema += char
                    # if llxema in self.__KEY_WORDS:
                    #     self._decrement_head()
                    #     self._ART()
                    # else:
                    #     self.__lexema = '-' + llxema

                else:
                    self._decrement_head()
                    self._ART()
            
    def _q20(self) -> None:
        self._ART()
    
    # Checkpoint
    # Estado responsavel pelo caractere / dos
    # operadores aritmeticos
    def _q21(self) -> None:
        char = self._get_next_char()
        self.__lexema += char
        if char == '*':
            self.__scanning_block_comment = True
            self.__first_CoM_ocurrence_line = self.__numero_linha
            self._q17()
        elif char == '/':
            self._q15()
        # Aqui so pode ser um caractere que e diferente de
        # / e *, por implicacao das duas verificacoes feitas acima
        else:
            self.__lexema = self.__lexema[:-1]
            self._decrement_head()
            self._ART()
    def _q22(self) -> None:
        pass
    
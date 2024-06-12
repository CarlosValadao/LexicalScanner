
from LexcialScanner import LexcialScanner
from os import chdir, path, listdir, sep, mkdir
import Tools

# negrito = "\033[1m"
# reset = "\033[0m"
# get_directories = lambda file: path.isdir(file)
# working_dir_files = listdir(path.abspath('.'))
# dirs = list(filter(get_directories, working_dir_files))
# files_path = path.abspath('.') + sep + 'files'
# if not 'files' in dirs:
#     print(negrito + 'Por favor, crie uma pasta chamada "files" na raiz do projeto\n \
#         (1) E adicione os seus arquivos de entrada\n\
#          (2) Quaislquer dúvidas leia README.txt ou então execute\n\
#                 python main.py -h' + reset)
#     exit(1)
# chdir(files_path)

# parser = cli_parser()
# inputfiles = parser['infiles']
# outputflies = parser['outputfiles']

# get_filename = lambda file: file.split(sep)[-1]

# input_filenames = list(map(get_filename, inputfiles))
# output_filenames = list(map(get_filename, outputflies)) if outputflies != None else None

WORK_DIR = './files'
LEXICAL_SCANNER_FILES_SUFFIX = '-lexico-temp'

Tools.change_dir(path=WORK_DIR)
input_filenames = Tools.get_input_filenames()
output_filenames = Tools.generate_output_filenames(input_filenames, LEXICAL_SCANNER_FILES_SUFFIX)

# input_filenames = ['input.txt']
# output_filenames = None
if input_filenames:
    print(input_filenames)
    print(output_filenames)
    scanner = LexcialScanner(infiles=[input_filenames[0]], outfiles=output_filenames)
    scanner.run()
    scanner.exec(input_filenames[1:], output_filenames[1:])
    scanner.load_files(input_filenames[1:], output_filenames[1:])    
    # scanner.run()
    # # # for i in range(l
    # en(input_filenames)):
    #     # out = output_filenames[i] if output_filenames != None else None
    #     scanner = LexcialScanner(infiles=[input_filenames[i]], outfiles=output_filenames)
    #     scanner._run()
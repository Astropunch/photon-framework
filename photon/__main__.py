import sys

try:
    from .parser import Parser
except ImportError:
    print("Error: Please use 'python -m photon' instead")
    sys.exit(1)

def main():
    Parser(sys.argv[1:]).run()
    
main()
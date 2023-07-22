from journal_manager import JournalManager

def main():
    a = 'C'
    for i in range(5):
        a = chr(ord(a)+1)
        print(a)



if __name__ == '__main__':
    main()
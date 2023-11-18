import sys

def main():
    # Mengecek jumlah argumen yang diberikan
    if len(sys.argv) != 3:
        print("Cara penggunaan: python main.py <nama_file_pda> <nama_file_input>")
        return

    # Mengambil nama file dari argumen baris perintah
    pda_file = sys.argv[1]
    input_file = sys.argv[2]

    # Lakukan operasi Anda pada file-file ini
    # Contoh: Buka dan baca isi dari file
    try:
        with open(pda_file, 'r') as pda:
            pda_content = pda.read()
        with open(input_file, 'r') as input_acc:
            input_content = input_acc.read()

        # Lakukan operasi Anda dengan isi file yang telah dibaca
        # Misalnya: cetak isi file
        print("Isi dari pda.txt:", pda_content)
        print("Isi dari inputAcc.html:", input_content)

    except FileNotFoundError:
        print("File tidak ditemukan.")

if __name__ == "__main__":
    main()

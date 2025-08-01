import java.util.Scanner;

public class CryptoSimple {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("1. Crypter");
        System.out.println("2. Decrypter");
        System.out.print("Choix : ");
        int choice = Integer.parseInt(sc.nextLine());

        System.out.print("Mot : ");
        String input = sc.nextLine();

        System.out.print("Clé : ");
        String key = sc.nextLine();

        String output = xorCipher(input, key);

        if (choice == 1) {
            System.out.println("Texte chiffré : " + toHex(output));
        } else {
            System.out.println("Texte déchiffré : " + output);
        }

        sc.close();
    }

    static String xorCipher(String text, String key) {
        char[] result = new char[text.length()];
        for (int i = 0; i < text.length(); i++) {
            result[i] = (char)(text.charAt(i) ^ key.charAt(i % key.length()));
        }
        return new String(result);
    }

    static String toHex(String input) {
        StringBuilder sb = new StringBuilder();
        for (char c : input.toCharArray()) {
            sb.append(String.format("%02X", (int)c));
        }
        return sb.toString();
    }
}

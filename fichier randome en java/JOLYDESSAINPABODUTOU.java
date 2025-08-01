import javax.swing.*;
import java.awt.*;
import java.util.Random;

public class JoliDessins extends JPanel {

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Random rand = new Random();

        for (int i = 0; i < 100; i++) {
            int x = rand.nextInt(getWidth());
            int y = rand.nextInt(getHeight());
            int w = rand.nextInt(100) + 10;
            int h = rand.nextInt(100) + 10;

            Color c = new Color(rand.nextInt(256), rand.nextInt(256), rand.nextInt(256));
            g.setColor(c);

            if (rand.nextBoolean()) {
                g.fillOval(x, y, w, h);
            } else {
                g.drawLine(x, y, x + w, y + h);
            }
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Dessins Aléatoires");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);
        frame.add(new JoliDessins());
        frame.setVisible(true);
    }
}
